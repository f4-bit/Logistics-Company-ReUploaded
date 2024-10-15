class Microservice:
    """
    Class representing a microservice.
    """

    def __init__(self, name, orderId):
        """
        Microservice class constructor.

        :param name: Name of the microservice.
        :type name: str
        :param orderId: ID of the order associated with the microservice.
        :type orderId: int
        """
        self.name = name
        self.orderId = orderId

