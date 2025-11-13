from http.server import HTTPServer
from socketserver import BaseRequestHandler
from typing import Protocol, TypeVar, Any

T_contra = TypeVar("T_contra", contravariant=True)

class SupportsWrite(Protocol[T_contra]):
    def write(self,s: T_contra, /) -> object:...

class RequestHandlerFactory(Protocol):
    def __call__(self, request: Any, client_adress: Any, server: HTTPServer) -> BaseRequestHandler: ...