from wsgiref.simple_server import make_server

from framework.main import MyFramework
from urls import routes, fronts


application = MyFramework(routes, fronts)

with make_server("", 8000, application) as httpd:
    print("Запуск на порту 8000")
    httpd.serve_forever()
