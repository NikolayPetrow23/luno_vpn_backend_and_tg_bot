from datetime import datetime
import json

from src.dao import ShortLinkDAO, SubscriptionDAO, DeviceDAO, PlanSubscriptionDAO, TrafficDAO, UserDAO
from src.models import Server, Subscription, ShortLink, Traffic, User
from src.utils.utils import make_vless_config_server, utc_now_no_microseconds
from src.broker.nats import nats

class VPNService:
    @classmethod
    async def get_config_vpn(
        cls, code: str, user_agent: str,
        x_hwid: str, device_model: str
    ) -> dict:
        if user_agent not in ("Happ", "v2ra"):
            return await cls._not_user_agent()

        short_link: ShortLink | None = await ShortLinkDAO.find_one_or_none(code=code)

        if short_link is None:
            return {"status": "not_short_link"}

        sub_join_plan: Subscription = await SubscriptionDAO.find_subscription_joinload_in_plan(
            subscription_id=short_link.subscription_id
        )
        user: User = await UserDAO.find_by_id(sub_join_plan.user_id)

        if sub_join_plan is None or sub_join_plan.is_active != True:
            return await cls._expired_subscription_response(
                expire=sub_join_plan.end_date
            )

        count_devices: int | None = await DeviceDAO.find_count_devices_in_sub_or_none(
            subscription_id=sub_join_plan.id
        )
        hwid: str | None = await DeviceDAO.find_one_or_none(
            identifier_value=x_hwid, 
            subscription_id=sub_join_plan.id
        )

        if hwid is None:
            if sub_join_plan.plan.count_devices > count_devices:
                identifier_type_id = 1 if user_agent == "Happ" else 2
                now = utc_now_no_microseconds()
                await DeviceDAO.add_data(
                    subscription_id=sub_join_plan.id,
                    identifier_type_id=identifier_type_id,
                    identifier_value=x_hwid,
                    device_model=device_model,
                    last_connected=now
                )
                payload = {
                    "type": "client.new.device",
                    "status": "new_device",
                    "user_id": user.telegram_id,
                    "device_model": device_model,
                    "identifier_value": x_hwid,
                    "count_devices": count_devices + 1,
                    "max_devices": sub_join_plan.plan.count_devices
                }
                await nats.publish("bot.client.notifications", json.dumps(payload).encode())
            else:
                payload = {
                    "type": "client.max.devices",
                    "status": "max_device",
                    "user_id": user.telegram_id,
                    "count_devices": count_devices,
                    "max_devices": sub_join_plan.plan.count_devices
                }
                await nats.publish("bot.client.notifications", json.dumps(payload).encode())
                return await cls._max_devices_response(expire=sub_join_plan.end_date)
            
        return await cls._build_config_response(
            expire=sub_join_plan.end_date,
            subscription_id=sub_join_plan.id,
            uuid=sub_join_plan.uuid, 
            plan_id=sub_join_plan.plan.id
        )

    @classmethod
    async def _build_config_response(
        cls, expire: datetime, subscription_id: int, 
        uuid: str, plan_id: int
    ) -> dict:
        servers: list[Server] = await PlanSubscriptionDAO.find_all_servers_in_plan(
            plan_id=plan_id
        )
        traffic: Traffic | None = await TrafficDAO.find_one_or_none(
            subscription_id=subscription_id
        )
        if traffic is None:
            traffic: Traffic | None = await TrafficDAO.add_data(
                subscription_id=subscription_id,
                downlink=23
            )
        configs = []
        for server in servers:
            config = await make_vless_config_server(
                uuid=uuid,
                domain=server.domain,
                port=server.port,
                pbk=server.pbk,
                sid=server.sid,
                location=server.location,
                emoji=server.emoji
            )
            configs.append(config)

        body = "\n".join(configs)
        profile_title = "Luno VPN @lunovpn_bot"
        announce = "Luno VPN дешевый и надежный vpn"
        return {
            "status": "success",
            "expire": expire,  
            "downlink": traffic.downlink,
            "body": body,
            "profile_title": profile_title,
            "announce": announce,          
        }

    @classmethod
    async def _expired_subscription_response(cls, expire: datetime) -> dict:
        body = "\n".join(["vless://123456@123456:123#Ваша подписка кончилась, купите через @lunovpn_bot"])
        profile_title = "Luno VPN @lunovpn_bot"
        announce = "Ваша подписка кончилась, для продления войдите в нашего бота и выберите нужный тариф!"
        return {
            "status": "expire_subscription",
            "body": body,
            "profile_title": profile_title,
            "announce": announce,
            "expire": expire
        }

    @classmethod
    async def _max_devices_response(cls, expire: datetime) -> dict:
        body = "\n".join(["vless://123456@123456:123#Увеличьте количество устройств!"])
        profile_title = "LunoVPN @lunovpn_bot"
        announce = "У вас добавлено максимальное количество устройств, увеличьте количество устройств в подписке!"
        return {
            "status": "max_devices",
            "body": body,
            "profile_title": profile_title,
            "announce": announce
        }
    
    @classmethod
    async def _not_user_agent(cls)  -> dict:
        body = "\n".join(["vless://123456@123456:123#Скачайте приложение Happ или V2RayTun!"])
        profile_title = "Luno VPN @lunovpn_bot работает только через приложение Happ или V2RayTun, ссылку на скачивание можно найти в инструкции нашего телеграм бота!"
        return {
            "status": "not_user_agent",
            "body": body,
            "announce": profile_title,
            "profile_title": profile_title,
        }
