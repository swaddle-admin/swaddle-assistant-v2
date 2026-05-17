from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str
    supabase_url: str = ""
    supabase_key: str = ""
    model_name: str = "claude-sonnet-4-20250514"
    environment: str = "development"

    model_config = {"env_file": ".env"}

settings = Settings()
print(f"API KEY LOADED: {settings.anthropic_api_key[:10]}...")
print(f"SUPABASE URL: {settings.supabase_url}")
print(f"SUPABASE KEY: {settings.supabase_key[:10]}...")
print(f"MODEL: {settings.model_name}")
print(f"ENVIRONMENT: {settings.environment}")