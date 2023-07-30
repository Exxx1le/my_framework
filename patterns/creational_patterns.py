"""
Описывает модель сайта типа YouDo с заказчиками и исполнителями, заказывающими
разовые и переодические работы.
"""

from copy import deepcopy
from quopri import decodestring


class User:
    pass


# исполнитель заказа
class Contractor(User):
    pass


# заказчик
class Customer(User):
    pass


class UsersFactory:
    types = {"contractor": Contractor, "customer": Customer}

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


# выполняемые работы
class WorkPrototype:
    def clone(self):
        return deepcopy(self)


class Work(WorkPrototype):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.works.append(self)


# периодические работы (сервисы)
class ServiceWork(Work):
    pass


# разовые работы
class OneTimeWork(Work):
    pass


class WorkFactory:
    types = {"service": ServiceWork, "onetime": OneTimeWork}

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# категория работ
class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.works = []

    def works_count(self):
        result = len(self.works)
        if self.category:
            result += self.category.works_count()
        return result


class Engine:
    def __init__(self):
        self.contractors = []
        self.customers = []
        self.works = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UsersFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print("item", item.id)
            if item.id == id:
                return item
        raise Exception(f"Не найдено категории с id {id}")

    @staticmethod
    def create_work(type_, name, category):
        return WorkFactory.create(type_, name, category)

    def get_work(self, name):
        for item in self.works:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace("%", "=").replace("+", " "), "UTF-8")
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode("UTF-8")


class SingletonByName(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs["name"]

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print("log--->", text)
