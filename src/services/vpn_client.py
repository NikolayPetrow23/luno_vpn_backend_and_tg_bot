import asyncio
import json
import httpx

from src.schemas.subscription import SXrayClients
from src.config import settings
from src.broker.nats import nats


class VpnServerClient:
    token = settings.config.API_TOKEN_SERVER
    port = settings.config.PORT_API_SERVER

    @classmethod
    async def add_user_to_all_servers(cls, servers: list, uuid: str, email: str):
        tasks = [cls._request_add_user_to_server(domain=server, uuid=uuid, email=email) for server in servers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for srv, result in zip(servers, results):
            if isinstance(result, Exception):
                print(f"{srv} — не удалось добавить: {result}")
            else:
                print(f"{srv} — пользователь добавлен")

    @classmethod
    async def remove_user_to_all_servers(cls, servers: list, uuid: str, email: str):
        tasks = [cls._request_delete_user_to_server(domain=server, uuid=uuid, email=email) for server in servers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for srv, result in zip(servers, results):
            if isinstance(result, Exception):
                print(f"{srv} — не удалось удалить: {result}")
            else:
                print(f"{srv} — пользователь удален")

    @classmethod
    async def add_users_to_all_servers(cls, servers: list, data: SXrayClients):
        data = data.model_dump()
        tasks = [cls._request_add_users_to_server(domain=server, data=data) for server in servers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for srv, result in zip(servers, results):
            if isinstance(result, Exception):
                print(f"{srv} — не удалось обновить все активные подписки: {result}")
            else:
                print(f"{srv} — подписки обновлены")

    @classmethod
    async def check_servers(cls, servers: list):
        tasks = [cls._request_check_server(domain=server) for server in servers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for srv, result in zip(servers, results):
            if isinstance(result, Exception):
                print(f"Ошибка при проверке сервера {srv}: {result}")
                payload = {
                    "type": "server.status.error",
                    "status": "error",
                    "server": srv,
                    "error":  result
                }
                await nats.publish("bot.admin.notifications", json.dumps(payload).encode())
            else:
                print(f"Проверка сервера {srv} успешна: {result}")
                payload = {
                    "type": "server.status.ok",
                    "status": "ok",
                    "result": result,
                }
                await nats.publish("bot.admin.notifications", json.dumps(payload).encode())

    @classmethod
    async def _request_add_user_to_server(cls, domain: str, uuid: str, email: str):
        headers = {"Authorization": f"Bearer {cls.token}"}
        data = {"id": uuid, "email": email}
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"https://{domain}:{cls.port}/api/user/add", json=data, headers=headers)
            resp.raise_for_status()
            return resp.json()
    
    @classmethod
    async def _request_delete_user_to_server(cls, domain: str, uuid: str, email: str):
        headers = {
            "Authorization": f"Bearer {cls.token}",
            "Content-Type": "application/json"
        }
        data = {"id": uuid, "email": email}
        async with httpx.AsyncClient() as client:
            resp = await client.request(
                "DELETE",
                f"https://{domain}:{cls.port}/api/user/remove",
                content=json.dumps(data),
                headers=headers
            )
            resp.raise_for_status()
            return resp.json()
    
    @classmethod
    async def _request_add_users_to_server(cls, domain: str, data: dict):
        headers = {"Authorization": f"Bearer {cls.token}"}
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"https://{domain}:{cls.port}/api/users/add", json=data, headers=headers)
            resp.raise_for_status()
            return resp.json()

    @classmethod
    async def _request_check_server(cls, domain: str):
        headers = {"Authorization": f"Bearer {cls.token}"}
        async with httpx.AsyncClient(timeout=25.0) as client:
            resp = await client.get(f"https://{domain}:{cls.port}/api/check/status", headers=headers)
            resp.raise_for_status()
            return resp.json()

