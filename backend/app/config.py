from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    price_refresh_seconds: int = 15 * 60
    max_concurrent_requests: int = 4
    http_timeout_seconds: int = 12
    scraper_user_agent: str = "QuidlyBot/0.1 (+https://quidly.local/pricing)"
    enable_json_ld_fallback: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", case_sensitive=False)


settings = Settings()
