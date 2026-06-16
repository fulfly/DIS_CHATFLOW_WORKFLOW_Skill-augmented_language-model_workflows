"""Project constants that are independent of measured data values."""

DIMENSION_FIELDS = [
    "color_change",
    "shape_change",
    "surface_texture_change",
    "volume_change",
    "dissolution_speed_time",
    "physical_state_change",
    "dissolution_medium",
    "fragment_distribution_density",
]

DIMENSION_DISPLAY = {
    "color_change": "Color change",
    "shape_change": "Shape change",
    "surface_texture_change": "Surface texture change",
    "volume_change": "Area/size change",
    "dissolution_speed_time": "Dissolution speed over time",
    "physical_state_change": "Physical state change",
    "dissolution_medium": "Dissolution medium",
    "fragment_distribution_density": "Fragment distribution density",
}

MODEL_ORDER = [
    "GPT-5-mini",
    "DIS GPT",
    "Qwen3.6-plus",
    "GLM-4.6V",
    "Kimi-K2.5",
    "Gemini 2.5 Flash",
]

MODEL_ALIASES = {
    "gpt-5-mini": "GPT-5-mini",
    "gpt5-mini": "GPT-5-mini",
    "gpt-5 mini": "GPT-5-mini",
    "dis-gpt": "DIS GPT",
    "dis gpt": "DIS GPT",
    "dis gpt old": "DIS GPT",
    "qwen3.6-plus": "Qwen3.6-plus",
    "qwen-3.6-plus": "Qwen3.6-plus",
    "glm-4.6v": "GLM-4.6V",
    "glm4.6v": "GLM-4.6V",
    "kimi-k2.5": "Kimi-K2.5",
    "kimi k2.5": "Kimi-K2.5",
    "gemini": "Gemini 2.5 Flash",
    "gemini-2.5-flash": "Gemini 2.5 Flash",
    "gemini 2.5 flash": "Gemini 2.5 Flash",
    "gemini25flash": "Gemini 2.5 Flash",
}

VISCOSITY_ORDER = [
    "Low viscosity",
    "Medium viscosity",
    "High viscosity",
]

VISCOSITY_ALIASES = {
    "low": "Low viscosity",
    "low viscosity": "Low viscosity",
    "low-viscosity": "Low viscosity",
    "medium": "Medium viscosity",
    "medium viscosity": "Medium viscosity",
    "medium-viscosity": "Medium viscosity",
    "mid": "Medium viscosity",
    "high": "High viscosity",
    "high viscosity": "High viscosity",
    "high-viscosity": "High viscosity",
}

STANDARD_ALIASES = {
    "standard": "Standard",
    "reference": "Standard",
    "standard/reference": "Standard",
    "std": "Standard",
}
