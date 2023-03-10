from typing import cast
from pint import Quantity as Q_
from pint import Unit as U_

from functools import reduce

Value = int | float | Q_

NODIM = U_("1")

class Vec:
    els: list[float]
    units: U_

    def __init__(self, *args, units=None):
        if len(args) == 0:
            raise ValueError("Cannot create a dimensionless vector!")

        if units is None:
            self.units = None
        else:
            try:
                self.units = U_(units)
            except TypeError as err:
                raise err
        
        self.els = list()
        
        try:
            for a in args:
                if isinstance(a, Q_):
                    if self.units is None:
                        self.units = a.units
                    assert a.units.is_compatible_with(self.units)
                    self.els.append(a.to(self.units).m)
                if isinstance(a, int | float):
                    if self.units is None:
                        self.units = U_(NODIM)
                    self.els.append(a)
                else:
                    raise TypeError("Vectors elements have to be numbers or quantities!")
        except:
            raise ValueError("Vector elements not compatible with each others!")

        self.nodim = self.units.is_compatible_with(NODIM)
        self.dim = len(self.els)

    def __repr__(self) -> str:
        return (
            f"<Vec (" +
            reduce(lambda a, b : str(a) + ", " + str(b), self.els) +
            ")>"
        )

    def __getitem__(self, idx: int) -> Value:
        el = self.els[idx]
        if self.nodim:
            return el
        return el * self.units

    def __setitem__(self, idx: int, val: Value):
        if isinstance(val, Q_) and val.units.is_compatible_with(self.units):
            self.els[idx] = val.to(self.units).m
        elif isinstance(val, int | float) and self.nodim:
            self.els[idx] = val
        else:
            raise TypeError("Given element not compatible with vector's units!")

class Vec2(Vec):
    def __init__(*args, **kwargs):
        units = U_(NODIM)
        try:
            units = kwargs["units"]
            del kwargs["units"]
        except:
            pass

        if len(kwargs) == 0:
            if len(args) != 2:
                raise ValueError("Two arguments please!")
            super().__init__(args, units=units)
        elif len(args) == 0:
            try:
                super().__init__(kwargs["x"], kwargs["y"], units=units)
            except KeyError:
                raise ValueError("'x' and 'y' needed for kwargs!")
        else:
            raise ValueError("args OR kwargs, not both!")

    @property
    def x(self) -> Value:
        return self[0]
    
    @x.setter
    def x(self, val: Value):
        self[0] = val
    
    @property
    def y(self) -> Value:
        return self[1]
    
    @y.setter
    def y(self, val: Value):
        self[1] = val