from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from auth.auth_bearer import JWTBearer
from services.integrations import get_github_repos

router = APIRouter()

# Request model for GitHub integration
class GitHubIntegrationRequest(BaseModel):
    username: str
    token: str = None  # Optional personal access token

@router.post("/github", dependencies=[Depends(JWTBearer())])
async def github_integration(request: GitHubIntegrationRequest):
    """
    Retrieve GitHub repositories for the given username.
    Optionally, you can provide a token for authenticated access.
    """
    try:
        repos = get_github_repos(request.username, request.token)
        return {"repositories": repos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
