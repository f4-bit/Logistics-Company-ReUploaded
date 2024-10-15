from google.cloud import bigquery
from fastapi import APIRouter
from logic.fleet_management import FleetManagement


class FleetManagementController:
    """
    Controller class for Fleet Management functionality.
    """

    def __init__(self):
        """
        FleetManagementController class constructor.
        """
        self.router = APIRouter(
            prefix="/fleet",
            tags=["Fleet Management"]
        )
        self.fleet_management = FleetManagement(None)  # Initialize with None for order_id
        self.router.add_api_route(
            "/orders/{order_id}/fleetResponsible",
            self.get_fleet_responsible,
            methods=["GET"]
        )
        self.router.add_api_route(
            "/orders/{order_id}/fleetResponsible",
            self.update_fleet_responsible,
            methods=["PUT"]
        )
        self.router.add_api_route(
            "/vehiclePlates",
            self.get_vehicle_plates,
            methods=["GET"]
        )
        self.client = bigquery.Client()

    async def get_fleet_responsible(self, order_id: str):
        """
        Retrieves the fleet responsible for a given order ID.

        :param order_id: Order ID.
        :type order_id: str
        :returns: Fleet responsible.
        :rtype: dict
        """
        self.fleet_management = FleetManagement(order_id)
        return {"fleetResponsible": await self.fleet_management.get_fleet_responsible(order_id)}
    
    async def get_fleet_info(self, fleet_id: str):
        query = f"SELECT fleet_id, fleetplates FROM orders.fleets WHERE fleet_id = '{fleet_id}'"
        query_job = self.client.query(query)
        result = query_job.result()

        for row in result:
            fleet_info = {
                "fleet_id": row.fleet_id,
                "fleetplates": row.fleetplates
            }
            return fleet_info


    async def update_fleet_responsible(self, order_id: str, new_fleet: str):
        """
        Updates the fleet responsible for a given order ID.

        :param order_id: Order ID.
        :type order_id: str
        :param responsible: Fleet responsible.
        :type responsible: str
        :returns: Success message.
        :rtype: dict
        """
        self.fleet_management = FleetManagement(order_id)
        await self.fleet_management.update_fleet_responsible(order_id, new_fleet)
        return {"message": "Fleet responsible updated successfully"}

    async def get_vehicle_plates(self, fleet_id: str):
        """
        Retrieves the list of vehicle plates.

        :returns: List of vehicle plates.
        :rtype: dict
        """
        return {"vehiclePlates": await self.fleet_management.get_vehicle_plates(fleet_id)}