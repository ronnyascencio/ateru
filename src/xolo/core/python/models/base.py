from __future__ import annotations

import uuid
from typing import Annotated, ClassVar

from annotated_types import MinLen
from pydantic import BaseModel, ConfigDict, Field


def generate_id() -> str:
    """
    Generate a unique, stable ID for each model instance.
    UUID4 is enough for pipeline-level uniqueness.
    """
    return uuid.uuid4().hex


class XoloBaseModel(BaseModel):
    """
    Base model for all Xolo pipeline entities.
    """

    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    id: str = Field(default_factory=generate_id)
    name: Annotated[str, MinLen(2)]
