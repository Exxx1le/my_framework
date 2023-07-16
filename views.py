from framework.templator import render


class Index:
    def __call__(self, request):
        return "200 OK", render("index.html")


class Contact:
    def __call__(self, request):
        return "200 OK", render("contact.html")


class Examples:
    def __call__(self, request):
        return "200 OK", render("examples.html")


class Page:
    def __call__(self, request):
        return "200 OK", render("page.html")


class AnotherPage:
    def __call__(self, request):
        return "200 OK", render("another_page.html")
