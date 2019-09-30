"""

AUTOR: Juanjo

FECHA DE CREACIÓN: 26/09/2019

"""


def parse_args(request_json, schema, partial=False):
    if not request_json:
        raise NoValidParamsError()
    errors = schema.validate(request_json, partial=partial)
    if errors:
        raise NoValidParamsError(str(errors))


class AppErrorBaseClass(Exception):
    pass


class NoValidParamsError(AppErrorBaseClass):
    pass


class ObjectNotFound(AppErrorBaseClass):
    pass


class MultipleObjectsFound(AppErrorBaseClass):
    pass
