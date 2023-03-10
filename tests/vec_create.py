from pint import Quantity as Q_
from pint import Unit as U_

from veclite.vector import Vec, NODIM

import pytest

def test_creation():
    a = Vec(0)
    assert a.els == [0]
    assert a.units.is_compatible_with(NODIM)

    b = Vec(1, 2, 3)
    assert b.els == [1, 2, 3]
    assert b.units.is_compatible_with(NODIM)

    meter = U_("m")
    c = Vec([1, 2], units=meter)
    assert c.els == [1, 2]
    assert c.units.is_compatible_with(meter)

    d = Vec(Q_(1), Q_(2), Q_(4))
    assert d.els == [1, 2, 4]
    assert d.units.is_compatible_with(NODIM)
