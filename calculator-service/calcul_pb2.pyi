from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class numberRes(_message.Message):
    __slots__ = ("resultat",)
    RESULTAT_FIELD_NUMBER: _ClassVar[int]
    resultat: int
    def __init__(self, resultat: _Optional[int] = ...) -> None: ...

class numbersReq(_message.Message):
    __slots__ = ("number1", "number2")
    NUMBER1_FIELD_NUMBER: _ClassVar[int]
    NUMBER2_FIELD_NUMBER: _ClassVar[int]
    number1: int
    number2: int
    def __init__(self, number1: _Optional[int] = ..., number2: _Optional[int] = ...) -> None: ...
