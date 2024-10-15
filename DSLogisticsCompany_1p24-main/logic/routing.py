from logic.microservice import Microservice
from google.cloud import bigquery


class Routing(Microservice):
    """
    Class used to represent routing functionality.
    """

    def __init__(self, order_id: int = None):
        """
        Routing class constructor.

        :param order_id: An optional integer that identifies the order associated with this Routing instance.
        :type order_id: int
        :returns: Routing object
        :rtype: Routing
        """
        self.order_id = order_id
        if self.order_id is None:
            self.microservice = Microservice(name="Routing", orderId=0)
        else:
            self.microservice = Microservice(name="Routing", orderId=self.order_id)
        self.destination_location = None
        self.origin_location = None
        self.client = bigquery.Client()

    async def get_destination_location(self, order_id: str):
        """
        Returns the destination location.

        :returns: Destination location.
        :rtype: str
        """
        query = f"SELECT destination_location FROM orders.order WHERE order_id = '{order_id}'"
        query_job = self.client.query(query)
        result = query_job.result()

        for row in result:
            self.destination_location = row.destination_location

        return self.destination_location

    async def update_destination_location(self, order_id: str, new_destination: str):
        """
        Sets the destination location.

        :param location: Destination location.
        :type location: str
        """
        query = f"""
        UPDATE orders.order
        SET destination_location = '{new_destination}'
        WHERE order_id = '{order_id}'
        """
        query_job = self.client.query(query)
        query_job.result()
        return new_destination

