from typing import Iterable, Callable, Any, Iterator, List


def data_generation(start: int, stop: int, step: int = 1) -> Iterator[int]:
    """
    Input Data Generator

    Args:
        start (int): The beginning of the range
        stop (int): The end of the range
        step (int, optional): Step. Defaults to 1.

    Yields:
        Iterator[int]: The resulting generator
    """
    yield from range(start, stop, step)


def pipeline(
    data: Iterable[Any], operations: List[Callable[[Iterable[Any]], Iterable[Any]]]
) -> Iterable[Any]:
    """
    A pipeline function that sequentially applies passed operations to the input sequence

    Args:
        data (Iterable[Any]): Input data
        operations (list[Callable[[Iterable[Any]], Iterable[Any]]]): List of operations

    Returns:
        Iterable[Any]: The resulting iterator
    """
    stream = data
    for op in operations:
        stream = op(stream)
    return stream


def aggregate(stream: Iterable[Any]) -> list[Any]:
    """
    Aggregator function that collect the Iterable into a collection

    Args:
        stream (Iterable[Any]): Stream

    Returns:
        list[Any]: Collection
    """
    return list(stream)


# Example custom operation
def custom_multiply(factor: int) -> Callable[[Iterable[Any]], Iterator[Any]]:
    """
    User operations. Multiplies each element by a factor

    Args:
        factor (int): What to multiply by

    Returns:
        Callable[[Iterable[Any]], Iterator[Any]]: Returns the operation
    """

    def multiplier(stream: Iterable[Any]) -> Iterator[Any]:
        for item in stream:
            yield item * factor

    return multiplier
