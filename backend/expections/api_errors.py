class APIError(Exception):
    status_code = 400
    message = "API Error"

    def __init__(self, message: str = None):
        if message:
            self.message = message
        super().__init__(self.message)

class NotSupportedFormatError(APIError):
    def __init__(self, supported_format: set[str]):
        formats_list = ','.join(sorted(supported_format))
        message = f"Unsupported file format. Supported formats: {formats_list}."
        super().__init__(message)

class MaxSizeError(APIError):
    def __init__(self, max_size_bytes: int):
        max_size = max_size_bytes / (1024 * 1024)
        message = f"File size exceeds the maximum allowed size of {max_size:.1f} MB."
        super().__init__(message)