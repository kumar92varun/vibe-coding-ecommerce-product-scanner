from fastapi import APIRouter, HTTPException
from app.schemas.product import ProductScanRequest, ProductScanResponse
from app.services.browser_service import scrape_product_page
from app.services.ai_service import extract_product_data
from app.core.structure_conf import STRUCTURE_MAPPING

router = APIRouter()

def map_data(raw_data: dict) -> dict:
    """
    Maps the raw data extracted by Gemini to the final structure defined in structure_conf.py.
    """
    mapped_data = {}
    
    for final_key, mapping_value in STRUCTURE_MAPPING.items():
        if isinstance(mapping_value, dict):
            # Nested structure
            mapped_data[final_key] = {}
            for sub_key, source_key in mapping_value.items():
                mapped_data[final_key][sub_key] = raw_data.get(source_key, "not-identified")
        else:
            # Direct mapping
            mapped_data[final_key] = raw_data.get(mapping_value, "not-identified")
            
    return mapped_data

@router.post("/scan", response_model=ProductScanResponse)
async def scan_product(request: ProductScanRequest):
    """
    Scans a product page and extracts structured data.
    """
    url = str(request.url)
    
    # 1. Scrape the page content
    print(f"Scraping {url}...")
    content, error_msg = await scrape_product_page(url)
    
    if error_msg:
        raise HTTPException(status_code=400, detail=error_msg)
        
    # 2. Extract data using AI
    print("Extracting data with AI...")
    raw_data = await extract_product_data(content)
    
    if "error" in raw_data:
        return ProductScanResponse(
            status="error",
            message=f"AI Extraction failed: {raw_data['error']}"
        )
        
    # 3. Map to final structure
    final_data = map_data(raw_data)
    
    return ProductScanResponse(
        status="success",
        data=final_data
    )
