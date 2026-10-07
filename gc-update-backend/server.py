import asyncio
import logging
from grpc import aio
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

# Import all proto-generated modules
import user_pb2
import user_pb2_grpc
import task_pb2
import task_pb2_grpc
import emailsSent_pb2
import emailsSent_pb2_grpc
import meetingsAttended_pb2
import meetingsAttended_pb2_grpc
import teamMessages_pb2
import teamMessages_pb2_grpc
import workHours_pb2
import workHours_pb2_grpc

# Import celery tasks
from proj.tasks import (
    updateAtSOD,
    updateEmailsSend,
    updateMeeting,
    updateTeamMessages,
    updateWorkHours,
    updatePerChat
)

# User Service implementation
class UserServicer(
    user_pb2_grpc.UserServiceServicer,
    emailsSent_pb2_grpc.UserServiceServicer,
    meetingsAttended_pb2_grpc.UserServiceServicer,
    teamMessages_pb2_grpc.UserServiceServicer,
    workHours_pb2_grpc.UserServiceServicer,
    task_pb2_grpc.LeaveServiceServicer
):
    async def UpdateAtSOD(self, request, context):
        empid = request.empid
        
        try:
            # Queue the Celery task
            job = updateAtSOD.delay(empid)
            
            # Create timestamp for response
            now = datetime.now()
            timestamp = Timestamp()
            timestamp.FromDatetime(now)
            
            return user_pb2.UpdateAtSODResponse(
                success=True,
                message=f"Chat update request queued for {empid}",
                streakDays=0,
                numberOfParticipants=0,
                chatCheckInPoints=0,
                streakBonusPoints=0,
                timestamp=timestamp
            )
            
        except Exception as e:
            return user_pb2.UpdateAtSODResponse(
                success=False,
                message=f"Error processing request: {str(e)}",
                streakDays=0,
                numberOfParticipants=0,
                chatCheckInPoints=0,
                streakBonusPoints=0,
                timestamp=Timestamp()
            )
    
    async def UpdateEmails(self, request, context):
        empid = request.empid
        numberOfemailsSent = request.numberOfemailsSent
        
        try:
            job = updateEmailsSend.apply_async(
                args=[request.empid, request.numberOfemailsSent]
            )
            
            return emailsSent_pb2.UpdateEmailsResponse(
                success=True,
                message=f"updateEmailsSend request queued for {empid}",
            )
            
        except Exception as e:
            return emailsSent_pb2.UpdateEmailsResponse(
                success=False,
                message=f"Error processing request: {str(e)}",
            )
    
    async def UpdateMeeting(self, request, context):
        empid = request.empid
        numberOfmeetingsAttended = request.numberOfmeetingsAttended
        
        try:
            job = updateMeeting.apply_async(
                args=[request.empid, request.numberOfmeetingsAttended]
            )
            
            return meetingsAttended_pb2.UpdateMeetingResponse(
                success=True,
                message=f"updateMeeting request queued for {empid}",
            )
            
        except Exception as e:
            return meetingsAttended_pb2.UpdateMeetingResponse(
                success=False,
                message=f"Error processing request: {str(e)}",
            )
    
    async def UpdateTeamMessages(self, request, context):
        empid = request.empid
        numberOfteamMessages = request.numberOfteamMessages
        
        try:
            job = updateTeamMessages.apply_async(
                args=[request.empid, request.numberOfteamMessages]
            )
            
            return teamMessages_pb2.UpdateTeamMessagesResponse(
                success=True,
                message=f"Team messages update request queued for {empid}",
            )
            
        except Exception as e:
            return teamMessages_pb2.UpdateTeamMessagesResponse(
                success=False,
                message=f"Error processing request: {str(e)}",
            )
    
    async def UpdateWorkHours(self, request, context):
        empid = request.empid
        workHours = request.workHours
        
        try:
            job = updateWorkHours.apply_async(
                args=[request.empid, request.workHours]
            )
            
            return workHours_pb2.UpdateWorkHoursResponse(
                success=True,
                message=f"updateWorkHours request queued for {empid}",
            )
            
        except Exception as e:
            return workHours_pb2.UpdateWorkHoursResponse(
                success=False,
                message=f"Error processing request: {str(e)}",
            )
    
    async def SubmitLeaveRequest(self, request, context):
        print(request)
        job = updatePerChat.apply_async(
            args=[request.currentMood, request.isEscalated, request.briefMoodSummary, request.currentMoodRate, request.userChat, request.botChat, request.empid, request.wellnessScore, request.moodAnalysis, request.recommendedAction, request.chatAIAnalysis]
        )


        return task_pb2.LeaveResponse(message="Done prompting", jobId=job.id)



async def serve():
    server = aio.server(
        options=[
            ('grpc.so_reuseport', 1),
            ('grpc.max_concurrent_streams', 1000),
            ('grpc.max_send_message_length', 100*1024*1024),
            ('grpc.max_receive_message_length', 100*1024*1024)
        ]
    )
    
    # Register all servicers with the server
    user_servicer = UserServicer()
    
    # Add user service implementations
    user_pb2_grpc.add_UserServiceServicer_to_server(user_servicer, server)
    emailsSent_pb2_grpc.add_UserServiceServicer_to_server(user_servicer, server)
    meetingsAttended_pb2_grpc.add_UserServiceServicer_to_server(user_servicer, server)
    teamMessages_pb2_grpc.add_UserServiceServicer_to_server(user_servicer, server)
    workHours_pb2_grpc.add_UserServiceServicer_to_server(user_servicer, server)
    task_pb2_grpc.add_LeaveServiceServicer_to_server(user_servicer, server)
    

    # Start server on port 50051
    server.add_insecure_port('[::]:50052')
    await server.start()

    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(5)

if __name__ == '__main__':
    # Initialize database connection (if needed)
    # init_db()
    
    # Run the server
    asyncio.run(serve())