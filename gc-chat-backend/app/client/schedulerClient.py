import grpc
from client import scheduler_pb2
from client import scheduler_pb2_grpc

async def run(EMPID:str, EMAILID:str, MESSAGE:str, EMPNAME:str, TIMESTAMP:int):
    print(f"SCHEDULER FOR EMP - {EMPID}")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = scheduler_pb2_grpc.SchedulerStub(channel)
        response = stub.ScheduleMeet(
            scheduler_pb2.MeetRequest(
                empid=EMPID,
                emailID=EMAILID,
                message=MESSAGE,
                empName=EMPNAME,
                timestamp=TIMESTAMP
            )
        )
    print("SCHEDULER RESPONSE - ", response)