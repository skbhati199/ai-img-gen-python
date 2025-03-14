class AIImageGeneratorError(Exception):
    """Base exception for AI Image Generator SDK."""
    pass


class APIError(AIImageGeneratorError):
    """Exception raised when the API returns an error."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error ({status_code}): {message}")


class ValidationError(AIImageGeneratorError):
    """Exception raised when input validation fails."""
    pass


class AuthenticationError(AIImageGeneratorError):
    """Exception raised when authentication fails."""
    pass


class RateLimitError(APIError):
    """Exception raised when rate limit is exceeded."""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(429, message)