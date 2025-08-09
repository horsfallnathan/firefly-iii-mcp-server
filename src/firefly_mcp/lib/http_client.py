import os
import httpx
import logging

def create_client() -> httpx.Client:
    """Create HTTP client with appropriate SSL settings for development."""
    
    api_url = os.environ.get("FIREFLY_API_URL", "https://firefly.dev.nlocal/api/v1")
    api_token = os.environ.get("FIREFLY_API_TOKEN", "")
    
    # Only include Authorization header if token is not empty
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    if api_token and api_token.strip():
        headers["Authorization"] = f"Bearer {api_token}"
    

    return httpx.Client(
        base_url=api_url, 
        headers=headers,
        verify=verify_ssl(),
        timeout=30.0
    )

def verify_ssl() -> bool:
    """Check if SSL verification is enabled."""
    disable_ssl_verify = os.environ.get('FIREFLY_DISABLE_SSL_VERIFY', 'false').lower()
    if disable_ssl_verify not in ['true', 'false']:
        logging.warning("FIREFLY_DISABLE_SSL_VERIFY environment variable must be 'true' or 'false'. Defaulting to 'false'.")
        disable_ssl_verify = 'false'

    return disable_ssl_verify == 'true'


client = create_client()