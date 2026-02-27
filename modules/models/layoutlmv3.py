import re
import torch
from PIL import Image
import pytesseract
from pytesseract import Output
from transformers import LayoutLMv3Processor, LayoutLMv3Model
import os
import time
from huggingface_hub import HfApi

from .base import AIModel

import os

# TESSERACT PATH CONFIGURATION
tesseract_path = os.getenv("TESSERACT_CMD")
if tesseract_path is None:
    if os.name == 'nt':  
        tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    else: 
        tesseract_path = "tesseract"  

pytesseract.pytesseract.tesseract_cmd = tesseract_path

# HTTP TIMEOUT CONFIGURATION
# Increase timeout for downloading large models from Hugging Face
os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", "300")  
os.environ.setdefault("HTTPX_TIMEOUT", "300")  

MODEL_NAME = "microsoft/layoutlmv3-base"


class LayoutLMv3ReceiptModel(AIModel):
    """
    Receipt Extraction Model
    - OCR with pytesseract
    - Regex-based parsing (Indonesia-friendly)
    - LayoutLMv3 ready (forward skipped)
    """

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load with retry mechanism and increased timeout
        max_retries = 3
        retry_delay = 5 
        
        for attempt in range(max_retries):
            try:
                print(f"Loading LayoutLMv3 processor (attempt {attempt + 1}/{max_retries})...")
                self.processor = LayoutLMv3Processor.from_pretrained(
                    MODEL_NAME,
                    apply_ocr=False,
                    local_files_only=False
                )
                
                print(f"Loading LayoutLMv3 model (attempt {attempt + 1}/{max_retries})...")
                self.model = LayoutLMv3Model.from_pretrained(
                    MODEL_NAME,
                    local_files_only=False
                ).to(self.device)
                self.model.eval()
                
                print("LayoutLMv3 model loaded successfully!")
                break  
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Failed to load model (attempt {attempt + 1}): {e}")
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    # Last attempt failed
                    raise RuntimeError(
                        f"Failed to load LayoutLMv3 model after {max_retries} attempts. "
                        f"This may be due to network issues or Hugging Face being unavailable. "
                        f"Please check your internet connection and try again. "
                        f"Last error: {str(e)}"
                    ) from e

    # PUBLIC API
    def run(self, image):
        if isinstance(image, str):
            image = Image.open(image).convert("RGB")

        words, boxes = self._ocr(image)

        # LayoutLMv3 forward 
        self._layoutlm_forward(image, words, boxes)

        return self._parse(words, boxes)

    # OCR
    def _ocr(self, image):
        data = pytesseract.image_to_data(image, output_type=Output.DICT)

        words, boxes = [], []
        w, h = image.size

        for i, text in enumerate(data["text"]):
            text = text.strip()
            if not text:
                continue

            words.append(text)

            x1 = int(1000 * data["left"][i] / w)
            y1 = int(1000 * data["top"][i] / h)
            x2 = int(1000 * (data["left"][i] + data["width"][i]) / w)
            y2 = int(1000 * (data["top"][i] + data["height"][i]) / h)

            boxes.append([x1, y1, x2, y2])

        return words, boxes

    # LayoutLMv3 FORWARD
    def _layoutlm_forward(self, image, words, boxes):
        """
        LayoutLMv3 forward pass
        (OCR + parsing already sufficient for receipt)
        """
        pass

    # GROUP WORDS BY LINE
    def _group_by_line(self, words, boxes, y_thresh=15):
        lines = []
        current = []
        last_y = None

        for w, b in zip(words, boxes):
            y = b[1]
            if last_y is None or abs(y - last_y) <= y_thresh:
                current.append(w)
            else:
                lines.append(" ".join(current))
                current = [w]
            last_y = y

        if current:
            lines.append(" ".join(current))

        return lines

    # MAIN PARSER
    def _parse(self, words, boxes):
        from modules.data.receipt_data import ReceiptData

        lines = self._group_by_line(words, boxes)

        items = []
        total = 0.0

        for line in lines:
            low = line.lower()

            # TOTAL / TAGIHAN 
            if any(k in low for k in ["total", "tagihan", "grand total"]):
                total = self._extract_amount(line)
                continue

            # ITEM 
            item = self._parse_item(line)
            if item:
                items.append(item)

        # fallback total
        if total == 0.0:
            total = sum(i.total_price for i in items)

        return ReceiptData(
            items={item.id: item for item in items},
            total=total
        )

    # ITEM PARSER
    def _parse_item(self, line):
        from modules.data.receipt_data import ItemData

        nums = re.findall(r"\d+(?:[.,]\d+)?", line)
        if not nums:
            return None

        try:
            if len(nums) == 1:
                count = 1
                total_price = self._to_float(nums[0])
            else:
                count = int(nums[0])
                total_price = self._to_float(nums[-1])

            name = re.sub(r"\d+(?:[.,]\d+)?", "", line)
            name = re.sub(r"\s{2,}", " ", name).strip()

            if len(name) < 2:
                return None

            blacklist = [
                "total", "subtotal", "tax",
                "service", "ppn", "diskon", "tagihan", "serv. charge %", "pajak %"
            ]
            if any(b in name.lower() for b in blacklist):
                return None

            return ItemData(
                name=name,
                count=max(count, 1),
                total_price=total_price
            )

        except Exception:
            return None

    # UTILS
    def _extract_amount(self, text):
        nums = re.findall(r"\d+(?:[.,]\d+)?", text)
        return self._to_float(nums[-1]) if nums else 0.0

    def _to_float(self, val):
        """
        Indonesia Rupiah-safe number parser
        40.000 / 40,000 -> 40000
        """
        val = val.replace(" ", "")

        # ribuan format (IDR)
        if re.match(r"^\d{1,3}([.,]\d{3})+$", val):
            val = val.replace(".", "").replace(",", "")
            return float(val)

        # fallback decimal
        if val.count(",") == 1 and val.count(".") == 0:
            val = val.replace(",", ".")
        else:
            val = val.replace(".", "").replace(",", ".")


        return float(val)
