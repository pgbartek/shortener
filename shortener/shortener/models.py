from typing import Optional
import random

from pydantic import BaseModel

BASE56 = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz"


class Redirect(BaseModel):
    url: str
    url_id: Optional[str] = None

    @staticmethod
    def generate_url_id(length=7):
        return "".join(random.choices(BASE56, k=length))
