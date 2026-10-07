import grpc
from client import SOD_pb2
from client import SOD_pb2_grpc

async def updatePerChat(empid: str):
    async with grpc.aio.insecure_channel("http://gc-update-backend:50052") as channel:
        print(f"UPDATE SOD FOR EMP - {empid}")
        stub = SOD_pb2_grpc.UserServiceStub(channel)
        response = await stub.UpdateAtSOD(
            SOD_pb2.UpdateAtSODRequest(empid=empid)
        )
        print("UPDATE SOD RESP - ", response)