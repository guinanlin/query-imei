from pydantic import BaseModel

class IMEIRequest(BaseModel):
    imei: str

class CSPireResponse(BaseModel):
    code: int
    result: str

class TokenResponse(BaseModel):
    token: str
    expires: int
    sessionId: str
    loggedIn: bool

class DeviceUnlockResponse(BaseModel):
    code: int
    result: dict 