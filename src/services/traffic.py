from src.dao.traffic import TrafficDAO
from src.dao.configuration import ConfigurationDAO

from src.schemas.subscription import SPlanSubscription, SXrayClient, SXrayClients


class TrafficService:
    @staticmethod
    async def update_dowlink_traffic():
        config = await ConfigurationDAO.find_config()
        increment = config.increment
        await TrafficDAO.update_traffic_in_subscription_is_active(increment=increment)
