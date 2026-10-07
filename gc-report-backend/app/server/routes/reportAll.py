from fastapi.responses import FileResponse
from fastapi import APIRouter
import logging
from datetime import datetime
from bson import ObjectId
from utils.report_all import create_report
from server.models.admindb import Admindb

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
admindball_router = APIRouter()

def create_response(success: bool, message: str, data=None, code=200):
    return {"success": success, "message": message, "data": data, "code": code}

def custom_serializer(obj):
    if isinstance(obj, ObjectId):
        return {"$oid": str(obj)}
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, "dict"):
        return obj.dict()
    elif hasattr(obj, "__dict__"):
        return {k: custom_serializer(v) for k, v in obj.__dict__.items()}
    return str(obj)

@admindball_router.get("")
async def download_pdf():
    try:
        admindb_data = await Admindb.find_one({})
        if not admindb_data:
            logger.warning("AdminDB all data not found")
            return create_response(False, "AdminDB all data not found", code=404)
        
        processed_data = custom_serializer(admindb_data)
        if "_id" in processed_data:
            processed_data["_id"] = {"$oid": str(processed_data["_id"])}
        
        logger.info("AdminDB all data retrieved successfully")
        # Generate the PDF. This function returns the path to the PDF file.
        pdf_path = create_report(processed_data, "ReportAll.pdf")
        
        # Return the PDF as a downloadable file
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename="ReportAll.pdf",
            headers={"Content-Disposition": "attachment; filename=ReportAll.pdf"}
        )
    except Exception as e:
        logger.error(f"Error retrieving admin DB all: {str(e)}", exc_info=True)
        return create_response(False, "Internal Server Error", code=500)
