import grpc
import workHours_pb2
import workHours_pb2_grpc
import asyncio

async def update_work_hours(empid: str, workHours: int):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = workHours_pb2_grpc.UserServiceStub(channel)
        response = await stub.UpdateWorkHours(
            workHours_pb2.UpdateWorkHoursRequest(
                empid=empid, 
                workHours=workHours
            )
        )
        print("Response received:", response)

if __name__ == "__main__":
    asyncio.run(update_work_hours("EMP1402", 100))
