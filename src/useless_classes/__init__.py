from typing import Any, Self, Type


FORBIDDEN_METHODS = {"class", "dict", "weakref", "dir"}


def empty():
    ...


class Skeleton:
    def __init__(self, proto: Type) -> None:
        """Class to use in place of others. Copies the methods and attributes of proto.

        Args:
            proto(Type): Class to copy from.
        """
        self._proto = proto
        self._discover()

    def _discover(self):
        for attr in {a for a in dir(self._proto) if a.strip("_") not in FORBIDDEN_METHODS}:
            if isinstance(attr, type(empty)):
                setattr(self, attr, lambda *args, **kwargs: NullClass())
                continue
            setattr(self, attr, NullClass())

    def __bool__(self) -> bool:
        try:
            return self._proto().__bool__()
        except Exception as _:
            return False


class NullClass:
    def __call__(self, *_args: Any, **_kwds: Any) -> Self:
        return self

    def __getattr__(self, _: str) -> Self:
        return self

    def __setattr__(self, name: str, value: Any, /) -> None:
        pass

    def __bool__(self) -> bool:
        """NullClass is always False"""
        return False

    def __str__(self) -> str:
        return str(None)

    def __repr__(self) -> str:
        return "NullClass"

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, NullClass):
            return True
        return False
