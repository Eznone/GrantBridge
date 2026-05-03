"""
Rate limiting middleware for authentication endpoints.
"""

import time
import logging
from typing import Dict, Tuple
from django.core.cache import cache
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)


class RateLimitMiddleware:
    """
    Simple rate limiting middleware for authentication endpoints.
    Uses Django cache to track request counts.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Rate limit configuration
        self.limits = {
            "/api/auth/login": (5, 300),  # 5 requests per 5 minutes
            "/api/auth/register": (3, 3600),  # 3 requests per hour
            "/api/auth/refresh": (10, 300),  # 10 requests per 5 minutes
            "/api/auth/change-password": (3, 3600),  # 3 per hour
        }

    def __call__(self, request):
        # Check if path should be rate limited
        path = request.path

        if path in self.limits:
            # Get client identifier (IP address)
            client_ip = self.get_client_ip(request)

            # Check rate limit
            is_allowed, retry_after = self.check_rate_limit(client_ip, path)

            if not is_allowed:
                return JsonResponse(
                    {
                        "detail": "Rate limit exceeded. Please try again later.",
                        "retry_after": retry_after,
                    },
                    status=429,
                )

        response = self.get_response(request)
        return response

    def get_client_ip(self, request) -> str:
        """
        Get client IP address from request.

        Args:
            request: Django request object

        Returns:
            Client IP address
        """
        # Check for forwarded IP (behind proxy)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")

        return ip

    def check_rate_limit(self, client_ip: str, path: str) -> Tuple[bool, int]:
        """
        Check if request is within rate limit.

        Args:
            client_ip: Client IP address
            path: Request path

        Returns:
            Tuple of (is_allowed, retry_after_seconds)
        """
        max_requests, window = self.limits.get(path, (100, 60))

        # Create cache key
        cache_key = f"rate_limit:{path}:{client_ip}"

        # Get current request data
        request_data = cache.get(cache_key)

        current_time = int(time.time())

        if request_data is None:
            # First request
            cache.set(cache_key, {"count": 1, "start_time": current_time}, window)
            return True, 0

        # Check if window has expired
        if current_time - request_data["start_time"] >= window:
            # Reset window
            cache.set(cache_key, {"count": 1, "start_time": current_time}, window)
            return True, 0

        # Check if limit exceeded
        if request_data["count"] >= max_requests:
            # Calculate retry after
            retry_after = window - (current_time - request_data["start_time"])
            return False, retry_after

        # Increment count
        request_data["count"] += 1
        cache.set(cache_key, request_data, window)

        return True, 0


class IPWhitelistMiddleware:
    """
    Middleware to whitelist specific IP addresses from rate limiting.
    Useful for internal services or trusted clients.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.whitelist = getattr(settings, "RATE_LIMIT_WHITELIST", [])

    def __call__(self, request):
        # Check if IP is whitelisted
        client_ip = self.get_client_ip(request)

        if client_ip in self.whitelist:
            # Add marker to skip rate limiting
            request.rate_limit_whitelisted = True

        response = self.get_response(request)
        return response

    def get_client_ip(self, request) -> str:
        """Get client IP address."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


# Made with Bob
