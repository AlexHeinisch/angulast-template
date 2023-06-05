from typing import List
from app.schemas.auth_schemas import Permission, Token, TokenPayload, TokenType
import jwt
from app.exceptions import InvalidTokenException, ExpiredTokenException
from app.config import settings
from datetime import datetime

class TokenService:

    def verify_access_token_and_get_payload(self, token: Token) -> TokenPayload:
        try:
            payload = jwt.decode(
                jwt=token.token,
                key=settings.access_token_pubkey,
                algorithms=[settings.access_token_algo],
                audience=TokenType.ACCESS
            )
            return TokenPayload(
                subject=payload['sub'],
                expiration_time=datetime.fromtimestamp(payload['exp']),
                audience=payload['aud'],
                issuer=payload['iss'],
                issued_at=datetime.fromtimestamp(payload['iat']),
                jwt_id=payload['jti'],
                permissions=payload['permissions']
            )
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenException(detail={'message': 'Access token expired!'})
        except:
            raise InvalidTokenException(detail={'message': 'Invalid token!'})
