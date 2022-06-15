"""Hubspot tap class."""
import os
from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th
from tap_hubspot.streams import ContactsStream

ENTITIES = {
    "contacts": ContactsStream,
}

CONFIG_VARS = {
    "full_refresh": "TAP_HUBSPOT_FULL_REFRESH",
    "access_token": "TAP_HUBSPOT_ACCESS_TOKEN",
    "hapikey": "TAP_HUBSPOT_HAPIKEY",
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

        for k, v in CONFIG_VARS.items():
            if os.environ.get(v):
                self._config[k] = os.environ.get(v)

        self._config["full_refresh"] = str2bool(self._config["full_refresh"])

        return [
            ENTITIES[stream](tap=self, params=params)
            for stream, params in self.config.get("entities").items()
        ]
