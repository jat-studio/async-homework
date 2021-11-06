import uuid as uuid
from django.contrib.auth.models import AbstractUser

from users.roles import UserRole


class User(AbstractUser):
    public_id: uuid
    email: str
    full_name: str
    is_active: bool
    role: UserRole
