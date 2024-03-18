from datetime import datetime

from pydantic import BaseModel, Field

from utils.utils import now


class CreatedUpdatedSchema(BaseModel):
    created_at: datetime = Field(default_factory=now)
    updated_at: datetime = Field(default_factory=now)

    class ConfigDict:
        from_attributes = True

    def __hash__(self):
        return hash(
            (type(self),) + tuple(getattr(self, f) for f in self.model_fields.keys())
        )
