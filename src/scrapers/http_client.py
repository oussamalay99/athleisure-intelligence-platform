import requests


class HttpClient:
    def __init__(self, timeout: int = 20):
        self.timeout = timeout

        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/140.0 Safari/537.36"
                )
            }
        )

    def get(self, url:str) -> requests.Response:
        response = self.session.get(
            url,
            timeout=self.timeout
        )

        response.raise_for_status()

        return response
