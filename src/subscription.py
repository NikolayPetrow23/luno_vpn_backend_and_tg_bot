from fastapi import APIRouter, Request, Response

from src.utils.utils import make_header_vpn_config
from src.services.vpn import VPNService

router = APIRouter(prefix="/sub/client", tags=["Получение запроса от HAPP и V2RayTun"])


@router.get("/{code}")
async def sub_code(code: str, request: Request):
    try:
        scope = request.scope
        print(scope)
        headers = dict(scope.get("headers", {}))
        user_agent: str = headers.get(b"user-agent", b"").decode()[0:4]
        x_hwid: str = headers.get(b"x-hwid", b"").decode()
        device_model: str = headers.get(b"x-device-model", b"").decode()

        if x_hwid == "" or device_model == "":
            return Response(status_code=400)
        
        data: dict = await VPNService.get_config_vpn(
            code, 
            user_agent,
            x_hwid,
            device_model
        )
        
        if data.get("status", "") == "not_short_link" or data.get("status", "") == "not_user_agent":
            return Response(status_code=400)
        
        body = data.get("body")
        announce = data.get("announce")
        profile_title = data.get("profile_title")
        expire = data.get("expire", None)
        downlink = data.get("downlink", None)
        headers = await make_header_vpn_config(profile_title=profile_title, announce=announce, expire=expire, downlink=downlink)
        return Response(content=body, headers=headers, status_code=200)
    
    except Exception as e:
        return Response(status_code=500)