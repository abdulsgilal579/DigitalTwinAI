import httpx

from app.config import ELEVENLABS_AGENT_ID, ELEVENLABS_API_KEY

ELEVENLABS_SIGNED_URL_ENDPOINT = (
    "https://api.elevenlabs.io/v1/convai/conversation/get-signed-url"
)


async def get_elevenlabs_signed_url():
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY is missing. Add it to your .env file.")

    if not ELEVENLABS_AGENT_ID:
        raise ValueError("ELEVENLABS_AGENT_ID is missing. Add it to your .env file.")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            ELEVENLABS_SIGNED_URL_ENDPOINT,
            headers={"xi-api-key": ELEVENLABS_API_KEY},
            params={"agent_id": ELEVENLABS_AGENT_ID},
        )

        response.raise_for_status()
        data = response.json()

    return data["signed_url"]