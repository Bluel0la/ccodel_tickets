from pydantic import BaseModel
from datetime import datetime

class TokenBlacklist(BaseModel):
    token: str
    expires_at: datetime
