import asyncio
from contextlib import suppress
from datetime import timedelta
import random
import time
import traceback
from mesh.mesh import Mesh
from env import Env
from utils.dt import human_readable
from utils.loggy import logger


class MeshChainBot:
    def format_time(self, seconds: int) -> str:
        hours: int = seconds // 3600
        minutes: int = (seconds % 3600) // 60
        secs: int = seconds % 60
        return f"{hours} hour(s), {minutes} minute(s), {secs} second(s)"

    async def sleeper(self, time_elapsed_sec: int):
        refill_time_in_sec: int = 60 * 60 * 2
        time_left: int = refill_time_in_sec - time_elapsed_sec
        if time_left > 0:
            formatted_time: str = self.format_time(time_left)
            logger.info("Refill is not ready yet!")
            logger.info(f"Time left: {formatted_time}")
            logger.info(f"Sleeping for {time_left} seconds...")
            await asyncio.sleep(time_left)
            random_del = random.randint(60, 120)
            logger.info(f"Added extra random {random_del // 60} minutes sleep")
            await asyncio.sleep(random_del)

        logger.info("No need to wait, refill is ready!")

    async def main(self):
        sleep_delay = Env.SLEEP_DELAY_MINUTES
        logger.info(f"SLEEP DELAY SET TO {sleep_delay} MINUTES")
        while True:
            try:
                mesh = Mesh("meshchain_bot")
                is_logged = await mesh.login()
                if not is_logged:
                    return
                estimate_data = await mesh.estimate()
                if estimate_data:
                    if not estimate_data["filled"]:
                        await self.sleeper(estimate_data["time_elapsed_sec"])
                    await mesh.claim()

                rest_period = 60 * sleep_delay
                logger.info(
                    f"Lets take a rest for {human_readable(timedelta(seconds=rest_period))}"
                )
                await asyncio.sleep(rest_period)
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                logger.error(traceback.format_exc())
                logger.info("Let's take a 10 minutes break.")
                await asyncio.sleep(60 * 10)

    def run(self):
        while True:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.main())
            except Exception as e:
                logger.error(traceback.format_exc())
                logger.error(f"Restarting event loop due to error: {e}")
            finally:
                with suppress(Exception):
                    loop.close()
                logger.info("Restarting the main loop...")
                time.sleep(10)


if __name__ == "__main__":
    MeshChainBot().run()
