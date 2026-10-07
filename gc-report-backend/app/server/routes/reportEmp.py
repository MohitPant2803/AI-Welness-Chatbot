import logging
from fastapi import APIRouter
from fastapi.responses import FileResponse
from datetime import datetime
from bson import ObjectId
from server.models.admindbemp import Admindbemp
from utils.report_one_emp import create_report

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

admindbemp_router = APIRouter()

def create_response(success: bool, message: str, data=None, code=200):
    return {"success": success, "message": message, "data": data, "code": code}

def custom_serializer(obj):
    """Handle MongoDB ObjectId, datetime, and custom class serialization"""
    if isinstance(obj, ObjectId):
        return {"$oid": str(obj)}
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, "dict"):
        return obj.dict()
    elif hasattr(obj, "__dict__"):
        return {k: custom_serializer(v) for k, v in obj.__dict__.items()}
    return str(obj)

@admindbemp_router.get("/{empid}")
async def download_emp_report(empid: str):
    try:
        admindb_data = await Admindbemp.find_one(Admindbemp.briefUserDetails.empid == empid)
        if not admindb_data:
            logger.warning(f"AdminDB data not found for empid: {empid}")
            return create_response(False, "AdminDB data not found", code=404)
        
        processed_data = custom_serializer(admindb_data)
        if "_id" in processed_data:
            processed_data["_id"] = {"$oid": str(processed_data["_id"])}
        
        # Generate the PDF file and get the file path
        pdf_path = create_report(processed_data, "ReportEmp.pdf")
        
        logger.info(f"AdminDB data retrieved successfully for empid: {empid}")
        # Return the PDF as a downloadable file
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename="ReportEmp.pdf",
            headers={"Content-Disposition": "attachment; filename=ReportEmp.pdf"}
        )
    except Exception as e:
        logger.error(f"Error retrieving admin DB for empid {empid}: {str(e)}", exc_info=True)
        return create_response(False, "Internal Server Error", code=500)
