from typing import Any, Dict, List, Union
from ._http import HTTPClient

class Embeddings:
    """
    ProtonX Embeddings API wrapper
    Usage:
        client.embeddings.create(input="Hello world")
    """

    def __init__(self, http: HTTPClient):
        self._http = http

    def create(self, input: Union[str, List[str]], model: str = None, **kwargs: Any) -> Dict[str, Any]:
        if isinstance(input, str):
            texts = [input]
        else:
            texts = input

        payload = {"input": texts}
        if model is not None:
            payload["model"] = model  # optional, if your API supports it
        payload.update(kwargs)

        return self._http.post("/embeddings/", payload)
