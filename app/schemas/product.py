from pydantic import BaseModel, HttpUrl, Field
from typing import Dict, Any, Optional

class ProductScanRequest(BaseModel):
    url: HttpUrl = Field(..., description="The URL of the e-commerce product page to scan.")

class ProductScanResponse(BaseModel):
    status: str = Field(..., description="Status of the scan (success/error).")
    data: Optional[Dict[str, Any]] = Field(None, description="Extracted product data.")
    message: Optional[str] = Field(None, description="Error message if any.")
