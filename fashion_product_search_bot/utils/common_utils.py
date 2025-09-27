# utils/filter_utils.py
import re

def apply_filters(df, filters):
    if "price_max" in filters:
        df = df[df["price"] <= filters["price_max"]]
    if "price_min" in filters:
        df = df[df["price"] >= filters["price_min"]]
    if "rating_min" in filters:
        df = df[df["avg_rating"] >= filters["rating_min"]]
    if "discount_min" in filters and "discount_percentage" in df.columns:
        df = df[df["discount_percentage"] >= filters["discount_min"]]
    if "gender" in filters and "gender" in df.columns:
        df = df[df["gender"].str.lower().str.contains(filters["gender"].lower())]
    if "brand" in filters:
        df = df[df["brand"].str.lower() == filters["brand"].lower()]
    return df


def format_agent_response(text: str) -> str:
    """
    Format agent output if it includes quoted items like product names.
    Otherwise, return raw response.
    """
    # Match any values inside single or double quotes
    items = re.findall(r"[\"']([^\"']+)[\"']", text)

    if items and len(items) > 1:
        formatted = "### 🔎 Results\n"
        for i, item in enumerate(items, 1):
            formatted += f"- **{i}. {item}**\n"
        return formatted

    # Optional: Convert numbered inline list to bullets
    numbered_items = re.findall(r"\d+\.\s+([^\n]+)", text)
    if numbered_items:
        formatted = "### 🔎 Results\n"
        for i, item in enumerate(numbered_items, 1):
            formatted += f"- **{i}. {item.strip()}**\n"
        return formatted

    # If nothing matched, return raw response
    return text
