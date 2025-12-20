import json

from src.broker.admin import push_exception_admin
from src.broker.nats import nats
from src.schemas.user import SUser
from src.services.subscribtion import RefferalService
from src.services.user import UserService
from src.dao import UserDAO, ServerDAO
from src.services.vpn_client import VpnServerClient
from src.models import Server
from src.schemas.subscription import SXrayClients
from src.services.subscribtion import SubscriptionService



async def cb(msg):
    data = json.loads(msg.data.decode())

    if data["type"] == "app.client.reffer.start":
        try:
            user_data: SUser = SUser(
                telegram_id=str(data["user_telegram_id"]),
                username=data["user_username"],
                first_name=data["user_username"]
            )
        except Exception as e:
            await push_exception_admin(
                user_id=None,
                exception=e,
                path="cb - app.client.reffer.start",
                raise_exc=f"Ошибка при создании SUser из данных NATS сообщения"
            )
            raise
        try:
            await RefferalService.process_refferal(
                user_data=user_data,
                ref_code=data["ref_code"]
            )
        except Exception as e:
            raise
    
    elif data["type"] == "app.clients.get.not_is_active":
        users: list = await UserDAO.find_not_is_active_users_in_telegram_id()
        paylaod = {
            "type": "request.clients.not_is_active",
            "users": users
        }
        await nats.publish("bot.request.clients", json.dumps(paylaod).encode())

    elif data["type"] == "app.clients.get.all":
        users: list = await UserDAO.find_all_users_in_telegram_id()
        paylaod = {
            "type": "request.clients.all",
            "users": users
        }
        await nats.publish("bot.request.clients", json.dumps(paylaod).encode())

    elif data["type"] == "app.client.create":
        try:
            user_data: SUser = SUser(
                telegram_id=data["user_telegram_id"],
                username=data["user_username"],
                first_name=data["first_name"]
            )
            await UserService.crate_user(
                user_data=user_data
            )
        except Exception as e:
            await push_exception_admin(
                user_id=None,
                exception=e,
                path="cb - app.client.create",
                raise_exc=f"Ошибка при создании пользователя из данных NATS сообщения"
            )
            raise  
    
    elif data["type"] == "app.servers.update.config":
        try:
            servers: Server = await ServerDAO.find_servers_is_active_in_domain()
            data: SXrayClients = await SubscriptionService.subsribtion_is_active_all()
            await VpnServerClient.add_users_to_all_servers(servers, data)   
            print("✅ Конфиги на серверах успешно обновлены по запросу из бота!")
        except Exception as e:
            await push_exception_admin(
                user_id=None,
                exception=e,
                path="cb - app.servers.update.config",
                raise_exc=f"Ошибка при обновлении конфигурации серверов из данных NATS сообщения"
            )
            raise
