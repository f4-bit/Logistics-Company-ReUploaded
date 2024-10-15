from logic.microservice import Microservice
from google.cloud import bigquery
from datetime import date


class Scheduling(Microservice):
    """
    Class used to represent scheduling functionality.
    """

    def __init__(self, order_id: int = None):
        """
        Scheduling class constructor.

        :param order_id: An optional integer that identifies the order associated with this Scheduling instance.
        :type order_id: int
        :returns: Scheduling object
        :rtype: Scheduling
        """
        self.order_id = order_id
        if self.order_id is None:
            self.microservice = Microservice(name="Scheduling", orderId=0)
        else:
            self.microservice = Microservice(name="Scheduling", orderId=self.order_id)
        self.delivery_date = None
        self.client = bigquery.Client()

    async def get_delivery_date(self, order_id: str):
        """
        Returns the delivery date.

        :returns: Delivery date.
        :rtype: str
        """
        query = f"SELECT delivery_date FROM orders.order WHERE order_id = '{order_id}'"
        query_job = self.client.query(query)
        result = query_job.result()

        for row in result:
            self.delivery_date = row.delivery_date

        return self.delivery_date

    async def update_delivery_date(self, order_id: str, delivery_date: date):
        """
        Sets the delivery date.

        :param order_id: Order id.
        :type order_id: str
        :param delivery_date: Delivery date.
        :type delivery_date: date
        """
        self.delivery_date = delivery_date
        query = f"""
        UPDATE orders.order
        SET delivery_date = '{self.delivery_date}'
        WHERE order_id = '{order_id}'
        """
        query_job = self.client.query(query)
        query_job.result()

