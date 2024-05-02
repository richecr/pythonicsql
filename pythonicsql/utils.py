from pydantic import BaseModel, ConfigDict


class PythonicBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
