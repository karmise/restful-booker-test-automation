"""Branding service client."""

from requests import Response

from restful_booker.api.clients.base_client import BaseApiClient


class BrandingClient(BaseApiClient):
    """Public branding operations."""

    def get_branding(self) -> Response:
        """Return current B&B branding and contact information."""

        return self._request("GET", "/branding")
