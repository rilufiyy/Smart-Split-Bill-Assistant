# gemini.py
import base64
import json
import os
from io import BytesIO
from typing import TYPE_CHECKING

from PIL import Image

from modules.data.receipt_data import ItemData, ReceiptData
from modules.utils import AIError, SettingsError
from .base import AIModel

MODEL_NAME = "gemini-2.5-flash"

PROMPT = """
You are given an image of a receipt. Please read the content into JSON format:

{
    "menus": [
        {
            "name": <item_name>,
            "count": <purchased_count>,
            "price": <total_price_for_this_item> 
        }
    ],
    "total": <total_price_in_receipt>
}

Return only JSON.
"""


class GeminiModel(AIModel):
    """Receipt reader based on Gemini model API.
    This module is SAFE: it will only require langchain if you really use GeminiModel.
    """

    def __init__(self) -> None:
        try:
            from langchain_core.messages import HumanMessage
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError as e:
            raise SettingsError(
                "Gemini dependencies not installed. Install with:\n"
                "pip install langchain-core langchain-google-genai"
            ) from e

        if "GOOGLE_API_KEY" not in os.environ or os.environ["GOOGLE_API_KEY"] == "":
            raise SettingsError("GOOGLE_API_KEY not set.")

        self.HumanMessage = HumanMessage
        self.llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0.0)

    def run(self, image: Image.Image) -> ReceiptData:
        image_b64 = self._encode_image(image)

        message = self.HumanMessage(
            content=[
                {"type": "text", "text": PROMPT},
                {
                    "type": "image_url",
                    "image_url": f"data:image/png;base64,{image_b64}",
                },
            ]
        )

        response = self.llm.invoke([message]).content
        if not isinstance(response, str):
            raise AIError(f"Gemini response invalid: {response}")

        try:
            return self._format_response(response)
        except Exception as err:
            raise AIError(f"Unable to parse Gemini response: {response}") from err

    def _encode_image(self, image: Image.Image) -> str:
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def _format_response(self, response: str) -> ReceiptData:
        dict_data = self._parse_response_to_dict(response)

        total = float(dict_data["total"])
        menus_list = dict_data["menus"]

        items = [
            ItemData(
                name=str(item["name"]),
                count=int(item.get("count", 1)),
                total_price=float(item["price"]),
            )
            for item in menus_list
        ]

        return ReceiptData(items={it.id: it for it in items}, total=total)

    def _parse_response_to_dict(self, response: str) -> dict:
        clean_json_str = response.replace("```json", "").replace("```", "")
        return json.loads(clean_json_str)
