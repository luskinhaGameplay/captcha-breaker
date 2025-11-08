from pydantic import BaseModel

class Base64File(BaseModel):
    file_data: str