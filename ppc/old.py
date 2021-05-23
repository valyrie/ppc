#

from collections import namedtuple
from typing import cast, Tuple, Union, List, Any

#character range helper
def chrs(start: str, stop: str) -> List[str]:
    return [chr(c) for c in range(ord(start), ord(stop) + 1)]

#parser state is immutable (thus uses pass-by-value aka copy semantics) due to subclassing tuple
class parserState(namedtuple("parserState", ["text", "eol", "src", "index", "line", "col", "saved", "failed"], defaults=["\n", "", 0, 0, 0, -1, False])):
    __slots__: List[str] = []
    
    @property
    def remaining(self) -> Any:
        return self.text[self.index:]

    @property
    def atstart(self) -> bool:
        return self.index == 0

    @property
    def atend(self) -> bool:
        return self.index == len(self.text)
    
    def copy(self, *, text: str = None, eol: str = None, src: str = None, index: int = None, line: int = None, col: int = None, saved: int = None, failed: bool = None) -> 'parserState':
        if not text: text = self.text
        if not eol: eol = self.eol
        if not src: src = self.src
        if not index: index = self.index
        if not line: line = self.line
        if not col: col = self.col
        if not saved: saved = self.saved
        if failed is None: failed = self.failed
        return parserState(text, eol, src, index, line, col, saved, failed)
    
    def advance(self, n: int = 1) -> 'parserState':
        if self.index + n > len(self.text):
            raise ValueError("unable to advance by {0} items, {1} only has {2} more".format(n, self, len(self.remaining)))
        line: int = self.line
        col: int = self.col

        for i in range(self.index, self.index + n):
            col += 1
            if self.text[i] == self.eol:
                line += 1
                col = 0
        
        return self.copy(index = self.index + n)
    
    def next(self, n: int = 1) -> Any:
        if self.index + n > len(self.text):
            raise ValueError("unable to get the next {0} items, {1} only has {2} more".format(n, self, len(self.remaining)))
        return self.text[self.index:self.index+n]
    
    def mark(self) -> 'parserState':
        if self.mark != -1: raise ValueError("unable to mark while a marked start already exists")
        return self.copy(saved = self.index)
    
    def unmark(self) -> 'parserState':
        if self.mark == -1: raise ValueError("unable to remove a marked start that doesn't exist")
        return self.copy(saved = -1)

    def lift(self) -> Tuple[Any, 'parserState']:
        if self.mark == -1:
            raise ValueError("unable to lift without a marked start")
        return self.text[self.saved:self.index]

    def accept(self, chars: Any) -> Union['parserState', None]:
        state: parserState = self
        for char in chars:
            if char != state.next():
                return None
            state = state.advance()
        return state

    #TODO properly handle sequences of chars, instead of just assuming they're 1 char long
    def skip(self, chars: Tuple[Any]) -> 'parserState':
        state: parserState = self
        while True:
            if state.next() not in chars:
                return state
            state = state.advance()

    def error(self, msg: str, *args: Any) -> 'parserException':
        return parserException(msg, self, *args)

class parserException(Exception):
    __slots__ = ["msg", "state", "args"]

    def __init__(self, msg: str, state: parserState, *args: Any):
        self.msg: str = msg
        self.state: parserState = state
        self.args: Tuple[Any] = cast(Tuple[Any], args)

