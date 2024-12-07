from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class Endpoints:
    _API_URL: Final[str] = "https://api.meshchain.ai/meshmain"
    LOGIN_URL: Final[str] = f"{_API_URL}/auth/telegram-miniapp-signin"
    ESTIMATE_URL: Final[str] = f"{_API_URL}/rewards/estimate"
    CLAIM: Final[str] = f"{_API_URL}/rewards/claim"


# class Endpoints:
#     LOGIN_URL: Final[str] = (
#         "https://api.meshchain.ai/meshmain/auth/telegram-miniapp-signin"
#     )
#     ESTIMATE_URL: Final[str] = "https://api.meshchain.ai/meshmain/rewards/estimate"
#     CLAIM: Final[str] = "https://api.meshchain.ai/meshmain/rewards/claim"
