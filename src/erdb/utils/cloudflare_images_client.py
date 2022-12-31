import requests
from typing import NamedTuple


class CloudflareImagesClient(NamedTuple):
    account_id: str
    api_token: str

    @property
    def endpoint(self) -> str:
        return f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/images/v1"

    @property
    def headers(self) -> dict:
        return {"Authorization": f"Bearer {self.api_token}"}

    def upload(self, data: bytes, image_id: str):
        files = {
            "file": data,
            "id": (None, image_id),
        }

        resp = requests.post(self.endpoint, headers=self.headers, files=files)

        if resp.status_code == 409:
            print(f"WARNING: {image_id} not uploaded due to conflict (409)", flush=True)
            return

        if resp.status_code != 200:
            print(f"Uploading {image_id} failed with response code {resp.status_code}.", flush=True)
            assert False, "Image upload to Cloudflare instance failed"