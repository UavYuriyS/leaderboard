from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from config import settings

# Define the API Key headers
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
admin_api_key_header = APIKeyHeader(name="X-Admin-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Verify that the provided API key matches the configured key.

    Args:
        api_key: API key from the X-API-Key header

    Returns:
        The API key if valid

    Raises:
        HTTPException: If API key is missing or invalid
    """
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key. Please provide X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    if api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key. Access denied.",
        )

    return api_key


async def verify_admin_api_key(admin_api_key: str = Security(admin_api_key_header)):
    """
    Verify that the provided admin API key matches the configured admin key.

    This is used for privileged operations like deleting users.

    Args:
        admin_api_key: Admin API key from the X-Admin-API-Key header

    Returns:
        The admin API key if valid

    Raises:
        HTTPException: If admin API key is missing or invalid
    """
    if admin_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Admin API Key. Please provide X-Admin-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    if admin_api_key != settings.admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Admin API Key. Access denied. Admin privileges required.",
        )

    return admin_api_key
