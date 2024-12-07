import asyncio
import traceback
from typing import Optional
import httpx

from env import Env
from mesh.endpoints import Endpoints
from telegram.client import TGClient
from telegram.platform import Platform
from fake_useragent.fake import UserAgent
from utils.loggy import logger


class Mesh:
    def __init__(
        self,
        peer_id: str,
        http_timeout: float = 120,
        platform: Platform = Platform.ANDROID,
    ) -> None:
        self.peer_id: str = peer_id
        self.user_id: Optional[str] = None
        self.client: httpx.AsyncClient = httpx.AsyncClient(
            timeout=http_timeout,
            headers={"User-Agent": UserAgent(os=platform.value).random},
        )

    async def _post(
        self, url: str, data: Optional[dict] = None, json: Optional[dict] = None
    ) -> Optional[httpx.Response]:
        try:
            return await self.client.post(url, data=data, json=json)
        except httpx.HTTPStatusError as e:
            logger.error(
                f"Request to {url} failed with status {e.response.status_code}"
            )
            logger.error(traceback.print_exc())
        except Exception as e:
            logger.error(f"Request to {url} failed: {str(e)}")
            logger.error(traceback.print_exc())

    async def _get(self, url: str) -> Optional[httpx.Response]:
        try:
            return await self.client.get(url)
        except httpx.HTTPStatusError as e:
            logger.error(
                f"GET request to {url} failed with status {e.response.status_code}"
            )
        except Exception as e:
            logger.error(f"GET request to {url} failed: {str(e)}")
            logger.error(traceback.print_exc())

    async def login(self):
        tg_client = TGClient()
        query: str = await tg_client.get_query_string(self.peer_id, short_name="app")
        self.client.headers["authorization"] = f"tma {query}"
        response: Optional[httpx.Response] = await self._post(
            Endpoints.LOGIN_URL, json={"referral_code": Env.REF_ID}
        )

        if not response:
            logger.error("Unable to login")
            logger.error(traceback.print_exc())
            return False

        token = response.json().get("access_token")
        if not token:
            logger.error("Unable to obtain access token")
            logger.error("Unable to login")
            logger.error(traceback.print_exc())
            logger.error(response.json())
            return False

        if response.status_code == 201:
            self.client.headers["Authorization"] = f"Bearer {token}"
            logger.success("Logged in successfully")
            self.user_id = await tg_client.get_userid()
            await asyncio.sleep(10)
            return True
        return False

    async def estimate(self) -> Optional[dict]:
        if not self.user_id:
            logger.error("Unable to estimate without user ID")
            return
        response: Optional[httpx.Response] = await self._post(
            Endpoints.ESTIMATE_URL, json={"unique_id": self.user_id}
        )

        if not response:
            logger.error("Unable to estimate")
            logger.error(traceback.print_exc())
            return

        rewards = response.json()
        if not rewards:
            logger.error("Unable to get estimate")
            logger.error(traceback.print_exc())
            logger.error(response.json())
            return
        return rewards

    async def claim(self):
        if not self.user_id:
            logger.error("Unable to claim without user ID")
            return
        response: Optional[httpx.Response] = await self._post(
            Endpoints.CLAIM, json={"unique_id": self.user_id}
        )

        if not response:
            logger.error("Unable to claim rewards")
            logger.error(traceback.print_exc())
            return

        rewards = response.json()
        if not rewards:
            logger.error("Unable to claim rewards")
            logger.error(traceback.print_exc())
            logger.error(response.json())
            return
        return rewards
