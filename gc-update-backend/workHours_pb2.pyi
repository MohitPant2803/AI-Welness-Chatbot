from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateWorkHoursRequest(_message.Message):
    __slots__ = ("empid", "workHours")
    EMPID_FIELD_NUMBER: _ClassVar[int]
    WORKHOURS_FIELD_NUMBER: _ClassVar[int]
    empid: str
    workHours: int
    def __init__(self, empid: _Optional[str] = ..., workHours: _Optional[int] = ...) -> None: ...

class UpdateWorkHoursResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...
