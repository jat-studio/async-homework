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
class Task:

    id: int
    public_id: str
    description: str
    status: str
    price: str
    assign_to_public_id: Optional[str]
