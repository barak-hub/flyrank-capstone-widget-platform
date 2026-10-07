from typing import Optional


def provider_a(ip_address: str) -> Optional[dict]:
    """
    Geo Provider A.

    In the real system this represents the primary geo provider.
    Returning None means the provider failed or had no result.
    """
    return {
        "country": "Uganda",
        "city": "Kampala",
        "latitude": 0.3476,
        "longitude": 32.5825,
        "provider": "provider-a",
    }


def provider_b(ip_address: str) -> Optional[dict]:
    """
    Geo Provider B.

    This is the fallback provider.
    """
    return {
        "country": "Uganda",
        "city": "Kampala",
        "latitude": 0.3476,
        "longitude": 32.5825,
        "provider": "provider-b",
    }


def get_geo_from_ip(ip_address: str) -> Optional[dict]:
    """
    Try Provider A first.

    If Provider A fails, use Provider B.
    If both providers fail, return None.
    """

    # Provider A
    try:
        result = provider_a(ip_address)
        if result:
            return result
    except Exception:
        pass

    # Provider B — fallback
    try:
        result = provider_b(ip_address)
        if result:
            return result
    except Exception:
        pass

    # Both providers failed
    return None