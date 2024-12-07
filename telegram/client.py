from pyrogram.client import Client
from pyrogram.raw.types.input_bot_app_short_name import InputBotAppShortName
from pyrogram.raw.functions.messages.request_app_web_view import RequestAppWebView
from pyrogram.raw.types.input_peer_user import InputPeerUser
from pyrogram.raw.types.app_web_view_result_url import AppWebViewResultUrl
from pyrogram.errors.exceptions import UsernameNotOccupied

from env import Env

import os
import re
from typing import Final
from telegram.platform import Platform
from utils.loggy import logger
import urllib.parse


class TGClient(Client):
    WORKDIR: Final[str] = "sessions/"

    def __init__(self) -> None:
        self.create_workdir()
        super().__init__(
            name=Env.SESSION_NAME,
            api_id=Env.API_ID,
            api_hash=Env.API_HASH,
            workdir=self.WORKDIR,
            phone_number=Env.PHONE,
        )

    def create_workdir(self) -> None:
        os.makedirs(self.WORKDIR, exist_ok=True)

    async def get_userid(self) -> str:
        async with self:
            user = await self.get_me()
            return str(user.id)

    async def get_query_string(
        self,
        peer_id: str,
        short_name: str,
        platform: Platform = Platform.ANDROID,
    ) -> str:
        try:
            async with self:
                user = await self.get_me()
                username = user.username
                logger.success(f"Logged in as @{username}")

                try:
                    bot_peer: InputPeerUser = await self.resolve_peer(peer_id)  # type: ignore
                except UsernameNotOccupied as e:
                    raise e

                bot_app: InputBotAppShortName = InputBotAppShortName(
                    bot_id=bot_peer,  # type: ignore
                    short_name=short_name,
                )

                web_view_request: RequestAppWebView = RequestAppWebView(
                    peer=bot_peer,  # type: ignore
                    app=bot_app,  # type: ignore
                    platform=platform.value,
                    write_allowed=True,
                    start_param=Env.REF_ID,
                )

                web_view: AppWebViewResultUrl = await self.invoke(web_view_request)

                match = re.search(r"tgWebAppData=([^&]+)", web_view.url)
                query = match.group(1) if match else ""
                query = urllib.parse.unquote(query)

                if not query:
                    raise ValueError("Could not find query string")
                return query

        except Exception as e:
            logger.error(f"Query Retrieval Failed - Reason: {e}")
            raise e
