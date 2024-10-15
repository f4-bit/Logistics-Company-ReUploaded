from logic.microservice import Microservice
from google.cloud import bigquery


class OrderTracking(Microservice):
    """
    Class used to represent order tracking.
    """

    def __init__(self, order_id: int = None):
        """
        OrderTracking class constructor.

        :param order_id: An optional integer that identifies the order associated with this OrderTracking instance.
        :type order_id: int
        :returns: OrderTracking object
        :rtype: OrderTracking
        """
        self.order_id = order_id
        if self.order_id is None:
            self.microservice = Microservice(name="Order Tracking", orderId=0)
        else:
            self.microservice = Microservice(name="Order Tracking", orderId=self.order_id)
        self.order_state = 1  # 1 for "on its way", 0 for "delivered"
        self.client = bigquery.Client()
        

    async def get_order_state(self, order_id: str):
        """
        Returns the current state of the order.

        :returns: Order state (1 for "on its way", 0 for "delivered").
        :rtype: int
        """
        query = f"SELECT order_state FROM orders.order WHERE order_id = '{order_id}'"
        query_job = self.client.query(query)
        result = query_job.result()

        for row in result:
            self.order_state = row.order_state

        return self.order_state
    
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
        Sets the state of the order.

        :param state: Order state (1 for "on its way", 0 for "delivered").
        :type state: int
        """
        self.order_state = state
        query = f"UPDATE orders.order SET order_state = {self.order_state} WHERE order_id = '{order_id}'"
        query_job = self.client.query(query)
        query_job.result()

