from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MeetRequest(_message.Message):
    __slots__ = ("empid", "emailID", "message", "empName", "timestamp")
    EMPID_FIELD_NUMBER: _ClassVar[int]
    EMAILID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    EMPNAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    empid: str
    emailID: str
    message: str
    empName: str
    timestamp: int
    def __init__(self, empid: _Optional[str] = ..., emailID: _Optional[str] = ..., message: _Optional[str] = ..., empName: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...

class MeetResponse(_message.Message):
    __slots__ = ("success", "job_id")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    job_id: str
    def __init__(self, success: bool = ..., job_id: _Optional[str] = ...) -> None: ...
