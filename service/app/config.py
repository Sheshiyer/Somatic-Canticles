from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://lore:lore_local_dev@localhost:5434/canticles_lore"
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    nvidia_api_key: str = ""
    embed_model: str = "nvidia/nv-embed-v1"
    vl_embed_model: str = "nvidia/llama-nemotron-embed-vl-1b-v2"
    default_top_k: int = 10
    pilot_data_path: str = "/data/pilot"

    llm_provider: str = "nvidia"
    llm_model: str = "meta/llama-3.3-70b-instruct"
    llm_api_key: str = ""
    llm_base_url: str = "https://integrate.api.nvidia.com/v1"
    llm_max_tokens: int = 2048
    llm_temperature: float = 0.7

    model_config = {"env_prefix": "", "case_sensitive": False}


settings = Settings()