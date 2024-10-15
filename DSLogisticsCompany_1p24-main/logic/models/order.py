from pydantic import BaseModel

class Order (BaseModel):
    product: str
    orderState: int
    destinationLocation: int
