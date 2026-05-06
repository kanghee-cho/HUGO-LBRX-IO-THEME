from __future__ import annotations

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    azure_devops_org_url: str
    azure_devops_project: str
    azure_devops_pat: str
    azure_devops_wiki_id: str = ""  # defaults to "{project}.wiki" if not set
    log_level: str = "INFO"
    request_timeout: int = 30

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @model_validator(mode="after")
    def _default_wiki_id(self) -> Settings:
        if not self.azure_devops_wiki_id:
            self.azure_devops_wiki_id = f"{self.azure_devops_project}.wiki"
        return self
