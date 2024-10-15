from fastapi import APIRouter
from pydantic import BaseModel
from logic.cloud_data_warehouse import CloudDataWarehouse

class Order (BaseModel):
    product: str
    orderState: int
    destinationLocation: int

class Fleet (BaseModel):
    fleetPlates: str

class Query(BaseModel):
    sql_query: str

class Insertion(BaseModel):
    table_id: str
    rows_to_insert: list

class CloudDataWarehouseController:
    """
    Controller class for Cloud Data Warehouse functionality.
    """

    def __init__(self):
        """
        CloudDataWarehouseController class constructor.
        """
        self.router = APIRouter(
            prefix="/warehouse",
            tags=["Cloud Data Warehouse"]
        )
        self.warehouse = CloudDataWarehouse()
        self.router.add_api_route(
            "/query",
            self.run_query,
            methods=["POST"]
        )
        self.router.add_api_route(
            "/insert_data",
            self.insert_data,
            methods=["POST"]
        )
        self.router.add_api_route(
            "/orders/",
            self.create_order,
            methods=["POST"]
        )
        self.router.add_api_route(
            "/fleets/",
            self.create_fleet,
            methods=["POST"]
        )

    async def run_query(self, query: Query):
        """
        Runs a SQL query in BigQuery.

        :param query: SQL query.
        :type query: Query
        :returns: Query result.
        :rtype: dict
        """
        result = self.warehouse.query(query.sql_query)
        return {"result": [dict(row) for row in result]}

    async def insert_data(self, insertion: Insertion):
        """
        Inserts data into a BigQuery table.

        :param insertion: Table ID and data to insert.
        :type insertion: Insertion
        :returns: Insertion status.
        :rtype: dict
        """
        self.warehouse.insert_data(insertion.table_id, insertion.rows_to_insert)
        return {"message": "Data inserted."}

    async def create_order(self, product: str, destination: str):
        """
        Creates an order in BigQuery.

        :param order: Order details.
        :type order: Order
        :returns: Order status.
        :rtype: dict
        """
        return {"order": await self.warehouse.create_order(product, destination)}

    async def create_fleet(self, fleetPlates: str):
        """
        Creates a fleet in BigQuery.

        :param fleetPlates: Fleet plates.
        :type fleetPlates: str
        :returns: Fleet status.
        :rtype: dict
        """
        return {"fleet": await self.warehouse.create_fleet(fleetPlates)}

