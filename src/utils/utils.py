import base64
from datetime import datetime, timezone
import secrets
import string

from src.config import settings


def utc_now_no_microseconds():
    return datetime.now(timezone.utc).replace(microsecond=0).replace(tzinfo=None)


def generate_short_code(length: int = 16) -> str:
    """Генерация короткого кода типа qWJZPJ3Qr0vedo5z"""
    alphabet = string.ascii_letters + string.digits  # A-Z + a-z + 0-9
    return ''.join(secrets.choice(alphabet) for _ in range(length))


async def make_header_vpn_config(profile_title: str, announce: str, expire: datetime = None, downlink: str = None) -> dict:
    profile_title_b64 = base64.b64encode(profile_title.encode()).decode()
    announce_b64 = base64.b64encode(announce.encode()).decode()
    headers = {
        "content-type": "application/json",
        "content-disposition": 'attachment; filename="lunovpn"',
        "profile-web-page-url": f"https://{settings.config.URL_DOMAIN}",
        "support-url": "https://t.me/myvpn_support",
        "profile-title": f"base64:{profile_title_b64}",
        "profile-update-interval": "1",
        "subscription-userinfo": f"upload=0; download={0 if downlink is None else downlink}; total=0; expire={0 if expire is None else expire.timestamp()}",
        "announce": f"base64:{announce_b64}",
    }
    return headers


async def make_vless_config_server(
        uuid: str, domain: str, 
        port: int, pbk: str, sid: str, 
        location: str, emoji: str
    ):
    vless_config = f"vless://{uuid}@{domain}:{port}?&encryption=none&security=reality&pbk={pbk}&fp=chrome&type=tcp&flow=xtls-rprx-vision&sni={domain}&sid={sid}&#{location}{emoji}"
    
    return vless_config