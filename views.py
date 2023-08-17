from datetime import date

from framework.templator import render
from patterns.сreational_patterns import Engine, Logger, MapperRegistry
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import (
    EmailNotifier,
    SmsNotifier,
    ListView,
    CreateView,
    BaseSerializer,
)
from patterns.architectural_system_pattern_unit_of_work import UnitOfWork

site = Engine()
logger = Logger("main")
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


routes = {}


@AppRoute(routes=routes, url="/")
class Index:
    @Debug(name="Index")
    def __call__(self, request):
        return "200 OK", render("index.html", object_list=site.categories)


@AppRoute(routes=routes, url="/contact/")
class Contact:
    def __call__(self, request):
        return "200 OK", render("contact.html")


class NotFound404:
    @Debug(name="NotFound404")
    def __call__(self, request):
        return "404", "Page Not Found"


@AppRoute(routes=routes, url="/works-list/")
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
            return "200 OK", "Works haven't been added yet"


@AppRoute(routes=routes, url="/create-work/")
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

                work.observers.append(email_notifier)
                work.observers.append(sms_notifier)

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
                return "200 OK", "Works haven't been added yet"


@AppRoute(routes=routes, url="/create-category/")
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


@AppRoute(routes=routes, url="/category-list/")
class CategoryList:
    def __call__(self, request):
        logger.log("Список категорий")
        return "200 OK", render("category_list.html", objects_list=site.categories)


@AppRoute(routes=routes, url="/copy-work/")
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
            return "200 OK", "Works haven't been added yet"


@AppRoute(routes=routes, url="/customer-list/")
class CustomerListView(ListView):
    template_name = "customer_list.html"

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper("customer")
        return mapper.all()


@AppRoute(routes=routes, url="/create-customer/")
class CustomerCreateView(CreateView):
    template_name = "create_customer.html"

    def create_obj(self, data: dict):
        name = data["name"]
        name = site.decode_value(name)
        new_obj = site.create_user("customer", name)
        site.customers.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url="/add-customer/")
class AddCustomerByWorkCreateView(CreateView):
    template_name = "add_customer.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["works"] = site.works
        context["customers"] = site.customers
        return context

    def create_obj(self, data: dict):
        work_name = data["work_name"]
        work_name = site.decode_value(work_name)
        work = site.get_work(work_name)
        customer_name = data["customer_name"]
        customer_name = site.decode_value(customer_name)
        customer = site.get_customer(customer_name)
        work.add_customer(customer)


@AppRoute(routes=routes, url="/api/")
class WorkApi:
    @Debug(name="workApi")
    def __call__(self, request):
        return "200 OK", BaseSerializer(site.works).save()
