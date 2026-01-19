class NoResultFoundException(Exception):
    """Exception raised when no result is found in the database."""

    def __init__(self, message: str = "No result found"):
        self.message = message
        self.status_code = 404
        super().__init__(self.message)


class DatabaseException(Exception):
    """Exception raised for database errors."""

    def __init__(self, message: str = "Database connection error"):
        self.message = message
        super().__init__(self.message)
