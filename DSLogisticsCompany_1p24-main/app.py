from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from logic.controllers.cloud_data_warehouse_controller import CloudDataWarehouseController
from logic.controllers.secure_gateway_controller import SecureGatewayController
from logic.controllers.order_tracking_controller import OrderTrackingController
from logic.controllers.fleet_management_controller import FleetManagementController
from logic.controllers.routing_controller import RoutingController

app = FastAPI()
app.mount("/static", StaticFiles(directory="assets"), name="static")
templates = Jinja2Templates(directory="templates")


"""
Middleware configuration for handling CORS.

:param origins: List of allowed origins for CORS requests.
:type origins: list
"""
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cloud_data_warehouse_controller = CloudDataWarehouseController()
app.include_router(cloud_data_warehouse_controller.router)

secure_gateway_controller = SecureGatewayController()
app.include_router(secure_gateway_controller.router)

order_tracking_controller = OrderTrackingController()
app.include_router(order_tracking_controller.router)

fleet_management_controller = FleetManagementController()
app.include_router(fleet_management_controller.router)

routing_controller = RoutingController()
app.include_router(routing_controller.router)

# app.py initial methods

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """
    Renders the index page.

    :param request: Request object.
    :type request: Request
    :returns: Rendered index page.
    :rtype: HTMLResponse
    """
    print('Request for index page received')
    return templates.TemplateResponse('index.html', {"request": request})

@app.get("/services", response_class=HTMLResponse)
def services(request: Request):
    """
    Renders the services page.

    :param request: Request object.
    :type request: Request
    :returns: Rendered services page.
    :rtype: HTMLResponse
    """
    return templates.TemplateResponse('services.html', {"request": request})

@app.get("/tracking_orders", response_class=HTMLResponse)

def tracking_orders(request: Request):
    """
    Renders the tracking_orders page.

    :param request: Request object.
    :type request: Request
    :returns: Rendered tracking_orders page.
    :rtype: HTMLResponse
    """
    return templates.TemplateResponse('tracking_orders.html', {"request": request})

@app.post("/api/track-order/{order_id}")
async def track_order(order_id: str):
    order_tracking = OrderTrackingController()
    order_info = await order_tracking.get_order_info(order_id)
    return order_info

@app.get("/fleet_management", response_class=HTMLResponse)
def fleet_management(request: Request):
    """
    Renders the fleet_managament page.

    :param request: Request object.
    :type request: Request
    :returns: Rendered fleet_managament page.
    :rtype: HTMLResponse
    """
    return templates.TemplateResponse('fleet_management.html', {"request": request})

@app.post("/api/fleet-management/{fleet_id}")
async def fleet_management(fleet_id: str):
    fleet_management = FleetManagementController()
    fleet_info = await fleet_management.get_fleet_info(fleet_id)
    return fleet_info

@app.put("/api/orders/{order_id}/destination")
async def update_destination_location(order_id: str, new_destination: str):
    routing = RoutingController()
    old_destination = await routing.get_destination_location(order_id)
    await routing.update_destination_location(order_id, new_destination)
    return {"message": f"Destination location updated successfully to {new_destination}"}

@app.get("/route_programming", response_class=HTMLResponse)
def about(request: Request):
    """
    Renders the route_programming page.

    :param request: Request object.
    :type request: Request
    :returns: Rendered route_programming page.
    :rtype: HTMLResponse
    """
    return templates.TemplateResponse('route_programming.html', {"request": request})

@app.get("/about", response_class=HTMLResponse)
def about(request: Request):
    """
    Renders the about page.

    :param request: Request object.
    :type request: Request
    :returns: Rendered about page.
    :rtype: HTMLResponse
    """
    return templates.TemplateResponse('about.html', {"request": request})


if __name__ == "__main__":
    """
    Entry point of the application.
    Runs the Uvicorn server on 127.0.0.1:8000.
    """
    uvicorn.run('app:app', host="127.0.0.1", port=8000, timeout_keep_alive=100)