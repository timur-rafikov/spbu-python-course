from typing import Iterable, Callable, Any, Iterator


def data_generation(start: int, stop: int, step: int = 1) -> Iterator[int]:
    yield from range(start, stop, step)


def pipeline(
    data: Iterable[Any], operations: list[Callable[[Iterable[Any]], Iterable[Any]]]
) -> Iterable[Any]:
    stream = data
    for op in operations:
        stream = op(stream)
    return stream


def aggregate(stream: Iterable[Any]) -> list[Any]:
    return list(stream)


def custom_multiply(factor: int) -> Callable[[Iterable[Any]], Iterator[Any]]:
    def multiplier(stream: Iterable[Any]) -> Iterator[Any]:
        for item in stream:
            yield item * factor

    return multiplier
