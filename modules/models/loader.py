from enum import Enum
import streamlit as st

from modules.utils import SettingsError
from .base import AIModel


class ModelNames(Enum):
    """Available model names."""
    GEMINI = "Gemini"
    DONUT = "Donut"
    LAYOUTLMV3 = "LayoutLMv3"


@st.cache_resource(show_spinner="Loading AI Model...")
def load_model_cached(model_name: ModelNames) -> AIModel:
    """Load AI model with caching."""
    
    if model_name == ModelNames.GEMINI:
        from .gemini import GeminiModel
        return GeminiModel()

    elif model_name == ModelNames.DONUT:
        from .donut import DonutModel
        return DonutModel()

    elif model_name == ModelNames.LAYOUTLMV3:
        from .layoutlmv3 import LayoutLMv3ReceiptModel
        return LayoutLMv3ReceiptModel()

    raise SettingsError(f"Model loader not implemented for {model_name}")


def _load_model() -> AIModel:
    """Load model based on session settings."""
    from modules.data import session_data
    
    model_name_str = session_data.model_name.get()

    try:
        model_name = ModelNames(model_name_str)
    except ValueError:
        # Fallback if mismatch formatting
        for m in ModelNames:
            if m.value.lower() == model_name_str.lower():
                model_name = m
                break
        else:
            # Default to Gemini if not found, or raise
            raise SettingsError(f"Model name is not recognized: {model_name_str}")

    return load_model_cached(model_name)


def get_model() -> AIModel:
    """Get receipt reader model."""
    return _load_model()