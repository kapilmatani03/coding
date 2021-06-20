import functools

instances = dict()
event_handlers = dict()
instances_to_register = []
event_handlers_to_register = dict()


def locate_instance(clazz):
    return instances.get(clazz)


def register_instance(dependencies=None, arguments=None):
    def register(cls):
        instances_to_register.append((cls, dependencies, arguments))
        return cls

    return register


def get_event_handler(event_type):
    return event_handlers.get(event_type)


def register_event_handler(event_type):
    def register(cls):
        event_handlers_to_register[event_type] = cls
        return cls

    return register


def complete_instance_creation():
    for instance_to_register in instances_to_register:
        cls, dependencies, arguments = instance_to_register
        args = []
        if dependencies:
            for d in dependencies:
                args.append(locate_instance(d))

        if arguments:
            for arg in arguments:
                args.append(arg)

        instances[cls] = cls(*args)

    for event_type, cls in event_handlers_to_register.items():
        event_handlers[event_type] = locate_instance(cls)


def finalize_app_initialization():
    complete_instance_creation()


def inject(**services_to_inject):
    """
    :return:
    """

    def real_decorator(func):
        def wrapper(*args, **kwargs):
            """
            Wrapper
            :param args:
            :param kwargs:
            :return:
            """
            try:

                dependencies = dict()
                for service_name, service_class in services_to_inject.items():
                    dependencies[service_name] = locate_instance(service_class)
                r_val = func(*args, **kwargs, **dependencies)
                return r_val
            except Exception as e:
                raise e

        return functools.update_wrapper(wrapper, func)

    return real_decorator
