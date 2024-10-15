from fastapi import APIRouter
from logic.scheduling import Scheduling
from datetime import date

class SchedulingController:
    """
    Controller class for Scheduling functionality.
    """

    def __init__(self):
        """
        SchedulingController class constructor.
        """
        self.router = APIRouter(
            prefix="/orders",
            tags=["Scheduling"]
        )
        self.scheduling = Scheduling(None)  # Initialize with None for order_id
        self.router.add_api_route(
            "/{order_id}/deliveryDate",
            self.get_delivery_date,
            methods=["GET"]
        )
        self.router.add_api_route(
            "/{order_id}/deliveryDate",
            self.update_delivery_date,
            methods=["PUT"]
        )

    async def get_delivery_date(self, order_id: str):
        """
        Retrieves the delivery date for a given order ID.

        :param order_id: Order ID.
        :type order_id: str
        :returns: Delivery date.
        :rtype: dict
        """
        self.scheduling = Scheduling(order_id)
        return {"deliveryDate": await self.scheduling.get_delivery_date(order_id)}

    async def update_delivery_date(self, order_id: str, date: date):
        """
        Updates the delivery date for a given order ID.

        :param order_id: Order ID.
        :type order_id: str
        :param date: Delivery date.
        :type date: str
        :returns: Success message.
        :rtype: dict
        """
        self.scheduling = Scheduling(order_id)
        await self.scheduling.update_delivery_date(order_id, date)
        return {"message": "Delivery date updated successfully"}

