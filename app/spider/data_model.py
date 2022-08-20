from re import L
from pydantic import BaseModel
from datetime import datetime  
from typing import List, Optional


class Multimedia(BaseModel):

    type: str
    path: str

class Post(BaseModel):

    text: str
    is_reposted: bool
    nickname: str
    user_tag: str
    datetime: Optional[str]
    multimedia: Optional[List[Multimedia]]