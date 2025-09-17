import requests
from typing import Dict, Any, Optional
from .errors import APIError, AuthError
import os

class HTTPClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: float = 30):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

        if not self.api_key:
            raise ValueError(
                "PROTONX_API_KEY is required. "
                "Please go to https://platform.protonx.io/ to obtain access token and set key PROTONX_API_KEY as environment variable."
            )

        self.timeout = timeout
        self.session = requests.Session()

    def _headers(self) -> Dict[str, str]:
        h = {"Content-Type": "application/json"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    def post(self, path: str, json_body: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        resp = self.session.post(url, headers=self._headers(), json=json_body, timeout=self.timeout)

        if resp.status_code == 401 or resp.status_code == 403:
            try:
                data = resp.json()
                readable = (
                    data.get("errors", {})
                        .get("server", {})
                        .get("readableMsg", "Unauthorized")
                )
                raise AuthError(f"{resp.status_code} Unauthorized: {readable}")
            except ValueError:
                raise AuthError(f"{resp.status_code} Unauthorized – invalid or missing PROTONX_API_KEY.")

        if not (200 <= resp.status_code < 300):
            # Try to include server message if available
            try:
                data = resp.json()
                readable = (
                    data.get("errors", {})
                        .get("server", {})
                        .get("readableMsg", resp.text)
                )
                raise APIError(resp.status_code, readable)
            except ValueError:
                raise APIError(resp.status_code, resp.text)

        return resp.json()
