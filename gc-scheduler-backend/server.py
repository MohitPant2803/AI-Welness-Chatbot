import asyncio
import logging
from grpc import aio
import task_pb2
import task_pb2_grpc
from datetime import datetime, timezone
from proj.tasks import addMailToQueue
import redis

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_redis_client():
    """
    Create a Redis client with the same configuration as in your auth system.
    """
    # Using the exact configuration you provided
    return redis.Redis(
        host="localhost",  # Replace with your AWS Redis host if different in production
        port=6379,
        decode_responses=True
    )

# Email tracking configuration
EMAIL_SET_KEY = 'sent_emails'
EMAIL_TTL_SECONDS = 86400  # 1 day in seconds

# Initialize Redis client with same configuration as your auth system
redis_client = get_redis_client()

# Ensure responses are decoded to strings (if not already configured)
if not getattr(redis_client, 'decode_responses', False):
    logger.warning("Creating new Redis client with decode_responses=True")
    # Get connection details from existing client
    connection_pool = redis_client.connection_pool
    connection_kwargs = connection_pool.connection_kwargs.copy()
    connection_kwargs['decode_responses'] = True
    
    # Create a new client with the same connection details plus decode_responses
    redis_client = redis.Redis(**connection_kwargs)

def is_email_sent(emp_id):
    return redis_client.sismember(EMAIL_SET_KEY, emp_id)

def mark_email_sent(emp_id):
   
    # Add to the set
    redis_client.sadd(EMAIL_SET_KEY, emp_id)
    
    member_key = f"{EMAIL_SET_KEY}:{emp_id}"
    redis_client.set(member_key, '1', ex=EMAIL_TTL_SECONDS)
    
    # Set up expiry callback
    redis_client.set(
        name=member_key,
        value='1',
        ex=EMAIL_TTL_SECONDS
    )



class AsyncScheduler(task_pb2_grpc.SchedulerServicer):
    async def ScheduleMeet(self, request, context):
        empId = request.empid
        if(is_email_sent(empId)):
            logger.info(f"Email already sent to {empId}. Not rescheduling.")
            return task_pb2.MeetResponse(success=False, job_id=None)
        
        scheduled_time = datetime.fromtimestamp(request.timestamp, tz=timezone.utc)

        job = addMailToQueue.apply_async(
            args=[ request.empid,request.emailID, request.message, request.empName],
            eta=scheduled_time
        )

        logger.info(f"Scheduled email to {request.emailID} at {scheduled_time} with job_id: {job.id}")
        mark_email_sent(empId)
        return task_pb2.MeetResponse(success=True, job_id=job.id)

async def serve():
    server = aio.server(
        options=[
            ('grpc.so_reuseport', 1),
            ('grpc.max_concurrent_streams', 1000),
            ('grpc.max_send_message_length', 100*1024*1024),
            ('grpc.max_receive_message_length', 100*1024*1024)
        ]
    )
    task_pb2_grpc.add_SchedulerServicer_to_server(AsyncScheduler(), server)
    server.add_insecure_port('[::]:50051')

    logger.info("Starting gRPC server on port 50051")
    await server.start()

    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down gRPC server")
        await server.stop(5)

if __name__ == '__main__':
    asyncio.run(serve())