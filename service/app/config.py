from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://lore:lore_local_dev@localhost:5432/canticles_lore"
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    nvidia_api_key: str = ""
    embed_model: str = "nvidia/nv-embed-v1"
    vl_embed_model: str = "nvidia/llama-nemotron-embed-vl-1b-v2"
    default_top_k: int = 10
    pilot_data_path: str = "/data/pilot"

    model_config = {"env_prefix": "", "case_sensitive": False}


settings = Settings()