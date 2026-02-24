from typing import Any, Self, Type, final, get_type_hints

FORBIDDEN_METHODS = {"class", "dict", "weakref", "dir"}


@final
class NullObject:
    def __init__(self):
        pass

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
        if isinstance(value, NullObject):
            return True
        return False


class Skeleton:
    def __init__(self, proto: Type, /) -> None:
        """Class to use in place of others. Copies the methods and attributes of proto.

        WARNING: Unstable

        Args:
            proto(Type): Class to copy from.
        """
        if isinstance(proto, Skeleton):
            raise ValueError("Cannot create Skeleton of a Skeleton")
        if isinstance(proto, NullObject):
            raise ValueError("Cannot create Skeleton of a NullClass")
        self._proto = proto
        self._discover()

    def _dummy_return(self, return_type: type, /):
        try:
            return RETURNS[return_type]
        except KeyError as _:
            return NullObject()

    def _discover(self):
        for attr in {
            getattr(self._proto, a)
            for a in dir(self._proto)
            if a.strip("_") not in FORBIDDEN_METHODS
        }:
            if not callable(attr):
                setattr(self, attr, NullObject())
            try:
                return_type: type = get_type_hints(attr)["return"]
            except KeyError as _ke:
                return_type = NullObject
            setattr(
                self,
                attr.__name__,
                lambda *args, **kwargs: self._dummy_return(return_type),
            )
            continue

    def __bool__(self) -> bool:
        try:
            return self._proto().__bool__()
        except Exception as _:
            return False


RETURNS: dict[type, Any] = {
    str: "",
    int: -1,
    float: -0.1,
    list: [],
    dict: {"skeleton": True},
    set: {"skeleton"},
    NullObject: NullObject(),
}
