from datetime import date


def secret_front(request):
    request["date"] = date.today()


def other_front(request):
    request["key"] = "key"


fronts = [secret_front, other_front]

# routes = {
#     "/": Index(),
#     "/contact/": Contact(),
#     "/works-list/": WorksList(),
#     "/create-work/": CreateWork(),
#     "/create-category/": CreateCategory(),
#     "/category-list/": CategoryList(),
#     "/copy-work/": CopyWork(),
# }
