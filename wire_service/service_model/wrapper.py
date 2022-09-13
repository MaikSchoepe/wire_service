from typing import Any


class DbProxy:
    def __init__(self):
        self._model = None  # pragma: no cover

    @classmethod
    def wrap(cls, model: Any):
        wrapper = cls.__new__(cls)
        wrapper._model = model
        return wrapper

    def __getattr__(self, attr):
        result = getattr(self._model, attr)
        if isinstance(result, list):
            return list(map(DbProxy.wrap, result))

        return result
