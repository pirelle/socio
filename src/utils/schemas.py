from datetime import datetime

from pydantic import BaseModel


class CreatedUpdatedSchema(BaseModel):
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        from_attributes = True

    def __hash__(self):
        return hash(
            (type(self),) + tuple(getattr(self, f) for f in self.model_fields.keys())
        )
