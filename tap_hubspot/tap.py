"""Hubspot tap class."""
import os
from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th
from tap_hubspot.streams import ContactsStream

ENTITIES = {
    "contacts": ContactsStream,
}


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


class TapHubspot(Tap):
    """Hubspot tap class."""

    name = "tap-hubspot"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "hapikey",
            th.StringType,
        ),
        th.Property(
            "properties",
            th.StringType,
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""

        self._config["full_refresh"] = str2bool(
            os.environ.get("TAP_HUBSPOT_FULL_REFRESH", False)
        )

        return [
            ENTITIES[stream](tap=self, params=params)
            for stream, params in self.config.get("entities").items()
        ]
