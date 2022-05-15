from typing import Any


class DbProxy:
    def __init__(self):
        self._model = None

    @classmethod
    def wrap(cls, model: Any):
        wrapper = object.__new__(cls)
        wrapper._model = model
        return wrapper

    def __getattr__(self, attr):
        result = getattr(self._model, attr)
        if isinstance(result, list):
            return list(map(DbProxy.wrap, result))

        return result
