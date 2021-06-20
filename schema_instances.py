single_object_schema = dict()
multi_object_schema = dict()


def register_schema(many=False):
    def register(cls):
        if many:
            multi_object_schema[cls] = cls(many=True)
        single_object_schema[cls] = cls()
        return cls

    return register


def get_schema_obj(clazz, many=False):
    return multi_object_schema.get(clazz) if many else single_object_schema.get(clazz)
