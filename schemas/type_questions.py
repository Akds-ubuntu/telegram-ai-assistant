from pydantic import BaseModel, ConfigDict


class TypeQuestion(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class TypeQuestionCreate(BaseModel):
    name: str
