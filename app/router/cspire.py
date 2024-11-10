from fastapi import APIRouter, HTTPException
from app.models.cspire import IMEIRequest, CSPireResponse, DeviceUnlockResponse
from app.services.cspire_service import CSpireService

router = APIRouter()

@router.post("/cspire", response_model=CSPireResponse)
async def check_cspire_imei(request: IMEIRequest):
    try:
        code, result = await CSpireService.check_imei(request.imei)
        return {"code": code, "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": 1, "result": f"服务器错误: {str(e)}"}
        )

@router.get("/imei-lockstatus/{imei}", response_model=DeviceUnlockResponse)
async def get_imei_lockstatus(imei: str, isProxy: str = "N"):
    try:
        code, result = await CSpireService.get_imei_lockstatus(imei, isProxy)
        return {"code": code, "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"code": 1, "result": f"服务器错误: {str(e)}"}
        )

@router.get("/test-proxy")
async def test_proxy():
    result = await CSpireService.test_proxy()
    return {"result": result}