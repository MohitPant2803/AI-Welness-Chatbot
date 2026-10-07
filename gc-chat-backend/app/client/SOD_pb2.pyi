from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateAtSODRequest(_message.Message):
    __slots__ = ("empid",)
    EMPID_FIELD_NUMBER: _ClassVar[int]
    empid: str
    def __init__(self, empid: _Optional[str] = ...) -> None: ...

class UpdateAtSODResponse(_message.Message):
    __slots__ = ("success", "message", "streakDays", "numberOfParticipants", "chatCheckInPoints", "streakBonusPoints", "timestamp")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STREAKDAYS_FIELD_NUMBER: _ClassVar[int]
    NUMBEROFPARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    CHATCHECKINPOINTS_FIELD_NUMBER: _ClassVar[int]
    STREAKBONUSPOINTS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    streakDays: int
    numberOfParticipants: int
    chatCheckInPoints: int
    streakBonusPoints: int
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., streakDays: _Optional[int] = ..., numberOfParticipants: _Optional[int] = ..., chatCheckInPoints: _Optional[int] = ..., streakBonusPoints: _Optional[int] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
