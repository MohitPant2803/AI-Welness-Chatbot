from beanie import Document

class Meet(Document):
    meetUrl: str

    class Settings:
        collection = "meets"
        indexes = [
            "meetUrl"
        ]

    class Config:
        json_schema_extra = {
            "example": {
                "meetUrl": "https://example.com/meet12345"
            }
        }