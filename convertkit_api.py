# File: convertkit_api.py
import requests
from typing import Optional

def subscribe_user_to_convertkit(email: str, api_key: str, form_id: str) -> bool:
    """
    Subscribe a user to a ConvertKit form via API.

    Args:
        email: Subscriber email address.
        api_key: ConvertKit API key.
        form_id: ConvertKit form ID to subscribe to.

    Returns:
        True if subscription succeeded (status 200), else False.
    """
    url = f"https://api.convertkit.com/v3/forms/{form_id}/subscribe"
    payload = {"api_key": api_key, "email": email}
    try:
        resp = requests.post(url, json=payload)
        return resp.status_code == 200
    except requests.RequestException:
        return False

