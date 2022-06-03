try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

from io import BytesIO, StringIO


def get_as_string(module, resource: str) -> str:
    return pkg_resources.read_text(module, resource)


def get_as_file_like_string(module, resource: str) -> StringIO:
    text: str = get_as_string(module, resource)
    return StringIO(text)


def get_as_bytes(module, resource: str) -> bytes:
    return pkg_resources.read_binary(module, resource)


def get_as_file_like_bytes(module, resource: str) -> BytesIO:
    text: bytes = get_as_bytes(module, resource)
    return BytesIO(text)


def get_path(module, resource: str):
    with pkg_resources.path(module, resource) as pth:
        return str(pth)
