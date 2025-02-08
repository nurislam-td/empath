from litestar import Router

from .controllers import FileStorageController

router = Router(
    path="/file-storage", route_handlers=[FileStorageController], tags=["File storage"]
)
