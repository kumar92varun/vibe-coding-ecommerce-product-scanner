from app.core.attributes_conf import ATTRIBUTE_PROMPTS

# Mapping from final JSON keys to the keys used in attributes_conf.py
# This ensures decoupling between internal logic and external API response structure.
STRUCTURE_MAPPING = {
    "name": "product_name",
    "price": {
        "current": "current_price",
        "original": "original_price",
        "currency": "currency"
    },
    "details": {
        "description": "description",
        "availability": "availability",
        "features": "features",
        "specifications": "tech_specs"
    },
    "social_proof": {
        "rating": "rating",
        "reviews": "review_count"
    },
    "media": {
        "main_image": "main_image_url"
    }
}
