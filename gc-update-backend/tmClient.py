import grpc
import teamMessages_pb2
import teamMessages_pb2_grpc
import asyncio

async def update_team_messages(empid: str, numberOfteamMessages: int):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = teamMessages_pb2_grpc.UserServiceStub(channel)
        response = await stub.UpdateTeamMessages(
            teamMessages_pb2.UpdateTeamMessagesRequest(
                empid=empid, 
                numberOfteamMessages=numberOfteamMessages
            )
        )
        print("Response received:", response)

if __name__ == "__main__":
    asyncio.run(update_team_messages("EMP1335", 10))
