import json
from typing import Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from app.core.config import settings
from app.core.attributes_conf import ATTRIBUTE_PROMPTS

# Initialize the Gemini Pro model
# We set temperature to 0 for deterministic extraction
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0.0
)

def construct_prompt(content: str) -> str:
    """
    Constructs the prompt for Gemini based on the configured attributes.
    """
    attributes_str = "\n".join([f"- {key}: {desc}" for key, desc in ATTRIBUTE_PROMPTS.items()])
    
    prompt = f"""
    You are an expert e-commerce data extraction assistant.
    Your task is to extract specific product attributes from the provided raw text content of a product page.
    
    Here are the attributes you need to extract:
    {attributes_str}
    
    Instructions:
    1.  Examine the text content carefully.
    2.  For each attribute, try to find the corresponding value.
    3.  If an attribute is found, extract its value accurately.
    4.  If an attribute is NOT found or unclear, use the exact string "not-identified".
    5.  For 'features' and 'tech_specs', capture them as a list of strings if possible, or a single string if not clearly listed.
    6.  Return the result as a VALID JSON object where keys are the attribute names listed above.
    7.  Do NOT include any markdown formatting (like ```json), just the raw JSON string.
    
    Raw Text Content:
    {content[:15000]}  # Truncate to avoid context window limits if content is huge
    
    JSON Output:
    """
    return prompt

async def extract_product_data(content: str) -> Dict[str, Any]:
    """
    Extracts structured product data from text content using Gemini.
    """
    if not content:
        return {"error": "No content to extract from."}
    
    prompt_text = construct_prompt(content)
    
    try:
        response = await llm.ainvoke(prompt_text)
        response_content = response.content.strip()
        
        # Clean up potential markdown code blocks if gemini insists on adding them
        if response_content.startswith("```json"):
            response_content = response_content[7:]
        if response_content.endswith("```"):
            response_content = response_content[:-3]
            
        try:
            data = json.loads(response_content)
            return data
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            print(f"Raw Response: {response_content}")
            return {"error": "Failed to parse AI response as JSON", "raw_response": response_content}
            
    except Exception as e:
        print(f"AI Extraction Error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Test logic can be added here
    pass
