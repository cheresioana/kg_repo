from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Statement(_message.Message):
    __slots__ = ["type"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: str
    def __init__(self, type: _Optional[str] = ...) -> None: ...

class Entity(_message.Message):
    __slots__ = ["type", "values"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    type: str
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, type: _Optional[str] = ..., values: _Optional[_Iterable[str]] = ...) -> None: ...

class EntityResponse(_message.Message):
    __slots__ = ["entities"]
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    entities: _containers.RepeatedCompositeFieldContainer[Entity]
    def __init__(self, entities: _Optional[_Iterable[_Union[Entity, _Mapping]]] = ...) -> None: ...
