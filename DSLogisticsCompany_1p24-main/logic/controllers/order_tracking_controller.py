from google.cloud import bigquery
from fastapi import APIRouter
from logic.order_tracking import OrderTracking


class OrderTrackingController:
    """
    Controller class for Order Tracking functionality.
    """

    def __init__(self):
        """
        OrderTrackingController class constructor.
        """
        self.router = APIRouter(
            prefix="/orders",
            tags=["Order Tracking"]
        )
        self.order_tracking = OrderTracking(None)  # Initialize with None for order_id
        self.router.add_api_route(
            "/{order_id}/state",
            self.get_order_state,
            methods=["GET"]
        )
        self.router.add_api_route(
            "/{order_id}/state",
            self.update_order_state,
            methods=["PUT"]
        )
        self.client = bigquery.Client()

    async def get_order_state(self, order_id: str):
        """
        Retrieves the state of the order for a given order ID.

        :param order_id: Order ID.
        :type order_id: str
        :returns: Order state.
        :rtype: dict
        """
        self.order_tracking = OrderTracking(order_id)
        return {"orderState": await self.order_tracking.get_order_state(order_id)}
    
    async def get_order_info(self, order_id: str):
        query = f"SELECT order_id, product, order_state, delivery_date, destination_location FROM orders.order WHERE order_id = '{order_id}'"
        query_job = self.client.query(query)
        result = query_job.result()

        for row in result:
            order_info = {
                "order_id": row.order_id,
                "product": row.product,
                "order_state": row.order_state,
                "delivery_date": row.delivery_date.strftime("%Y-%m-%d"),
                "destination_location": row.destination_location
            }
            return order_info


    async def update_order_state(self, order_id: str, state: int):
        """
        Updates the state of the order for a given order ID.

        :param order_id: Order ID.
        :type order_id: str
        :param state: Order state.
        :type state: int
        :returns: Success message.
        :rtype: dict
        """
        self.order_tracking = OrderTracking(order_id)
        await self.order_tracking.update_order_state(order_id, state)
        return {"message": "Order state updated successfully"}
