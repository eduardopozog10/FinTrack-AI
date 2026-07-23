from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FinTrack AI"
    version: str = "0.1.0"
    description: str = (
        "AI-powered personal finance assistant that understands natural language."
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()   