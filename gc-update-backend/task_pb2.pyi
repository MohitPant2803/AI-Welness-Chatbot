from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LeaveRequest(_message.Message):
    __slots__ = ("currentMood", "isEscalated", "briefMoodSummary", "currentMoodRate", "userChat", "botChat", "empid", "wellnessScore", "moodAnalysis", "recommendedAction", "chatAIAnalysis")
    CURRENTMOOD_FIELD_NUMBER: _ClassVar[int]
    ISESCALATED_FIELD_NUMBER: _ClassVar[int]
    BRIEFMOODSUMMARY_FIELD_NUMBER: _ClassVar[int]
    CURRENTMOODRATE_FIELD_NUMBER: _ClassVar[int]
    USERCHAT_FIELD_NUMBER: _ClassVar[int]
    BOTCHAT_FIELD_NUMBER: _ClassVar[int]
    EMPID_FIELD_NUMBER: _ClassVar[int]
    WELLNESSSCORE_FIELD_NUMBER: _ClassVar[int]
    MOODANALYSIS_FIELD_NUMBER: _ClassVar[int]
    RECOMMENDEDACTION_FIELD_NUMBER: _ClassVar[int]
    CHATAIANALYSIS_FIELD_NUMBER: _ClassVar[int]
    currentMood: str
    isEscalated: bool
    briefMoodSummary: str
    currentMoodRate: str
    userChat: str
    botChat: str
    empid: str
    wellnessScore: int
    moodAnalysis: str
    recommendedAction: str
    chatAIAnalysis: str
    def __init__(self, currentMood: _Optional[str] = ..., isEscalated: bool = ..., briefMoodSummary: _Optional[str] = ..., currentMoodRate: _Optional[str] = ..., userChat: _Optional[str] = ..., botChat: _Optional[str] = ..., empid: _Optional[str] = ..., wellnessScore: _Optional[int] = ..., moodAnalysis: _Optional[str] = ..., recommendedAction: _Optional[str] = ..., chatAIAnalysis: _Optional[str] = ...) -> None: ...

class LeaveResponse(_message.Message):
    __slots__ = ("message", "jobId")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    JOBID_FIELD_NUMBER: _ClassVar[int]
    message: str
    jobId: str
    def __init__(self, message: _Optional[str] = ..., jobId: _Optional[str] = ...) -> None: ...
