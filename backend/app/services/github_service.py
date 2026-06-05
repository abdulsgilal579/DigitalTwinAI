import httpx

from app.config import GITHUB_USERNAME, GITHUB_TOKEN

GITHUB_API_URL = "https://api.github.com"


async def fetch_repositories():
    if not GITHUB_USERNAME:
        raise ValueError("GITHUB_USERNAME is missing. Add it to your .env file.")

    headers = {}

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    url = f"{GITHUB_API_URL}/users/{GITHUB_USERNAME}/repos"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=headers,
            params={
                "sort": "updated",
                "direction": "desc",
                "per_page": 20,
            },
        )

        response.raise_for_status()
        repositories = response.json()

    return [
        {
            "name": repo["name"],
            "description": repo["description"],
            "url": repo["html_url"],
            "language": repo["language"],
            "stars": repo["stargazers_count"],
            "updated_at": repo["updated_at"],
        }
        for repo in repositories
    ]