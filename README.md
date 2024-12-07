# MeshChainBot

**MeshChainBot** automates claiming points on the Mesh platform every 2 hours.

---

## Features

- **Automated Point Claiming**: Logs into the Mesh platform and claims points every 2 hours.
- **Refill Timer**: Automatically waits until the refill time is ready.
- **Randomized Delays**: Adds a random sleep period to mimic realistic activity.
- **Error Handling**: Logs errors and automatically restarts.
- **Customizable Delays**: Adjust the delay between tasks with an environment variable.

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Praveensenpai/MeshChainBot.git
cd MeshChainBot
```

### 2. Install `uv` Package Manager

**Windows:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/macOS:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Sync Dependencies with `uv`

```bash
uv sync
```

### 4. Configure `.env`

Create a `.env` file in the project directory and set the following variables:

```plaintext
API_ID=your_api_id
API_HASH=your_api_hash
REF_ID=T_844807085
SESSION_NAME=mesh
PHONE=+91
SLEEP_DELAY_MINUTES=1
```

| Key                   | Description                                   |
| --------------------- | --------------------------------------------- |
| `API_ID`              | Your Telegram API ID                          |
| `API_HASH`            | Your Telegram API Hash                        |
| `REF_ID`              | Referral ID from the referral link            |
| `SESSION_NAME`        | Session name (e.g., `mesh`)                   |
| `PHONE`               | Your phone number                             |
| `SLEEP_DELAY_MINUTES` | Random Delay between task cycles (in minutes) |

---

## Running the Bot

To run the bot, simply execute the following command:

```bash
uv run main.py
```

The bot will log in, check for points to claim, and repeat the process every 2 hours, sleeping until the next available refill.

---

## Getting Your Telegram API ID and Hash

To obtain the **API ID** and **API Hash** for Telegram, follow these steps:

1. **Log in to Telegram**: Use the official [Telegram Web](https://web.telegram.org/) or app to log in to your account.
2. **Access the Telegram Developer Portal**:
   - Go to [https://my.telegram.org](https://my.telegram.org) and sign in with your Telegram credentials.
3. **Create a New Application**:
   - After logging in, click on **API Development Tools**.
   - Choose **Create new application** and fill in the required details (e.g., app name, platform).
4. **Get Your API ID and Hash**:
   - After completion, Telegram will provide an **API ID** and **API Hash**. Copy and paste them into your `.env` file.

These credentials allow your bot to interact with Telegram. Keep them secure and avoid sharing them publicly.

---

## Notes

- **No Proxy**: The bot operates without any proxy settings.
- **Single Session**: Only one active session is supported at a time.
- **Future Enhancements**: A task completion feature will be added in future updates.
