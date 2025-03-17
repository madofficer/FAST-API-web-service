from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status

from source.auth.utils import decode_token


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict | None:
        creds = await super().__call__(request)

        token = creds.credentials

        if self.token_valid(token):
            token_data = decode_token(token)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token"
            )

        self.verify_token_data(token_data)

        return token_data

    @staticmethod
    def token_valid(token: str) -> bool:
        return True if decode_token(token) else False

    def verify_token_data(self, token_data: dict) -> None:
        NotImplementedError()


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Provide an access token"
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Provide a refresh token"
            )
