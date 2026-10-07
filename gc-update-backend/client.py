import grpc
import asyncio
import task_pb2
import task_pb2_grpc

async def run(
            currentMood: str, isEscalated: bool, briefMoodSummary: str, currentMoodRate: int,
            userChat: str, botChat: str, empid:str,
            wellnessScore: int, moodAnalysis: str, recommendedAction: str, chatAIAnalysis: str):
    async with grpc.aio.insecure_channel('localhost:50052') as channel:
        stub = task_pb2_grpc.LeaveServiceStub(channel)
        response = await stub.SubmitLeaveRequest(
            task_pb2.LeaveRequest(
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
    print("Response received:", response)

async def main():
    await run(
        currentMood="tired",
        isEscalated=True,
        briefMoodSummary="Feeling unwell for a few days",
        currentMoodRate="90%",
        userChat="Hey, I am feeling sick.",
        botChat="I understand, take care!",
        empid="EMP1335",
        wellnessScore=78,
        moodAnalysis="Bhaag jaa Bhosdike",
        recommendedAction="Take a break",
        chatAIAnalysis="You need to rest",
    )

asyncio.run(main())