from typing import Generic, TypeVar

T = TypeVar('T')

class CustomResponse(Generic[T]):
    def __init__(self, success: bool = False, message: str = "", data: T = None):
        self._success = success
        self._message = message
        self._data = data
        
    @property
    def success(self) -> bool:
        return self._success

    @success.setter
    def success(self, value: bool):
        self._success = value

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, value: str):
        self._message = value

    @property
    def data(self) -> T:
        return self._data

    @data.setter
    def data(self, value: T):
        self._data = value

    def __repr__(self):
        return f"CustomResponse(success={self.success}, message='{self.message}', data={self.data})"
    
    def to_server_response(self):
        return {
            "data": self.data,
            "success": self.success,
            "message": self.message
        }