import grpc
import emailsSent_pb2
import emailsSent_pb2_grpc
import asyncio

async def update_emails_send(empid: str, numberOfemailsSent: int):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = emailsSent_pb2_grpc.UserServiceStub(channel)
        response = await stub.UpdateEmails(
            emailsSent_pb2.UpdateEmailsRequest(
                empid=empid, 
                numberOfemailsSent=numberOfemailsSent
            )
        )
        print("Response received:", response)

if __name__ == "__main__":
    asyncio.run(update_emails_send("EMP1335", 10))
