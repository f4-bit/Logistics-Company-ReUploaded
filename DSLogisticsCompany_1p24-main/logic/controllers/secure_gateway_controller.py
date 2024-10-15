from fastapi import APIRouter
from logic.secure_gateway import SecureGateway, RequestData

class SecureGatewayController:
    """
    Controller class for SecureGateway functionality.
    """

    def __init__(self):
        """
        SecureGatewayController class constructor.
        """
        self.router = APIRouter(
            prefix="/api",
            tags=["SecureGateway"]
        )
        self.gateway = SecureGateway()
        self.router.add_api_route(
            "/",
            self.handle_request,
            methods=["POST"]
        )

    async def handle_request(self, serviceType: str, operation:str, **kwargs):
        """
        Handles the request for a given RequestData.

        :param request_data: RequestData.
        :type request_data: RequestData
        :returns: Result of the request.
        :rtype: dict
        """

        return await self.handle_request(serviceType, operation, **kwargs)
