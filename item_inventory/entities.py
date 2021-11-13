from dataclasses import dataclass
from typing import Optional


@dataclass
class User:

    id: int
    public_id: str
    email: str
    full_name: str
    role: str


@dataclass
class Item:

    id: int
    public_id: str
    title: str
    description: str
    status: str
    user_id: Optional[int]
