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


def data_generator(
    data: Union[Generator[Any, None, None], range, List[Any], Iterable[Any]]
) -> Generator[Any, None, None]:
    if isinstance(data, Generator):
        yield from data
    else:
        for el in data:
            yield el


class Pipeline:
    def __init__(self, data: Iterable[Any]):
        self.data = data
        self.steps: List[
            Tuple[Callable[..., Any], Tuple[Any, ...], Dict[str, Any]]
        ] = []

    def __iter__(self) -> Iterator[Any]:
        it = self.data
        for func, args, kwargs in self.steps:
            it = func(*args, it, **kwargs)
        return iter(it)

    def pipe_step(
        self, func: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> "Pipeline":
        self.steps.append((func, args, kwargs))
        return self

    def aggregate(
        self,
        aggregator: Callable[[Iterable[Any]], Any] = list,
        *args: Any,
        **kwargs: Any
    ) -> Any:
        return aggregator(self.__iter__(), *args, **kwargs)


def convert(
    func: Callable[..., Any], *args: Any, **kwargs: Any
) -> Callable[[Iterable[Any]], Iterator[Any]]:
    if func in [filter, map, enumerate]:
        return lambda it: func(*args, it, **kwargs)
    elif func == reduce:
        if len(args) < 2:
            return lambda it: iter([func(*args, it, **kwargs)])
        else:
            return lambda it: iter([func(args[0], it, *args[1:], **kwargs)])
    else:
        return lambda it: func(it, *args, **kwargs)
