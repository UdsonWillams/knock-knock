from pydantic import BaseModel


class FunctionModel(BaseModel):
    date_format: str | None
    final_text_message: str | None
