import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi import HTTPException

from services.rate_limiter import rate_limit


def make_request(host="127.0.0.1"):
    request = MagicMock()
    request.client.host = host
    return request


# ── Авторизований користувач ──────────────────────────────────────────

@pytest.mark.asyncio
async def test_authenticated_under_limit():
    """Авторизований юзер ще не досяг ліміту — запит проходить (200)."""
    mock_r = AsyncMock()
    mock_r.zcard.return_value = 5  # limit = 10, ще є місце

    with patch("services.rate_limiter.r", mock_r):
        await rate_limit(make_request(), user_id="testuser")


@pytest.mark.asyncio
async def test_authenticated_over_limit():
    """Авторизований юзер досяг ліміту — повертається 429."""
    mock_r = AsyncMock()
    mock_r.zcard.return_value = 10  # limit = 10, вичерпано

    with patch("services.rate_limiter.r", mock_r):
        with pytest.raises(HTTPException) as exc_info:
            await rate_limit(make_request(), user_id="testuser")
        assert exc_info.value.status_code == 429


# ── Анонімний користувач ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_anonymous_under_limit():
    """Анонімний юзер ще не досяг ліміту — запит проходить (200)."""
    mock_r = AsyncMock()
    mock_r.zcard.return_value = 1  # limit = 2, ще є місце

    with patch("services.rate_limiter.r", mock_r):
        await rate_limit(make_request(), user_id=None)


@pytest.mark.asyncio
async def test_anonymous_over_limit():
    """Анонімний юзер досяг ліміту — повертається 429."""
    mock_r = AsyncMock()
    mock_r.zcard.return_value = 2  # limit = 2, вичерпано

    with patch("services.rate_limiter.r", mock_r):
        with pytest.raises(HTTPException) as exc_info:
            await rate_limit(make_request(), user_id=None)
        assert exc_info.value.status_code == 429