from aiohttp.web import View as AiohttpView


class View(AiohttpView):
    @property
    def data(self) -> dict:
        return self.request.get("data", {})

    @property
    def query(self) -> dict:
        return self.request.get("querystring", {})
