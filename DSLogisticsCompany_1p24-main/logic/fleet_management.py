from logic.microservice import Microservice
from google.cloud import bigquery


class FleetManagement(Microservice):
    """
    Class used to represent fleet management.
    """
    
    def __init__(self, order_id: int = None):
        """
        FleetManagement class constructor.

        :param order_id: An optional integer that identifies the order associated with this FleetManagement instance.
        :type order_id: int
        :returns: FleetManagement object
        :rtype: FleetManagement
        """
        self.order_id = order_id
        if self.order_id is None:
            self.microservice = Microservice(name="Fleet Management", orderId=0)
        else:
            self.microservice = Microservice(name="Fleet Management", orderId=self.order_id)
        self.fleet_responsible = None
        self.vehicle_plates = []
        self.client = bigquery.Client()

    async def get_fleet_responsible(self, order_id: str):
        """
        Returns the fleet responsible.

        :returns: Fleet responsible.
        :rtype: str
        """
        query = f"""
        SELECT fleet_id
        FROM `orders.fleet_assignments`
        WHERE order_id = '{order_id}'
        """
        query_job = self.client.query(query)
        result = query_job.result()

        for row in result:
            return row.fleet_id

        return None

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

    async def update_fleet_responsible(self, order_id:str, new_fleet: str):
        """
        Sets the fleet responsible.

        :param responsible: Fleet responsible.
        :type responsible: str
        """
        self.fleet_responsible = new_fleet
        query = f"""
        UPDATE `orders.fleet_assignments`
        SET fleet_id = '{self.fleet_responsible}'
        WHERE order_id = '{order_id}'
        """
        query_job = self.client.query(query)
        query_job.result()

    async def get_vehicle_plates(self, fleet_id: str):
        """
        Returns a list of vehicle plates in the fleet.

        :returns: List of vehicle plates.
        :rtype: list
        """
        query = f"""
        SELECT fleetplates 
        FROM `orders.fleets` 
        WHERE fleet_id = '{fleet_id}'
        """
        query_job = self.client.query(query)
        result = query_job.result()

        self.vehicle_plates = [row.fleetplates for row in result]

        return self.vehicle_plates
