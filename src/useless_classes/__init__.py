from typing import Any


class NullClass:
    def __call__(self, *_args: Any, **_kwds: Any) -> None:  # pyright: ignore[reportAny, reportExplicitAny]
        return None

    def __getattr__(self, _: str) -> None:
        def method(*_args: Any, **_kwargs: Any) -> None:  # pyright: ignore[reportAny, reportExplicitAny]
            return None

        return method  # pyright: ignore[reportReturnType]
