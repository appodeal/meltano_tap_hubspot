import requests


class HubspotClient:
    def __init__(self, config):
        self._access_token = config.get("access_token")
        self._hapikey = config.get("hapikey")

    def get_all_contacts(self, properties):
        endpoint = "https://api.hubapi.com/contacts/v1/lists/all/contacts/all"

        has_more = True
        vid_offset = None
        contacts = []

        while has_more:
            data = self._send_request(
                endpoint,
                {"vidOffset": vid_offset, "property": properties},
            )
            has_more = data["has-more"]
            vid_offset = data["vid-offset"]
            contacts += data["contacts"]

        return contacts

    def get_recently_updated_contacts(self, properties):
        endpoint = (
            "https://api.hubapi.com/contacts/v1/lists/recently_updated/contacts/recent"
        )

        has_more = True
        time_offset = None
        contacts = []

        while has_more:
            data = self._send_request(
                endpoint,
                {"timeOffset": time_offset, "property": properties},
            )
            has_more = data["has-more"]
            has_more = False
            time_offset = data["time-offset"]
            contacts += data["contacts"]

        return contacts

    def _send_request(self, url, params):
        request_params = {
            "count": 500,
            "property": ["email", "firstname", "hs_legal_basis", "acc__status"],
            "propertyMode": "value_and_history",
            "formSubmissionMode": "none",
            **params,
        }

        if self._access_token:
            headers = {"Authorization": f"Bearer {self._access_token}"}
        else:
            headers = {}
            request_params["hapikey"] = self._hapikey

        r = requests.get(url=url, params=request_params, headers=headers)
        return r.json()
