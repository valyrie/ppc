# Python Parser Combinator library, rev 2

# inf hack
from typing import Any, Union, List
from types import FunctionType

class _inf(object):
    def __repr__(self) -> str:
        return "inf"

inf = _inf()

#TODO parser output type
class parse(object):
    __slots__ = ["remaining", "result", "error"]
    def __init__(self, remaining: str, result: Any, error: str = None):
        self.remaining = remaining
        self.result = result
        self.error = error

#parsers

class base(object):
    __slots__: List[Any] = []
    def __add__(self, other) -> 'seq':
        if not isinstance(other, base): return NotImplemented
        return seq(self, other)
    def __or__(self, other) -> 'alt':
        if not isinstance(other, base): return NotImplemented
        return alt(self, other)
    def rep(self, min: int, max: Union[int, _inf]=None) -> 'rep':
        if not max:
            max = min
        return rep(self, min, max)
    def maybe(self) -> 'maybe':
        return maybe(self)
    def any(self) -> 'any':
        return any(self)
    def some(self) -> 'some':
        return some(self)
    def bind(self, function) -> 'bound':
        return bound(self, function)
    def discard(self) -> 'discard':
        return discard(self)
    def parse(self, text, *args, **kwargs):
        pass #TODO

class forward(base):
    __slots__ = ["_def"]
    def __repr__(self):
        return repr(self._def)

class terminal(base):
    __slots__ = ["terminal"]
    def __init__(self, terminal: Any):
        self.terminal = terminal

class any1(base):
    __slots__: List[Any] = []

#TODO lookahead, any1

class maybe(base):
    __slots__ = ["pattern"]
    def __init__(self, pattern):
        self.pattern = pattern 

class any(base):
    __slots__ = ["pattern"]
    def __init__(self, pattern):
        self.pattern = pattern

class some(base):
    __slots__ = ["pattern"]
    def __init__(self, pattern):
        self.pattern = pattern

class rep(base):
    __slots__ = ["pattern", "min", "max"]
    def __init__(self, pattern, min: int, max: Union[int, _inf]):
        self.pattern = pattern
        self.min = min
        self.max = max

class seq(base):
    __slots__ = ["left", "right"]
    def __init__(self, left, right):
        self.left = left
        self.right = right

class alt(base):
    __slots__ = ["left", "right"]
    def __init__(self, left, right):
        self.left = left
        self.right = right

class bound(base):
    __slots__ = ["pattern", "function"]
    def __init__(self, pattern, function: FunctionType):
        self.pattern = pattern

class discard(base):
    __slots__ = ["pattern"]
    def __init__(self, pattern):
        self.pattern = pattern

class start(base):
    __slots__: List[Any] = []

class end(base):
    __slots__: List[Any] = []
