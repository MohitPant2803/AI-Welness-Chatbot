import grpc
import task_pb2
import task_pb2_grpc
import time
import asyncio

async def run(EMPID:str, EMAILID:str, MESSAGE:str, EMPNAME:str, TIMESTAMP:int):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = task_pb2_grpc.SchedulerStub(channel)
        response = stub.ScheduleMeet(
            task_pb2.MeetRequest(
                empid=EMPID,
                emailID=EMAILID,
                message=MESSAGE,
                empName=EMPNAME,
                timestamp=TIMESTAMP
            )
        )
    print("Response received:")
    print(f"Success: {response.success}")
    print(f"Job ID: {response.job_id}")
    
asyncio.run(run(EMPID="EMP987",EMAILID="flameable.powder@gmail.com",MESSAGE="i am sad because i could not meet the deadline?",EMPNAME="Abhinav?Sad",TIMESTAMP=int(time.time())))
