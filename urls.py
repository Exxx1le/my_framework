from views import *


def front(request):
    request["key"] = "key"


fronts = [front]

routes = {
    "/": Index(),
    "/contact/": Contact(),
    "/examples/": Examples(),
    "/page/": Page(),
    "/another_page/": AnotherPage(),
}
