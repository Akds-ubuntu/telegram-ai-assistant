from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class QuestionSchema(BaseModel):
    id: int
    question: str
    answer: str
    type_questions_id: int = Field(validation_alias=AliasChoices("type_id"))
    model_config = ConfigDict(from_attributes=True)


class QuestionCreateSchema(BaseModel):
    question: str
    answer: str
    type_id: int
