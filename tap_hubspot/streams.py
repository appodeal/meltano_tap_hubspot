import os
import json
from singer_sdk import typing as th
from singer_sdk import Stream
from .hubspot import HubspotClient


class ContactsStream(Stream):
    def __init__(self, tap=None, params=None):
        self._params = params
        self._full_refresh = tap.config.get("full_refresh")
        self._hubspot = HubspotClient(tap.config)
        self._properties = params.get("properties", [])
        self._system_properties = ["vid", "addedAt"]
        super().__init__(tap=tap)

    @property
    def name(self):
        """Return primary key dynamically based on user inputs."""
        return self._params["stream"]

    @property
    def primary_keys(self):
        return ["vid"]

    @property
    def schema(self) -> dict:
        properties = [
            th.Property(p, th.StringType)
            for p in [*self._system_properties, *self._properties]
        ]

        return th.PropertiesList(*properties).to_dict()

    def get_records(self, context):
        data = (
            self._hubspot.get_all_contacts(self._properties)
            if self._full_refresh
            else self._hubspot.get_recently_updated_contacts(self._properties)
        )

        for raw_row in data:
            row = {key: raw_row[key] for key in self._system_properties}

            for p in self._properties:
                value = raw_row["properties"].get(p)
                row[p] = value["value"] if value else ""

            yield row
