from quopri import decodestring
from .requests_handler import GetRequests, PostRequests


class PageNotFound:
    def __call__(self, request):
        return "404", "404 PAGE Not Found"


class MyFramework:
    def __init__(self, routes_obj, fronts_obj) -> bytes:
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        path = environ["PATH_INFO"]

        if not path.endswith("/"):
            path = f"{path}/"

        request = {}
        method = environ["REQUEST_METHOD"]
        request["method"] = method

        if method == "POST":
            data = PostRequests().get_request_params(environ)
            request["data"] = MyFramework.decode_value(data)
            print(f"POST-request: {MyFramework.decode_value(data)}")
        if method == "GET":
            request_params = GetRequests().get_request_params(environ)
            request["request_params"] = MyFramework.decode_value(request_params)
            print(
                f"GET-request parameters" f" {MyFramework.decode_value(request_params)}"
            )

        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound()

        for front in self.fronts_lst:
            front(request)
        code, body = view(request)
        start_response(code, [("Content-Type", "text/html")])
        return [body.encode("utf-8")]

    @staticmethod
    def decode_value(data) -> dict:
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace("%", "=").replace("+", " "), "UTF-8")
            val_decode_str = decodestring(val).decode("UTF-8")
            new_data[k] = val_decode_str
        return new_data
