from google.cloud import bigquery
from datetime import date, timedelta
from pydantic import BaseModel
import random

class Order(BaseModel):
    order_id: str
    product: str 
    order_state: int
    delivery_date: date
    destination_location: str
    
class Fleet (BaseModel):
    fleetplates: str
    
class Assignment (BaseModel):
    assignment_id: str
    fleet_id: str
    order_id: str

class CloudDataWarehouse:
    def __init__(self):
        print("BigQuery started")
        self.client = bigquery.Client()

    def test_connection(self):
        print("The connection began to be made")
        try:
            self.client.list_datasets()  
            print("Successful connection to BigQuery.")
        except Exception as e:
            print("The connection to BigQuery failed.")
            print("Error:", e)

    def query(self, sql_query):
        query_job = self.client.query(sql_query)
        return query_job.result()

    def insert_data(self, table_id, rows_to_insert):
        table = self.client.get_table(table_id)
        errors = self.client.insert_rows(table, rows_to_insert)
        if errors == []:
            print("New rows have been added.")
        else:
            print("Errors were found when inserting rows: {}".format(errors))
            
    async def create_order(self, product: str, destinationLocation: str):
        # A random id is generated
        id = random.randint(1, 10**10)

        # Verificamos si el id ya existe en la base de datos
        result = self.query(f"SELECT order_id FROM orders.order WHERE order_id = '{id}'")
        while len(list(result)) > 0:
            id = random.randint(1, 10**10)
            result = self.query(f"SELECT order_id FROM orders.order WHERE order_id = '{id}'")

        # Establecemos la fecha de entrega para 2 días después de la fecha actual
        delivery_date = date.today() + timedelta(days=2)

        orderState = 1

        rows_to_insert = [
            {"order_id": str(id), "product": product, "order_state": orderState, "delivery_date": delivery_date, 
            "destination_location": destinationLocation}
        ]
        
        self.insert_data("orders.order", rows_to_insert)
        
        # Asignamos una flota a la orden recién creada
        assignment = await self.assign_fleet_to_order(str(id))
        
        return {"order": Order(order_id=str(id), product=product, order_state=orderState, delivery_date=delivery_date, destination_location=destinationLocation)}


        
    async def create_fleet(self, fleetplates: str):
        # Generamos un id aleatorio de entre 1 y 10 dígitos
        id = random.randint(1, 10**10)

        # Verificamos si el id ya existe en la base de datos
        result = self.query(f"SELECT fleet_id FROM orders.fleets WHERE fleet_id = '{id}'")
        while len(list(result)) > 0:
            id = random.randint(1, 10**10)
            result = self.query(f"SELECT fleet_id FROM orders.fleets WHERE fleet_id = '{id}'")

        rows_to_insert = [
            {"fleet_id": str(id), "fleetplates": fleetplates}
        ]
        self.insert_data("orders.fleets", rows_to_insert)
        return {"fleet": Fleet(id=str(id), fleetplates=fleetplates)}

    async def assign_fleet_to_order(self, order_id: str):
        # Buscamos el primer fleet_id disponible
        result = self.query("SELECT fleet_id FROM orders.fleets WHERE fleet_id NOT IN (SELECT fleet_id FROM orders.fleet_assignments) LIMIT 1")
        result_list = list(result)
        if len(result_list) == 0:
            raise Exception("There are no fleets available. Please, come back later")
        fleet_id = result_list[0]["fleet_id"]

        # Generamos un id aleatorio para la asignación
        assignment_id = random.randint(1, 10**10)
        result = self.query(f"SELECT assignment_id FROM orders.fleet_assignments WHERE assignment_id = '{assignment_id}'")
        while len(list(result)) > 0:
            assignment_id = random.randint(1, 10**10)
            result = self.query(f"SELECT assignment_id FROM orders.fleet_assignments WHERE assignment_id = '{assignment_id}'")

        rows_to_insert = [
            {"assignment_id": str(assignment_id), "fleet_id": fleet_id, "order_id": order_id}
        ]
        
        self.insert_data("orders.fleet_assignments", rows_to_insert)
        return {"assignment": Assignment(assignment_id=str(assignment_id), fleet_id=fleet_id, order_id=order_id)}

