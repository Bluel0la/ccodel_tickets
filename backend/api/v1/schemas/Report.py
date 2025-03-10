from pydantic import BaseModel
from typing import Optional

class ReportGenerateSchema(BaseModel):
    topic: str
    outline: Optional[list[str]] = []

class ReportImproveSchema(BaseModel):
    report_id: int
    content: str

class ReportResponseSchema(BaseModel):
    id: int
    topic: str
    content: str
    created_at: str
