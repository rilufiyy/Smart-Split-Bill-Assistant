
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import json
import re

from modules.data.receipt_data import ItemData, ReceiptData
from .base import AIModel

MODEL_ID = "vikhyatk/moondream2"
REVISION = "2024-08-26"

class MoondreamModel(AIModel):
    """Receipt reader based on Moondream2 (CPU Friendly)."""

    def __init__(self) -> None:
        """Initialize the model."""
        self.device = "cpu" # Strict CPU
        
        print(f"Loading {MODEL_ID} on {self.device}...")
        
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID, 
            trust_remote_code=True,
            revision=REVISION
        ).to(self.device).eval()
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_ID, 
            revision=REVISION
        )

    def run(self, image: Image.Image) -> ReceiptData:
        """Retrieve data from the receipt.

        Args:
            image (Image.Image): the receipt photo image

        Returns:
            ReceiptData: parsed receipt data
        """
        enc_image = self.model.encode_image(image)
        
        prompt = "Extract all items, quantity, and price from this receipt. Return valid JSON only with keys 'items' (list of {name, count, price}) and 'total'."
        
        # Moondream generation
        response = self.model.answer_question(enc_image, prompt, self.tokenizer)
        
        return self._parse_json_result(response)

    def _parse_json_result(self, text: str) -> ReceiptData:
        """Parse JSON-like response."""
        # Clean up markdown code blocks if any
        json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try finding first { and last }
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1:
                json_str = text[start:end+1]
            else:
                return ReceiptData(items={}, total=0.0)

        try:
            data = json.loads(json_str)
            items_list = data.get("items", [])
            total_val = data.get("total", 0.0)
            
            # Convert to ReceiptData
            items = []
            for it in items_list:
                name = it.get("name", "Unknown")
                count = it.get("count", 1)
                price = it.get("price", 0.0)
                
                # Ensure types
                try: count = int(count)
                except: count = 1
                try: price = float(str(price).replace(',', '').replace('Rp', ''))
                except: price = 0.0
                try: total_val = float(str(total_val).replace(',', '').replace('Rp', ''))
                except: pass

                items.append(ItemData(name=name, count=count, total_price=price))
                
            return ReceiptData(items={item.id: item for item in items}, total=float(total_val) if total_val else 0.0)
            
        except json.JSONDecodeError:
            # Fallback if JSON is malformed
            return ReceiptData(items={}, total=0.0)
