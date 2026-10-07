import grpc
import meetingsAttended_pb2
import meetingsAttended_pb2_grpc
import asyncio

async def update_numberofmeetingattended(empid: str, numberOfmeetingsAttended: int):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = meetingsAttended_pb2_grpc.UserServiceStub(channel)
        response = await stub.UpdateMeeting(
            meetingsAttended_pb2.UpdateMeetingRequest(
                empid=empid, 
                numberOfmeetingsAttended=numberOfmeetingsAttended
            )
        )
        print("Response received:", response)

if __name__ == "__main__":
    asyncio.run(update_numberofmeetingattended("EMP1335", 10))
