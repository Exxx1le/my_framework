from views import *
from datetime import date


def secret_front(request):
    request["date"] = date.today()


def other_front(request):
    request["key"] = "key"


fronts = [secret_front, other_front]

routes = {
    "/": Index(),
    "/contact/": Contact(),
    "/examples/": Examples(),
    "/page/": Page(),
    "/another_page/": AnotherPage(),
}
