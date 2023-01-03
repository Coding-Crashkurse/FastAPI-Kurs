from typing import List, Optional, Union


def add(a: int, b: int) -> int:
    return a + b


def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    return a + b


def add_with_default(
    a: Union[int, float], b: Union[int, float], c: Optional[Union[int, float]] = None
) -> Union[int, float]:
    if not c:
        return a + b
    else:
        return a + b + c


def sum_list(numbers: List[Union[int, float]]) -> Union[int, float]:
    result = 0
    for number in numbers:
        result += number
    return result


Vector = list[float]


def scale(scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]


print(add(1, 2))
print(add(1.5, 2.5))
print(add_with_default(1, 2))
print(add_with_default(1, 2, 3))
print(sum_list([1, 2, 3, 4, 5]))
print(scale(2.0, [1.0, -4.2, 5.4]))
