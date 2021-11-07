from datetime import datetime  
from datetime import timedelta  
import os


class AuthPayload(dict):

    def __init__(
        self,
        id: int,
        uuid: str,
        email: str,
        full_name: str,
        position: str,
        is_active: bool,
        role: str,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.email = email
        self.full_name = full_name
        self.position = position
        self.is_active = is_active
        self.role = role

        # set the expiry attrbute to 30 minutes
        self.exp = (
            datetime.utcnow() + timedelta(seconds=int(os.getenv('EXPIRESSECONDS')))
        )
