from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str
    supabase_url: str = ""
    supabase_key: str = ""
    model_name: str = "claude-sonnet-4-20250514"
    environment: str = "development"

    model_config = {"env_file": ".env"}


settings = Settings()