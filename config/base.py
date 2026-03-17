from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.constants import ENV_FILE_PATH


class Config(BaseSettings):
    BOT_TOKEN: str = Field(default="")
    DEEPGRAM_API_KEY: str = Field(default="")
    DOMEN: str = Field(default="")
    GROQ_API_KEY: str = Field(default="")
    GROQ_LLM_MODEL: str = Field(default="openai/gpt-oss-120b")
    PLATFORM_API_KEY: str = Field(default="")
    PARALLEL_MCP_URL: str = Field(default="https://mcp.parallel.ai/v1beta/search_mcp/")
    DB_NAME: str = Field(default="postgres")
    DB_USER: str = Field(default="postgres")
    DB_PASSWORD: str = Field(default="postgres")
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
