from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str
    supabase_url: str = ""
    supabase_key: str = ""
    model_name: str = "claude-3-5-haiku-20241022"
    environment: str = "development"
    user_context_url: str = "http://localhost:3000/user-context"
    chat_history_limit: int = 3
    task_manager_url: str = "http://localhost:3006/task-manager"
    default_max_tokens: int = 512

    model_config = {"env_file": ".env"}

settings = Settings()
print(f"API KEY LOADED: {settings.anthropic_api_key[:10]}...")
print(f"SUPABASE URL: {settings.supabase_url}")
print(f"SUPABASE KEY: {settings.supabase_key[:10]}...")
print(f"MODEL: {settings.model_name}")
print(f"ENVIRONMENT: {settings.environment}")
print(f"USER CONTEXT URL: {settings.user_context_url}")