from enum import Enum
from typing import Type

from modules.data import session_data
from modules.utils import SettingsError

from .base import AIModel
from .gemini import GeminiModel
from .donut import DonutModel
from .moondream_model import MoondreamModel

class ModelNames(Enum):
    """Available model names."""

    GEMINI = "Gemini"
    DONUT = "Donut"
    MOONDREAM = "Moondream2"


MODELS_LOADER: dict[ModelNames, Type[AIModel]] = {
    ModelNames.GEMINI: GeminiModel,
    ModelNames.DONUT: DonutModel,
    ModelNames.MOONDREAM: MoondreamModel,
}


def _load_model() -> AIModel:
    """Load new model.

    Raises:
        SettingsError: if the settings are not configured correctly
            and model loading failed.

    Returns:
        AIModel: loaded AI model.
    """
    model_name_str = session_data.model_name.get()
    
    # Simple mapping if string doesn't perfectly match Enum value (optional safety)
    try:
        model_name = ModelNames(model_name_str)
    except ValueError:
        # Fallback search or error
        # Try finding by value
        found = False
        for m in ModelNames:
            if m.value == model_name_str:
                model_name = m
                found = True
                break
        if not found:
             # If exact match fails, try case insensitive or partial (optional)
             raise SettingsError(f"Model name is not recognized {model_name_str}")

    if model_name not in MODELS_LOADER:
        raise SettingsError(f"Model loader not found for {model_name}")
        
    return MODELS_LOADER[model_name]()


def get_model() -> AIModel:
    """Get receipt reader model.

    Returns:
        AIModel: the loaded AI model
    """
    model = session_data.model.get()
    if model is None:
        model = _load_model()
        session_data.model.set(model)
    return model