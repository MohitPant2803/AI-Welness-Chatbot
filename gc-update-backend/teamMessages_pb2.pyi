from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateTeamMessagesRequest(_message.Message):
    __slots__ = ("empid", "numberOfteamMessages")
    EMPID_FIELD_NUMBER: _ClassVar[int]
    NUMBEROFTEAMMESSAGES_FIELD_NUMBER: _ClassVar[int]
    empid: str
    numberOfteamMessages: int
    def __init__(self, empid: _Optional[str] = ..., numberOfteamMessages: _Optional[int] = ...) -> None: ...

class UpdateTeamMessagesResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...
