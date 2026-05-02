"""
Main API router for GrantBridge.
Aggregates all app-level routers.
"""

from ninja import NinjaAPI
from ninja.security import HttpBearer
from ninja_jwt.authentication import JWTAuth

# Create main API instance
api = NinjaAPI(
    version='1.0.0',
    title='GrantBridge API',
    description='AI-powered grant management platform API for NGOs',
    docs_url='/docs',
)

# Health check endpoint (no auth required)
@api.get("/health", auth=None, tags=["Health"])
def health_check(request):
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "version": "1.0.0"}

# Import and register routers (will be created as we build the apps)
# These imports will be uncommented as we create each app's API router

# from apps.authentication.api import router as auth_router
# from apps.organizations.api import router as org_router
# from apps.grants.api import router as grants_router
# from apps.proposals.api import router as proposals_router
# from apps.matching.api import router as matching_router
# from apps.ai.api import router as ai_router
# from apps.core.api import router as core_router

# Register routers
# api.add_router('/auth/', auth_router, tags=['Authentication'], auth=None)
# api.add_router('/organizations/', org_router, tags=['Organizations'], auth=JWTAuth())
# api.add_router('/grants/', grants_router, tags=['Grants'], auth=JWTAuth())
# api.add_router('/proposals/', proposals_router, tags=['Proposals'], auth=JWTAuth())
# api.add_router('/matching/', matching_router, tags=['Matching'], auth=JWTAuth())
# api.add_router('/ai/', ai_router, tags=['AI Services'], auth=JWTAuth())
# api.add_router('/dashboard/', core_router, tags=['Dashboard'], auth=JWTAuth())

# Made with Bob
