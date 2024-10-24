from urllib.parse import urlencode


def build_url(base_url: str, path: str=None, *args, **kwargs) -> str:
    """
    Constructs a complete URL by combining a base URL, a path, and optional query parameters.
    """
    url = base_url.rstrip('/')
    if path:
        _uri = path.strip('/')
        url = '{}/{}'.format(url, _uri) if _uri else url
    if kwargs:
        url = '{}?{}'.format(url, urlencode(kwargs))
    return url