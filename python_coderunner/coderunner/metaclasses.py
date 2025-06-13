class ContextMeta(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        cls.clear()

    def __call__(cls, *args, **kwargs):
        raise TypeError(f"Instantiation of class {cls.__name__} is not allowed")
