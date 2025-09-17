class ProtonXError(Exception):
    pass

class APIError(ProtonXError):
    def __init__(self, status: int, body: str):
        super().__init__(f"APIError {status}: {body}")
        self.status = status
        self.body = body

class AuthError(ProtonXError):
    pass
