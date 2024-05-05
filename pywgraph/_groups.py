from typing import Callable, TypeVar


"""Since I don't find an easy way of providing a way to indicate the elements of the 
group due to the limitations in type hinting in python, the class Group do not have
an attribute for the elements. Instead, it is initialize with a name, neutral element and 
a binary operator, this is, a callable. Is up to the user to ensure that the operation 
and the neutral element are compatible with the group."""

T = TypeVar("T")


class Group:
    def __init__(
        self,
        name: str,
        neutral_element: T,
        operation: Callable[[T, T], T],
        inverse_operation: Callable[[T, T], T],
        hash_function: Callable[[T], int] = hash
    ) -> None:
        self._name = name
        self._neutral_element = neutral_element
        self._operation = operation
        self._inverse_operation = inverse_operation
        self._hash_function = hash_function

    @property
    def name(self) -> str:
        return self._name

    @property
    def neutral_element(self) -> T:  # type: ignore
        return self._neutral_element

    @property
    def operation(self) -> Callable[[T, T], T]:
        return self._operation

    @property
    def inverse_operation(self) -> Callable[[T, T], T]:
        return self._inverse_operation

    def inverse(
        self, element: T
    ) -> (
        T
    ):  # Using self._neutral_element due to mypy not liking the return type of neutral_element property
        return self.inverse_operation(self._neutral_element, element)
    
    def equal(self, a: T, b: T) -> bool:
        return self._hash_function(a) == self._hash_function(b)

    def __call__(self, a: T, b: T) -> T:
        return self.operation(a, b)

    def __repr__(self) -> str:
        return self.name


if __name__ == "__main__":
    reals_prod = Group(
        "Real numbers with product", 1.0, lambda x, y: x * y, lambda x, y: x / y
    )
    print(reals_prod(2, 3))

    reals_sum = Group(
        "Real numbers with sum", 0.0, lambda x, y: x + y, lambda x, y: x - y
    )
    print(reals_sum(2, 3))

    import numpy as np
    reals_3 = Group("R^3 space", np.zeros(3), lambda x, y: x + y, lambda x, y: x - y, lambda x: hash(tuple(x)))
    print(reals_3(np.array([1, 2, 3]), np.array([4, 5, 6])))
    print(reals_3.inverse(np.array([1, 1, 1])))
    print(reals_3.equal(np.array([1,2,3]), np.array([1.0,2,3])))
