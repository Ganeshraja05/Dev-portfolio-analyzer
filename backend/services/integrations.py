import requests
from fastapi import HTTPException

def get_github_repos(username: str, token: str = None) -> dict:
    """
    Fetch GitHub repositories for a given username.
    Optionally uses a token for authenticated requests.
    """
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    url = f"https://api.github.com/users/Ganeshraja05/repos"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch GitHub repositories")
    return response.json()
