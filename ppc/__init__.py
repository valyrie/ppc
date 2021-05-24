# Python Parser Combinator library, rev 2

from collections import namedtuple
from types import FunctionType
from typing import Any, List

#parses
#TODO whole text storage, line tracking
parse = namedtuple("parse", ["text", "result", "error"], defaults=[None])

#parsers

#TODO fn to turn a parser into an error message
class parser(object):
    __slots__: List[Any] = []
    def __add__(self, other) -> 'seq':
        if not isinstance(other, parser): return NotImplemented
        return seq(self, other)
    def __or__(self, other) -> 'alt':
        if not isinstance(other, parser): return NotImplemented
        return alt(self, other)
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
    def parse(self, text, *args, **kwargs) -> parse:
        pass

#TODO lookaround, arbitrary rep, start

class forward(parser):
    __slots__ = ["_def"]
    def __init__(self):
        self._def: parser = None
    def __repr__(self):
        return repr(self._def)
    def parse(self, text, *args, **kwargs) -> parse:
        return self._def.parse(text, *args, **kwargs)

class terminal(parser):
    __slots__ = ["terminal"]
    def __init__(self, terminal: Any):
        self.terminal = terminal
    def parse(self, text, *args, **kwargs) -> parse:
        if not len(text):
            return parse(text, None, self)
        if text[0] != self.terminal:
            return parse(text, None, self)
        else:
            return parse(text[1:], [text[0]])

class any1(parser):
    __slots__: List[Any] = []
    def parse(self, text, *args, **kwargs) -> parse:
        if not len(text):
            return parse(text, None, self)
        else:
            return parse(text[1:], [text[0]])

class end(parser):
    __slots__: List[Any] = []
    def parse(self, text, *args, **kwargs) -> parse:
        if len(text):
            return parse(text, None, self)
        else:
            return parse(text, text)

class maybe(parser):
    __slots__ = ["pattern"]
    def __init__(self, pattern: parser):
        self.pattern = pattern
    def parse(self, text, *args, **kwargs) -> parse:
        p = self.pattern.parse(text, *args, **kwargs)
        if p.error:
            return parse(text, [])
        else:
            return p

class any(parser):
    __slots__ = ["pattern"]
    def __init__(self, pattern: parser):
        self.pattern = pattern
    def parse(self, text, *args, **kwargs) -> parse:
        p = self.pattern.parse(text, *args, **kwargs)
        if p.error:
            return parse(text, [])
        while True:
            q = self.pattern.parse(p.text, *args, **kwargs)
            if q.error:
                break
            p = parse(q.text, p.result + q.result)
        return p

class some(parser):
    __slots__ = ["pattern"]
    def __init__(self, pattern: parser):
        self.pattern = pattern
    def parse(self, text, *args, **kwargs) -> parse:
        p = self.pattern.parse(text, *args, **kwargs)
        if p.error:
            return parse(p.text, None, self)
        while True:
            q = self.pattern.parse(p.text, *args, **kwargs)
            if q.error:
                break
            p = parse(q.text, p.result + q.result)
        return p

class seq(parser):
    __slots__ = ["left", "right"]
    def __init__(self, left: parser, right: parser):
        self.left = left
        self.right = right
    def parse(self, text, *args, **kwargs) -> parse:
        l = self.left.parse(text, *args, **kwargs)
        if l.error:
            return l
        r = self.right.parse(l.text, *args, **kwargs)
        if r.error:
            return r
        return parse(r.text, l.result + r.result)

class alt(parser):
    __slots__ = ["left", "right"]
    def __init__(self, left: parser, right: parser):
        self.left = left
        self.right = right
    def parse(self, text, *args, **kwargs) -> parse:
        l = self.left.parse(text, *args, **kwargs)
        if not l.error:
            return l
        r = self.right.parse(text, *args, **kwargs)
        if not r.error:
            return r
        return parse(text, [], self)

class bound(parser):
    __slots__ = ["pattern", "function"]
    def __init__(self, pattern: parser, function: FunctionType):
        self.pattern = pattern
        self.function = function
    def parse(self, text, *args, **kwargs) -> parse:
        p = self.pattern.parse(text, *args, **kwargs)
        if p.error:
            return p
        else:
            return parse(p.text, self.function(p.result, *args, **kwargs))

class discard(parser):
    __slots__ = ["pattern"]
    def __init__(self, pattern: parser):
        self.pattern = pattern
    def parse(self, text, *args, **kwargs) -> parse:
        p = self.pattern.parse(text, *args, **kwargs)
        if p.error:
            return p
        else:
            return parse(p.text, [])