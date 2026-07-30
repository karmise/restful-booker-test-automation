"""Branding service client."""

from requests import Response

from restful_booker.api.clients.base_client import BaseApiClient
from restful_booker.reporting import report_step


class BrandingClient(BaseApiClient):
    """Public branding operations."""

    @report_step("Request public branding")
    def get_branding(self) -> Response:
        """Return current B&B branding and contact information."""

        return self._request("GET", "/branding")
