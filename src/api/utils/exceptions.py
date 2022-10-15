
class RateLimited(Exception):
    """An Exception raised when the API is rate limited."""

    def __init__(self, json, headers):
        self.json = json
        self.headers = headers
        self.message = json['message']
        self.retry_after = json['retry_after']
        super().__init__(self.message)
