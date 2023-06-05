from enum import Enum
from datetime import datetime
from typing import Any, Dict, List
import uuid

from pydantic import BaseModel


class Permission(str, Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'

class TokenType(str, Enum):
    REFRESH = 'REFRESH'
    ACCESS = 'ACCESS'

class GrantedPermission(BaseModel):
    user_id: int
    permission: Permission

    class Config:
        orm_mode = True

class Token(BaseModel):
    token: str
    token_type: TokenType

class TokenPayload(BaseModel):
    # standard claims
    subject: int
    expiration_time: datetime
    audience: str
    issuer: str
    issued_at: datetime
    jwt_id: str = str(uuid.uuid4())

    # custom claims
    permissions: List[Permission] | None = None
    

    def to_claim_dict(self) -> Dict[str, Any]:
        d = dict()
        d['sub'] = self.subject
        d['exp'] = self.expiration_time.timestamp()
        d['iss'] = self.issuer
        d['aud'] = self.audience
        d['iat'] = self.issued_at.timestamp()
        d['jti'] = self.jwt_id
        if self.permissions:
            d['permissions'] = self.permissions
        return d
    
