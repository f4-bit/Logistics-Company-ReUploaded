from fastapi import APIRouter
from logic.routing import Routing


class RoutingController:
    """
    Controller class for Routing functionality.
    """

    def __init__(self):
        """
        RoutingController class constructor.
        """
        self.router = APIRouter(
            prefix="/orders",
            tags=["Routing"]
        )
        self.routing = Routing(None)  # Initialize with None for order_id
        self.router.add_api_route(
            "/{order_id}/destination",
            self.get_destination_location,
            methods=["GET"]
        )
        self.router.add_api_route(
            "/{order_id}/destination",
            self.update_destination_location,
            methods=["PUT"]
        )
    
    async def get_destination_location(self, order_id: str):
        """
        Retrieves the destination location for a given order ID.

        :param order_id: Order ID.
        :type order_id: str
        :returns: Destination location.
        :rtype: dict
        """
        self.routing = Routing(order_id)
        return {"destinationLocation": await self.routing.get_destination_location(order_id)}

    async def update_destination_location(self, order_id: str, new_destination: str):
        """
        Updates the destination location for a given order ID.

        :param order_id: Order ID.
        :type order_id: str
        :param location: Destination location.
        :type location: int
        :returns: Success message.
        :rtype: dict
        """
        await self.routing.update_destination_location(order_id, new_destination)
        return {"message": f"Destination location updated successfully to {new_destination}"}
