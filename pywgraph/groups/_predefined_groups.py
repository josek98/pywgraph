import numpy as np
from typing import Any
from ._groups import Group


# region: Real number 1 dimensional groups
def _reals_check(element: Any) -> bool:
    return isinstance(element, (int, float))


_real_multiplicative_group = Group(
    name="Real numbers with multiplication",
    identity=1.0,
    operation=lambda x, y: x * y,
    inverse_function=lambda x: 1 / x,
    group_checker=_reals_check,
    strict_total_order_function=lambda x, y: x < y,
)

_real_additive_group = Group(
    name="Real numbers with addition",
    identity=0.0,
    operation=lambda x, y: x + y,
    inverse_function=lambda x: -x,
    group_checker=_reals_check,
    strict_total_order_function=lambda x, y: x < y,
)

# region: Integers 1 dimensional groups
_integers_check = lambda x: isinstance(x, int)

_integer_additive_group = Group(
    name="Integers with addition",
    identity=1,
    operation=lambda x, y: x + y,
    inverse_function=lambda x: -x,
    group_checker=_integers_check,
    strict_total_order_function=lambda x, y: x < y,
)


# region: Real numbers N dimensional groups
def _reals_n_check(element: Any, n: int) -> bool:
    if not isinstance(element, np.ndarray):
        return False
    if element.shape != (n,):
        return False
    return True


def _reals_n_multiplicative_group(n: int) -> Group:
    return Group(
        name=f"Real numbers with elementwise multiplication in {n} dimensions",
        identity=np.ones(n),
        operation=lambda x, y: x * y,
        inverse_function=lambda x: 1 / x,
        group_checker=lambda x: _reals_n_check(x, n),
        strict_total_order_function=None,
    )


def _reals_n_additive_group(n: int) -> Group:
    return Group(
        name=f"Real numbers with elementwise addition in {n} dimensions",
        identity=np.zeros(n),
        operation=lambda x, y: x + y,
        inverse_function=lambda x: -x,
        group_checker=lambda x: _reals_n_check(x, n),
        strict_total_order_function=None,
    )


# region: Common groups
class CommonGroups:

    RealMultiplicative: Group = _real_multiplicative_group
    RealAdditive: Group = _real_additive_group
    IntegerAdditive: Group = _integer_additive_group

    @classmethod
    def RealsNMultiplicative(cls, n: int) -> Group:
        if not isinstance(n, int):
            raise TypeError("n must be an integer")
        if n == 1:
            return cls.RealMultiplicative
        if n < 1:
            raise ValueError("n must be a positive integer")
        return _reals_n_multiplicative_group(n)

    @classmethod
    def RealsNAdditive(cls, n: int) -> Group:
        if not isinstance(n, int):
            raise TypeError("n must be an integer")
        if n == 1:
            return cls.RealAdditive
        if n < 1:
            raise ValueError("n must be a positive integer")
        return _reals_n_additive_group(n)
