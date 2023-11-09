from pydantic import BaseModel, Field
from typing import Union, Literal


class generate_web(BaseModel):
    text: Union[str, None] = None

    char: Literal['obama', 'vn-male', 'lucia'] = Field(...)
    class Config:
        orm_mode = True
