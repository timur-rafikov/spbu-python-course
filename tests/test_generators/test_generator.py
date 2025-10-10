from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from typing import Generator, List, Any, Tuple, Set, Callable, Iterable, Iterator
from project.generators.generator import Pipeline, data_generator, convert
from functools import reduce

# Auxiliary functions with type annotations instead of lambdas
def multiply_by_two(x: int) -> int:
    return x * 2


def multiply_by_three(x: int) -> int:
    return x * 3


def multiply_by_ten(x: int) -> int:
    return x * 10


def is_even(x: int) -> bool:
    return x % 2 == 0


def is_odd(x: int) -> bool:
    return x % 2 == 1


def greater_than_two(x: int) -> bool:
    return x > 2


def add_ten(x: int) -> int:
    return x + 10


def add_one(x: int) -> int:
    return x + 1


def sum_reducer(x: int, y: int) -> int:
    return x + y


def string_length(s: str) -> int:
    return len(s)


def custom_multiplier(
    iterable: Iterable[int], multiplier: int
) -> Generator[int, None, None]:
    for item in iterable:
        yield item * multiplier


# Fixtures for test data
@pytest.fixture
def sample_list_data() -> List[int]:
    return [1, 2, 3, 4, 5]


@pytest.fixture
def sample_range_data() -> range:
    return range(1, 6)


@pytest.fixture
def sample_generator_data() -> Generator[int, None, None]:
    def gen() -> Generator[int, None, None]:
        for i in range(1, 6):
            yield i

    return gen()


@pytest.fixture
def string_data() -> List[str]:
    return ["a", "b", "c", "d", "e"]


# Tests for data_generator
def test_data_generator_with_list(sample_list_data: List[int]) -> None:
    gen: Generator[int, None, None] = data_generator(sample_list_data)
    result: List[int] = list(gen)
    assert result == [1, 2, 3, 4, 5]


def test_data_generator_with_range(sample_range_data: range) -> None:
    gen: Generator[int, None, None] = data_generator(sample_range_data)
    result: List[int] = list(gen)
    assert result == [1, 2, 3, 4, 5]


def test_data_generator_with_generator(
    sample_generator_data: Generator[int, None, None]
) -> None:
    gen: Generator[int, None, None] = data_generator(sample_generator_data)
    result: List[int] = list(gen)
    assert result == [1, 2, 3, 4, 5]


# Tests for the convert function
def test_convert_map() -> None:
    mapper: Callable[[Iterable[int]], Iterator[int]] = convert(map, multiply_by_two)
    result: List[int] = list(mapper([1, 2, 3]))
    assert result == [2, 4, 6]


def test_convert_filter() -> None:
    filterer: Callable[[Iterable[int]], Iterator[int]] = convert(filter, is_even)
    result: List[int] = list(filterer([1, 2, 3, 4]))
    assert result == [2, 4]


def test_convert_enumerate() -> None:
    enumerator: Callable[[Iterable[str]], Iterator[Tuple[int, str]]] = convert(
        enumerate
    )
    result: List[Tuple[int, str]] = list(enumerator(["a", "b"]))
    assert result == [(0, "a"), (1, "b")]


def test_convert_enumerate_with_start() -> None:
    enumerator: Callable[[Iterable[str]], Iterator[Tuple[int, str]]] = convert(
        enumerate, start=1
    )
    result: List[Tuple[int, str]] = list(enumerator(["a", "b"]))
    assert result == [(1, "a"), (2, "b")]


def test_convert_reduce() -> None:
    reducer: Callable[[Iterable[int]], Iterator[int]] = convert(reduce, sum_reducer)
    result: List[int] = list(reducer([1, 2, 3]))
    assert result == [6]


def test_convert_reduce_with_initial() -> None:
    reducer: Callable[[Iterable[int]], Iterator[int]] = convert(reduce, sum_reducer, 10)
    result: List[int] = list(reducer([1, 2, 3]))
    assert result == [16]


def test_convert_custom_function() -> None:
    custom_converter: Callable[[Iterable[int]], Iterator[int]] = convert(
        custom_multiplier, 3
    )
    result: List[int] = list(custom_converter([1, 2, 3]))
    assert result == [3, 6, 9]


# Pipeline tests using convert
def test_pipeline_single_map_step(sample_list_data: List[int]) -> None:
    pipeline: Pipeline = Pipeline(sample_list_data)
    mapper: Callable[[Iterable[int]], Iterator[int]] = convert(map, multiply_by_two)
    result: List[int] = pipeline.pipe_step(mapper).aggregate()
    assert result == [2, 4, 6, 8, 10]


def test_pipeline_single_filter_step(sample_list_data: List[int]) -> None:
    pipeline: Pipeline = Pipeline(sample_list_data)
    filterer: Callable[[Iterable[int]], Iterator[int]] = convert(filter, is_even)
    result: List[int] = pipeline.pipe_step(filterer).aggregate()
    assert result == [2, 4]


def test_pipeline_multiple_steps(sample_list_data: List[int]) -> None:
    pipeline: Pipeline = Pipeline(sample_list_data)
    filterer: Callable[[Iterable[int]], Iterator[int]] = convert(
        filter, greater_than_two
    )
    mapper: Callable[[Iterable[int]], Iterator[int]] = convert(map, multiply_by_ten)
    result: List[int] = pipeline.pipe_step(filterer).pipe_step(mapper).aggregate()
    assert result == [30, 40, 50]


def test_pipeline_with_enumerate(string_data: List[str]) -> None:
    pipeline: Pipeline = Pipeline(string_data)
    enumerator: Callable[[Iterable[str]], Iterator[Tuple[int, str]]] = convert(
        enumerate, start=1
    )
    result: List[Tuple[int, str]] = pipeline.pipe_step(enumerator).aggregate()
    assert result == [(1, "a"), (2, "b"), (3, "c"), (4, "d"), (5, "e")]


def test_pipeline_with_reduce(sample_list_data: List[int]) -> None:
    pipeline: Pipeline = Pipeline(sample_list_data)
    reducer: Callable[[Iterable[int]], Iterator[int]] = convert(reduce, sum_reducer)
    result: List[int] = pipeline.pipe_step(reducer).aggregate()
    assert result == [15]


def test_pipeline_custom_aggregator(sample_list_data: List[int]) -> None:
    # We create separate pipelines for each aggregator to avoid repeated operations.
    # Tuple aggregator
    pipeline1: Pipeline = Pipeline(sample_list_data)
    mapper1: Callable[[Iterable[int]], Iterator[int]] = convert(map, multiply_by_two)
    result_tuple: Tuple[int, ...] = pipeline1.pipe_step(mapper1).aggregate(tuple)
    assert result_tuple == (2, 4, 6, 8, 10)

    # Set Aggregator
    pipeline2: Pipeline = Pipeline(sample_list_data)
    mapper2: Callable[[Iterable[int]], Iterator[int]] = convert(map, multiply_by_two)
    result_set: Set[int] = pipeline2.pipe_step(mapper2).aggregate(set)
    assert result_set == {2, 4, 6, 8, 10}

    # Sum aggregator
    pipeline3: Pipeline = Pipeline(sample_list_data)
    mapper3: Callable[[Iterable[int]], Iterator[int]] = convert(map, multiply_by_two)
    result_sum: int = pipeline3.pipe_step(mapper3).aggregate(sum)
    assert result_sum == 30


def test_pipeline_with_generator_input(
    sample_generator_data: Generator[int, None, None]
) -> None:
    pipeline: Pipeline = Pipeline(sample_generator_data)
    mapper: Callable[[Iterable[int]], Iterator[int]] = convert(map, add_ten)
    result: List[int] = pipeline.pipe_step(mapper).aggregate()
    assert result == [11, 12, 13, 14, 15]


def test_pipeline_with_range_input(sample_range_data: range) -> None:
    pipeline: Pipeline = Pipeline(sample_range_data)
    filterer: Callable[[Iterable[int]], Iterator[int]] = convert(filter, is_odd)
    result: List[int] = pipeline.pipe_step(filterer).aggregate()
    assert result == [1, 3, 5]


def test_pipeline_iteration(sample_list_data: List[int]) -> None:
    pipeline: Pipeline = Pipeline(sample_list_data)
    mapper: Callable[[Iterable[int]], Iterator[int]] = convert(map, multiply_by_three)
    pipeline.pipe_step(mapper)

    result: List[int] = []
    for item in pipeline:
        result.append(item)

    assert result == [3, 6, 9, 12, 15]


def test_pipeline_complex_workflow() -> None:
    # A complex pipeline with multiple transformations
    pipeline: Pipeline = Pipeline(range(1, 11))  # 1-10

    # Filter the even numbers, multiply by 3, and number them.
    filter_step: Callable[[Iterable[int]], Iterator[int]] = convert(filter, is_even)
    map_step: Callable[[Iterable[int]], Iterator[int]] = convert(map, multiply_by_three)
    enumerate_step: Callable[[Iterable[int]], Iterator[Tuple[int, int]]] = convert(
        enumerate, start=100
    )

    result: List[Tuple[int, int]] = (
        pipeline.pipe_step(filter_step)  # 2, 4, 6, 8, 10
        .pipe_step(map_step)  # 6, 12, 18, 24, 30
        .pipe_step(enumerate_step)  # (100,6), (101,12), etc.
        .aggregate()
    )

    assert result == [(100, 6), (101, 12), (102, 18), (103, 24), (104, 30)]


def test_pipeline_lazy_evaluation() -> None:
    # Calculation Laziness Test
    evaluation_count: int = 0

    def counting_generator() -> Generator[int, None, None]:
        nonlocal evaluation_count
        for i in [1, 2, 3, 4, 5]:
            evaluation_count += 1
            yield i

    pipeline: Pipeline = Pipeline(counting_generator())
    mapper: Callable[[Iterable[int]], Iterator[int]] = convert(map, multiply_by_two)
    pipeline.pipe_step(mapper)

    # Nothing is calculated before the iteration
    assert evaluation_count == 0

    # During aggregation, all the elements are calculated
    result: List[int] = pipeline.aggregate()
    assert evaluation_count == 5
    assert result == [2, 4, 6, 8, 10]


# Parameterized tests - corrected expected values
@pytest.mark.parametrize(
    "input_data, expected",
    [
        ([1, 2, 3, 4], [4, 8]),  # even numbers [2,4] -> multiplication by 2 [4,8]
        ([5, 6, 7, 8], [12, 16]),  # even numbers [6,8] -> multiplication by 2 [12,16]
        ([10, 11, 12], [20, 24]),  # even numbers [10,12] -> multiplication by 2 [20,24]
    ],
)
def test_pipeline_parameterized_filter_map(
    input_data: List[int], expected: List[int]
) -> None:
    pipeline: Pipeline = Pipeline(input_data)
    filter_step: Callable[[Iterable[int]], Iterator[int]] = convert(filter, is_even)
    map_step: Callable[[Iterable[int]], Iterator[int]] = convert(map, multiply_by_two)
    result: List[int] = pipeline.pipe_step(filter_step).pipe_step(map_step).aggregate()
    assert result == expected


@pytest.mark.parametrize(
    "aggregator_func, expected",
    [
        (list, [2, 4, 6, 8, 10]),
        (tuple, (2, 4, 6, 8, 10)),
        (set, {2, 4, 6, 8, 10}),
        (sum, 30),
    ],
)
def test_pipeline_different_aggregators(
    aggregator_func: Callable[[Iterable[int]], Any],
    expected: Any,
    sample_list_data: List[int],
) -> None:
    # Creating a new pipeline for each test
    pipeline: Pipeline = Pipeline(sample_list_data)
    mapper: Callable[[Iterable[int]], Iterator[int]] = convert(map, multiply_by_two)
    result: Any = pipeline.pipe_step(mapper).aggregate(aggregator_func)
    assert result == expected


# Tests to verify the chain of methods
def test_pipeline_method_chaining(sample_list_data: List[int]) -> None:
    result: List[int] = (
        Pipeline(sample_list_data)
        .pipe_step(convert(filter, greater_than_two))
        .pipe_step(convert(map, multiply_by_ten))
        .pipe_step(convert(map, add_one))
        .aggregate()
    )
    assert result == [31, 41, 51]


def test_pipeline_empty_data() -> None:
    pipeline: Pipeline = Pipeline([])
    mapper: Callable[[Iterable[int]], Iterator[int]] = convert(map, multiply_by_two)
    result: List[int] = pipeline.pipe_step(mapper).aggregate()
    assert result == []


def test_pipeline_single_element() -> None:
    pipeline: Pipeline = Pipeline([42])
    mapper: Callable[[Iterable[int]], Iterator[int]] = convert(map, multiply_by_two)
    result: List[int] = pipeline.pipe_step(mapper).aggregate()
    assert result == [84]
