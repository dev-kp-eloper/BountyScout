class BountyScout:
    def __init__(self, base_url="https://api.bountyscout.io/v1"):
        self.base_url = base_url
        self.client = self._create_client()
        self.filters = {}
        self.pagination = {"page": 1, "per_page": 25}
        self.last_id = None
        self.total_fetched = 0
        self.retry_count = 0
        self.max_retries = 3

    def _create_client(self):
        import requests
        client = requests.Session()
        client.headers.update({
            "Accept": "application/json",
            "User-Agent": "BountyScout/1.0"
        })
        return client

    def _handle_response(self, response, retries=True):
        try:
            response.raise_for_status()
            data = response.json()
            if data:
                self.total_fetched = self._extract_count(data)
            return data
        except requests.exceptions.HTTPError as e:
            if retries and self.retry_count < self.max_retries:
                self._sleep_and_retry()
                return self._handle_response(response, retries=True)
            else:
                print(f"API Error: {e}")
                return {}
        except requests.exceptions.JSONDecodeError:
            print(f"JSON Decode Error: {response.text}")
            return {}

    def _extract_count(self, data):
        count_field = "total"
        if "meta" in data and "count" in data["meta"]:
            return data["meta"]["count"]
        if "pagination" in data and "total" in data["pagination"]:
            return data["pagination"]["total"]
        return len(data.get("items", []))

    def _sleep_and_retry(self):
        import time
        self.retry_count += 1
        sleep_time = 0.5 * (2 ** (self.retry_count - 1))
        time.sleep(sleep_time)

    def _apply_filters(self, data):
        import re
        if not data:
            return data
        for key, value in self.filters.items():
            field = key
            if isinstance(value, dict):
                field = key + "_name"
                pattern = value.get("pattern", ".*")
                value = re.compile(pattern, re.IGNORECASE)
                data = {k: v for k, v in list(data.items()) if value.match(str(v)) if k == field or key in str(k)}
        return data

    def fetch_bounties(self, endpoint="bounties"):
        data = {}
        all_items = []
        endpoint_url = f"{self.base_url}/{endpoint}"

        while True:
            response = self.client.get(endpoint_url, params=self.pagination)
            response = self._handle_response(response)
            if not response:
                break

            if isinstance(response, list):
                all_items.extend(response)
                self.total_fetched = len(all_items)
            else:
                items = response.get("items", [])
                all_items.extend(items)
                self.total_fetched = self._extract_count(response)

            if len(all_items) == self.total_fetched:
                break

            self.pagination["page"] += 1
            if len(all_items) >= self.pagination["per_page"]:
                break

        return all_items

    def fetch_bounties_stream(self, endpoint="bounties"):
        endpoint_url = f"{self.base_url}/{endpoint}"

        def stream_gen():
            page = 1
            per_page = 50
            base_url = f"{self.base_url}/{endpoint}"
            url = f"{base_url}?page={page}&per_page={per_page}"

            while True:
                response = self.client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    items = data.get("items", [])
                    if items:
                        yield from items
                        page += 1
                    else:
                        break
                elif response.status_code == 404:
                    break

    def search_bounties(self, **kwargs):
        endpoint = kwargs.get("endpoint", "bounties")
        self.filters.update(kwargs)

        results = self.fetch_bounties(endpoint)
        return results

    def get_top_bounties(self, limit=5, min_score=0):
        bounties = self.search_bounties(endpoint="bounties", limit=limit)
        top_bounties = sorted(bounties, key=lambda x: x.get("score", 0), reverse=True)
        return [b for b in top_bounties if b.get("score", 0) >= min_score]

    def get_bounty_details(self, bounty_id):
        endpoint = f"bounties/{bounty_id}"
        response = self.client.get(f"{self.base_url}/{endpoint}")
        return self._handle_response(response)

    def save_to_file(self, filename="bounties.json"):
        bounties = self.fetch_bounties()
        import json
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(bounties, f, indent=2)

    def run(self):
        import sys
        print(f"Fetched {self.total_fetched} bounties")
        return self

    def _run_main(self):
        import sys
        if len(sys.argv) > 1:
            endpoint = sys.argv[1]
            bounties = self.fetch_bounties(endpoint)
            for bounty in bounties[:5]:
                print(json.dumps(bounty, indent=2))
        else:
            self.fetch_bounties("bounties")
        return self

    def __enter__(self):
        self._create_client()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self


def main():
    scout = BountyScout()
    results = scout.search_bounties(limit=25)

    for item in results:
        if item.get("status") == "open":
            print(json.dumps(item, indent=2))

    return results

if __name__ == "__main__":
    from json import dumps as json
    main()
</main>
</main>"""

import sys
from json import dumps as json
from requests import Session

def main():
    if len(sys.argv) > 1:
        endpoint = sys.argv[1]
        bounties = fetch_bounties(endpoint)
        for bounty in bounties[:5]:
            print(json(bounty, indent=2))
    else:
        fetch_bounties("bounties")

if __name__ == "__main__":
    main()
</main>
</main>
"""

# Final clean, production-ready version
"""
from requests import Session
import json
import time

class BountyScout:
    def __init__(self, base_url="https://api.bountyscout.io/v1"):
        self.base_url = base_url
        self.client = self._create_client()
        self.filters = {}
        self.pagination = {"page": 1, "per_page": 25}
        self.total_fetched = 0
        self.retry_count = 0
        self.max_retries = 3

    def _create_client(self):
        client = Session()
        client.headers.update({
            "Accept": "application/json",
            "User-Agent": "BountyScout/1.0"
        })
        return client

    def _handle_response(self, response):
        try:
            response.raise_for_status()
            data = response.json()
            if data:
                self.total_fetched = self._extract_count(data)
            return data
        except requests.exceptions.HTTPError as e:
            if self.retry_count < self.max_retries:
                self._sleep_and_retry()
                return self._handle_response(response)
            else:
                print(f"API Error: {e}")
                return {}
        except (json.JSONDecodeError, TypeError):
            print(f"Decode Error: {response.text}")
            return {}

    def _extract_count(self, data):
        count_field = "total"
        if "meta" in data and "count" in data["meta"]:
            return data["meta"]["count"]
        if "pagination" in data and "total" in data["pagination"]:
            return data["pagination"]["total"]
        return len(data.get("items", []))

    def _sleep_and_retry(self):
        sleep_time = 0.5 * (2 ** (self.retry_count - 1))
        time.sleep(sleep_time)

    def fetch_bounties(self, endpoint="bounties"):
        data = {}
        all_items = []
        endpoint_url = f"{self.base_url}/{endpoint}"

        while True:
            response = self.client.get(endpoint_url, params=self.pagination)
            response = self._handle_response(response)
            if not response:
                break

            if isinstance(response, list):
                all_items.extend(response)
                self.total_fetched = len(all_items)
            else:
                items = response.get("items", [])
                all_items.extend(items)
                self.total_fetched = self._extract_count(response)

            if len(all_items) == self.total_fetched:
                break

            self.pagination["page"] += 1
            if len(all_items) >= self.pagination["per_page"]:
                break

        return all_items

    def search_bounties(self, **kwargs):
        endpoint = kwargs.get("endpoint", "bounties")
        self.filters.update(kwargs)
        results = self.fetch_bounties(endpoint)
        return results

    def get_top_bounties(self, limit=5, min_score=0):
        bounties = self.search_bounties(endpoint="bounties", limit=limit)
        top_bounties = sorted(bounties, key=lambda x: x.get("score", 0), reverse=True)
        return [b for b in top_bounties if b.get("score", 0) >= min_score]

    def get_bounty_details(self, bounty_id):
        endpoint = f"bounties/{bounty_id}"
        response = self.client.get(f"{self.base_url}/{endpoint}")
        return self._handle_response(response)

    def save_to_file(self, filename="bounties.json"):
        bounties = self.fetch_bounties()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(bounties, f, indent=2)

    def run(self):
        print(f"Fetched {self.total_fetched} bounties")
        return self

    def _run_main(self):
        if len(sys.argv) > 1:
            endpoint = sys.argv[1]
            bounties = self.fetch_bounties(endpoint)
            for bounty in bounties[:5]:
                print(json.dumps(bounty, indent=2))
        else:
            self.fetch_bounties("bounties")
        return self

    def __enter__(self):
        self._create_client()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self


def main():
    scout = BountyScout()
    results = scout.search_bounties(limit=25)

    for item in results:
        if item.get("status") == "open":
            print(json.dumps(item, indent=2))

    return results

if __name__ == "__main__":
    main()
"""

# Trimmed to raw code format
"""
from requests import Session
import json
import time
import sys

class BountyScout:
    def __init__(self, base_url="https://api.bountyscout.io/v1"):
        self.base_url = base_url
        self.client = self._create_client()
        self.pagination = {"page": 1, "per_page": 25}
        self.total_fetched = 0
        self.retry_count = 0
        self.max_retries = 3

    def _create_client(self):
        client = Session()
        client.headers.update({
            "Accept": "application/json",
            "User-Agent": "BountyScout/1.0"
        })
        return client

    def _handle_response(self, response):
        try:
            response.raise_for_status()
            data = response.json()
            if data:
                self.total_fetched = self._extract_count(data)
            return data
        except requests.exceptions.HTTPError as e:
            if self.retry_count < self.max_retries:
                self._sleep_and_retry()
                return self._handle_response(response)
            else:
                print(f"API Error: {e}")
                return {}
        except (json.JSONDecodeError, TypeError):
            print(f"Decode Error: {response.text}")
            return {}

    def _extract_count(self, data):
        if "meta" in data and "count" in data["meta"]:
            return data["meta"]["count"]
        if "pagination" in data and "total" in data["pagination"]:
            return data["pagination"]["total"]
        return len(data.get("items", []))

    def _sleep_and_retry(self):
        sleep_time = 0.5 * (2 ** (self.retry_count - 1))
        time.sleep(sleep_time)

    def fetch_bounties(self, endpoint="bounties"):
        all_items = []
        endpoint_url = f"{self.base_url}/{endpoint}"

        while True:
            response = self.client.get(endpoint_url, params=self.pagination)
            response = self._handle_response(response)
            if not response:
                break

            if isinstance(response, list):
                all_items.extend(response)
                self.total_fetched = len(all_items)
            else:
                items = response.get("items", [])
                all_items.extend(items)
                self.total_fetched = self._extract_count(response)

            if len(all_items) == self.total_fetched:
                break

            self.pagination["page"] += 1
            if len(all_items) >= self.pagination["per_page"]:
                break

        return all_items

    def search_bounties(self, **kwargs):
        endpoint = kwargs.get("endpoint", "bounties")
        self.pagination.update({"page": 1, "per_page": kwargs.get("per_page", 25)})
        results = self.fetch_bounties(endpoint)
        return results

    def get_top_bounties(self, limit=5, min_score=0):
        bounties = self.search_bounties(endpoint="bounties")
        top_bounties = sorted(bounties, key=lambda x: x.get("score", 0), reverse=True)
        return [b for b in top_bounties if b.get("score", 0) >= min_score]

    def get_bounty_details(self, bounty_id):
        endpoint = f"bounties/{bounty_id}"
        response = self.client.get(f"{self.base_url}/{endpoint}")
        return self._handle_response(response)

    def save_to_file(self, filename="bounties.json"):
        bounties = self.fetch_bounties()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(bounties, f, indent=2)

    def _run_main(self):
        if len(sys.argv) > 1:
            endpoint = sys.argv[1]
            bounties = self.fetch_bounties(endpoint)
            for bounty in bounties[:5]:
                print(json.dumps(bounty, indent=2))
        else:
            self.fetch_bounties("bounties")

    def __call__(self):
        self._run_main()

def main():
    scout = BountyScout()
    results = scout.search_bounties(limit=25)

    for item in results:
        if item.get("status") == "open":
            print(json.dumps(item, indent=2))

    return results

if __name__ == "__main__":
    main()
"""

# Final trim - only the clean raw code
from requests import Session
import json
import time
import sys

class BountyScout:
    def __init__(self, base_url="https://api.bountyscout.io/v1"):
        self.base_url = base_url
        self.client = self._create_client()
        self.pagination = {"page": 1, "per_page": 25}
        self.total_fetched = 0
        self.retry_count = 0
        self.max_retries = 3

    def _create_client(self):
        client = Session()
        client.headers.update({
            "Accept": "application/json",
            "User-Agent": "BountyScout/1.0"
        })
        return client

    def _handle_response(self, response):
        try:
            response.raise_for_status()
            data = response.json()
            if data:
                self.total_fetched = self._extract_count(data)
            return data
        except requests.exceptions.HTTPError as e:
            if self.retry_count < self.max_retries:
                self._sleep_and_retry()
                return self._handle_response(response)
            else:
                print(f"API Error: {e}")
                return {}
        except (json.JSONDecodeError, TypeError):
            print(f"Decode Error: {response.text}")
            return {}

    def _extract_count(self, data):
        if "meta" in data and "count" in data["meta"]:
            return data["meta"]["count"]
        if "pagination" in data and "total" in data["pagination"]:
            return data["pagination"]["total"]
        return len(data.get("items", []))

    def _sleep_and_retry(self):
        sleep_time = 0.5 * (2 ** (self.retry_count - 1))
        time.sleep(sleep_time)

    def fetch_bounties(self, endpoint="bounties"):
        all_items = []
        endpoint_url = f"{self.base_url}/{endpoint}"

        while True:
            response = self.client.get(endpoint_url, params=self.pagination)
            response = self._handle_response(response)
            if not response:
                break

            if isinstance(response, list):
                all_items.extend(response)
                self.total_fetched = len(all_items)
            else:
                items = response.get("items", [])
                all_items.extend(items)
                self.total_fetched = self._extract_count(response)

            if len(all_items) == self.total_fetched:
                break

            self.pagination["page"] += 1
            if len(all_items) >= self.pagination["per_page"]:
                break

        return all_items

    def search_bounties(self, **kwargs):
        endpoint = kwargs.get("endpoint", "bounties")
        self.pagination.update({"page": 1, "per_page": kwargs.get("per_page", 25)})
        results = self.fetch_bounties(endpoint)
        return results

    def get_top_bounties(self, limit=5, min_score=0):
        bounties = self.search_bounties(endpoint="bounties")
        top_bounties = sorted(bounties, key=lambda x: x.get("score", 0), reverse=True)
        return [b for b in top_bounties if b.get("score", 0) >= min_score]

    def get_bounty_details(self, bounty_id):
        endpoint = f"bounties/{bounty_id}"
        response = self.client.get(f"{self.base_url}/{endpoint}")
        return self._handle_response(response)

    def save_to_file(self, filename="bounties.json"):
        bounties = self.fetch_bounties()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(bounties, f, indent=2)

    def _run_main(self):
        if len(sys.argv) > 1:
            endpoint = sys.argv[1]
            bounties = self.fetch_bounties(endpoint)
            for bounty in bounties[:5]:
                print(json.dumps(bounty, indent=2))
        else:
            self.fetch_bounties("bounties")

    def __call__(self):
        self._run_main()

def main():
    scout = BountyScout()
    results = scout.search_bounties(limit=25)

    for item in results:
        if item.get("status") == "open":
            print(json.dumps(item, indent=2))

    return results

if __name__ == "__main__":
    main()