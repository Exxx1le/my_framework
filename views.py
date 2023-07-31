from datetime import date

from framework.templator import render
from patterns.creational_patterns import Engine, Logger

site = Engine()
logger = Logger("main")


class Index:
    def __call__(self, request):
        return "200 OK", render("index.html", object_list=site.categories)


class Contact:
    def __call__(self, request):
        return "200 OK", render("contact.html")


class NotFound404:
    def __call__(self, request):
        return "404", "Page Not Found"


class WorksList:
    def __call__(self, request):
        logger.log("Список работ")
        try:
            category = site.find_category_by_id(int(request["request_params"]["id"]))
            return "200 OK", render(
                "works_list.html",
                objects_list=category.works,
                name=category.name,
                id=category.id,
            )
        except KeyError:
            return "200 OK", "No such works"


class CreateWork:
    category_id = -1

    def __call__(self, request):
        if request["method"] == "POST":
            data = request["data"]

            name = data["name"]
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                work = site.create_work("record", name, category)
                site.works.append(work)

            return "200 OK", render(
                "works_list.html",
                objects_list=category.works,
                name=category.name,
                id=category.id,
            )

        else:
            try:
                self.category_id = int(request["request_params"]["id"])
                category = site.find_category_by_id(int(self.category_id))

                return "200 OK", render(
                    "create_work.html", name=category.name, id=category.id
                )
            except KeyError:
                return "200 OK", "No works to create"


class CreateCategory:
    def __call__(self, request):
        if request["method"] == "POST":
            data = request["data"]

            name = data["name"]
            name = site.decode_value(name)

            category_id = data.get("category_id")

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return "200 OK", render("index.html", objects_list=site.categories)
        else:
            categories = site.categories
            return "200 OK", render("create_category.html", categories=categories)


class CategoryList:
    def __call__(self, request):
        logger.log("Список категорий")
        return "200 OK", render("category_list.html", objects_list=site.categories)


class CopyWork:
    def __call__(self, request):
        request_params = request["request_params"]

        try:
            name = request_params["name"]

            old_work = site.get_work(name)
            if old_work:
                new_name = f"copy_{name}"
                new_work = old_work.clone()
                new_work.name = new_name
                site.works.append(new_work)

            return "200 OK", render(
                "works_list.html",
                objects_list=site.works,
                name=new_work.category.name,
            )
        except KeyError:
            return "200 OK", "No such works"
