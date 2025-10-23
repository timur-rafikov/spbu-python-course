from typing import (
    Iterable,
    Callable,
    Any,
    Iterator,
    List,
    Union,
    Generator,
    Tuple,
    Dict,
)
from functools import reduce
import random


def data_generator(
    start: int = 0, end: int = 10, step: int = 1, data_type: str = "range"
) -> Generator[Any, None, None]:
    """
    Generates data based on specified parameters

    Args:
        start (int): Starting value for generation
        end (int): Ending value for generation
        step (int): Step size for generation
        data_type (str): Type of data to generate ("range", "random", "fibonacci")

    Yields:
        Generator[Any, None, None]: Generated data values
    """
    if data_type == "range":
        current = start
        while current < end:
            yield current
            current += step
    elif data_type == "random":
        for _ in range((end - start) // step):
            yield random.randint(start, end - 1)
    elif data_type == "fibonacci":
        a, b = 0, 1
        while a < end:
            yield a
            a, b = b, a + b


class Pipeline:
    """
    A class for lazy data processing

    Attributes:
        data : Iterable[Any]
            Source iterable data

    Methods:
        __init__(self, data: Iterable[Any])
            Initialization of data

        __iter__(self) -> Iterator[Any]
            Returns iterator over processed data

        def pipe_step(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> "Pipeline"
            Add a step to the Pipeline

        def aggregate(
            self,
            aggregator: Callable[[Iterable[Any]], Any] = list,
            *args: Any,
            **kwargs: Any
        ) -> Any
            Aggregates data into an aggregator
    """

    def __init__(self, data: Iterable[Any]):
        """
        Initialization of data

        Args:
            data (Iterable[Any]): Data
        """
        self.data = data
        self.steps: List[
            Tuple[Callable[..., Any], Tuple[Any, ...], Dict[str, Any]]
        ] = []

    def __iter__(self) -> Iterator[Any]:
        """
        Performs all the steps

        Returns:
            Iterator[Any]: iterator over processed data
        """
        it = self.data
        for func, args, kwargs in self.steps:
            if func == reduce:
                if len(args) < 2:
                    it = iter([func(*args, it, **kwargs)])
                else:
                    it = iter([func(args[0], it, *args[1:], **kwargs)])
            elif func in [filter, map, enumerate]:
                it = func(*args, it, **kwargs)
            else:
                it = func(it, *args, **kwargs)
        return iter(it)

    def pipe_step(
        self, func: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> "Pipeline":
        """
        Adds a step

        Args:
            func (Callable[..., Any]): input function

        Returns:
            Pipeline: self object
        """
        self.steps.append((func, args, kwargs))
        return self

    def aggregate(
        self,
        aggregator: Callable[[Iterable[Any]], Any] = list,
        *args: Any,
        **kwargs: Any
    ) -> Any:
        """
        Aggregates data into an aggregator

        Args:
            aggregator (Callable[[Iterable[Any]], Any], optional): aggrefator. Defaults to list.

        Returns:
            Any: Aggregated data
        """
        return aggregator(self.__iter__(), *args, **kwargs)
