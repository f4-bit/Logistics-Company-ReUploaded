import datetime
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict
from .controllers.order_tracking_controller import OrderTrackingController
from .controllers.scheduling_controller import SchedulingController
from .controllers.routing_controller import RoutingController
from .controllers.fleet_management_controller import FleetManagementController
from .models.request_data import RequestData
from .models.response_data import ResponseData
from datetime import datetime

class SecureGateway:
    def __init__(self):
        # Log for auditory
        self.audit_log: list[Dict] = []

        # Initialize controllers
        self.controllers = {
            "fleet_management": FleetManagementController(),
            "order_tracking": OrderTrackingController(),
            "scheduling": SchedulingController(),
            "routing": RoutingController(),
        }

    # Method to handle requests
    async def handle_request(self, service_type: str, operation: str, **kwargs):
        # Register request in audit_log
        self.audit_log.append({"service_type": service_type, "operation": operation, "timestamp": datetime.now()})

        # Get the appropriate controller
        controller = self.controllers.get(service_type)
        if controller is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        # Get the appropriate method
        method = getattr(controller, operation, None)
        if method is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        # Call the method and return its result
        return await method(**kwargs)



