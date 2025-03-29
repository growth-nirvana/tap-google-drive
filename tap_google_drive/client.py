"""REST client handling for Google Drive API."""

from __future__ import annotations

import decimal
import typing as t
from functools import cached_property

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator
from singer_sdk.streams import RESTStream

from tap_google_drive.auth import GoogleDriveAuth

if t.TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Auth, Context


class GoogleDriveStream(RESTStream):
    """Base class for Google Drive streams."""

    # Update this value if necessary or override `parse_response`.
    records_jsonpath = "$[*]"

    @property
    def url_base(self) -> str:
        """Return the API URL root."""
        return "https://www.googleapis.com/drive/v3"

    @cached_property
    def authenticator(self) -> Auth:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return GoogleDriveAuth(
            client_id=self.config["client_id"],
            client_secret=self.config["client_secret"],
            refresh_token=self.config["refresh_token"]
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {
            "Accept": "application/json",
        }

    def get_new_paginator(self) -> BaseAPIPaginator:
        """Create a new pagination helper instance.

        Google Drive API uses pageToken for pagination.

        Returns:
            A pagination helper instance.
        """
        return super().get_new_paginator()

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page token from Google Drive API.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {
            "fields": "files(id, name, mimeType, modifiedTime)",
            "orderBy": "modifiedTime",
            "spaces": "drive",
        }
        if next_page_token:
            params["pageToken"] = next_page_token
        return params

    def prepare_request_payload(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: t.Any | None,  # noqa: ARG002, ANN401
    ) -> dict | None:
        """Prepare the data payload for the REST API request.

        Args:
            context: The stream context.
            next_page_token: The next page token.

        Returns:
            A dictionary with the JSON body for a POST requests.
        """
        return None

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        yield from extract_jsonpath(
            self.records_jsonpath,
            input=response.json(parse_float=decimal.Decimal),
        )

    def post_process(
        self,
        row: dict,
        context: Context | None = None,  # noqa: ARG002
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        return row
