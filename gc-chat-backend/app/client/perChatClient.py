import grpc
from client import perChat_pb2
from client import perChat_pb2_grpc

async def run(
            currentMood: str, isEscalated: bool, briefMoodSummary: str, currentMoodRate: str,
            userChat: str, botChat: str, empid:str,
            wellnessScore: int, moodAnalysis: str, recommendedAction: str, chatAIAnalysis: str):
    print(f"UPDATE PER CHAT FOR EMP - {empid}")
    async with grpc.aio.insecure_channel('http://gc-update-backend:50052') as channel:
        stub = perChat_pb2_grpc.LeaveServiceStub(channel)
        response = await stub.SubmitLeaveRequest(
            perChat_pb2.LeaveRequest(
                currentMood=currentMood,
                isEscalated=isEscalated,
                briefMoodSummary=briefMoodSummary,
                currentMoodRate=currentMoodRate,
                userChat=userChat,
                botChat=botChat,
                empid=empid,
                wellnessScore = wellnessScore,
                moodAnalysis =  moodAnalysis,
                recommendedAction = recommendedAction,
                chatAIAnalysis = chatAIAnalysis,
            )
        )
    print("UPDATE PER CHAT RESPONSE - ", response)