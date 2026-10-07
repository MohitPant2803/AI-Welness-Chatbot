import grpc
import user_pb2
import user_pb2_grpc
import asyncio

async def update_per_chat(empid: str):
    async with grpc.aio.insecure_channel("localhost:50052") as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        response = await stub.UpdateAtSOD(
            user_pb2.UpdateAtSODRequest(empid=empid)
        )
        print("Response received:", response)

if __name__ == "__main__":
    asyncio.run(update_per_chat("EMP1335"))