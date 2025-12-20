import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from src.models import Server
from src.schemas.subscription import SXrayClients
from src.services.subscribtion import SubscriptionService
from src.services.traffic import TrafficService
from src.dao.server import ServerDAO
from src.services.vpn_client import VpnServerClient

logger = logging.getLogger(__name__)


async def sync_all_sub():
    servers: Server = await ServerDAO.find_servers_is_active_in_domain()
    data: SXrayClients = await SubscriptionService.check_expired_subscriptions()
    await VpnServerClient.add_users_to_all_servers(servers, data)


async def sync_revision_hourly():
    servers: Server = await ServerDAO.find_servers_is_active_in_domain()
    data: SXrayClients = await SubscriptionService.subsribtion_is_active_all()
    await VpnServerClient.add_users_to_all_servers(servers, data)


async def update_downlink_traffic():
    await TrafficService.update_dowlink_traffic()


async def test_servers():
    servers: Server = await ServerDAO.find_servers_is_active_in_domain()
    await VpnServerClient.check_servers(servers)


def start_scheduler() -> AsyncIOScheduler:
    """Инициализация планировщика"""
    scheduler = AsyncIOScheduler(timezone="UTC")

    # Глобальная синхронизация раз в 8 часов, а также проверка активных подписок
    # scheduler.add_job(sync_all_sub, CronTrigger(hour=15, minute=0))
    # Нужно делать раз в 24 часа иначе постоянно будут приходить уведомления!
    scheduler.add_job(sync_all_sub, IntervalTrigger(hours=24))
    
    # Проверка раз в 35 минут, обновление активного списка подписок и отправка на VPN серверы 
    scheduler.add_job(sync_revision_hourly, IntervalTrigger(minutes=35))

    # Увеличение трафика (пока заглушка!)
    scheduler.add_job(update_downlink_traffic, IntervalTrigger(hours=2))

    # Тест серверов
    scheduler.add_job(test_servers, IntervalTrigger(minutes=27))

    scheduler.start()
    
    return scheduler
