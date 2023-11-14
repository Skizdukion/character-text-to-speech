from pydantic import BaseModel, Field, validator
from typing import Union, Literal
import os

class generate_web(BaseModel):
    text: Union[str, None] = None
    char: str = Field(...)

    @validator('char')
    def check_char(cls, v):
        foler_path = '/src/voices/' + v;
        if not os.path.isdir(folder_path):
            raise ValueError('Char is not valid')
        return v

    class Config:
        orm_mode = True