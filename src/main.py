import asyncio
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application
from config import config
from models import *
from utils import setup_logger, get_logger
from command_handlers import start_command_handler, stop_command_handler

setup_logger(
    root_path=config.project_root_path,
    service_name="flare_server",
    log_level=config.log_level,
    logfire_token=config.logfire_token,
    logfire_env=config.logfire_env,
)
logger = get_logger()

application = (
    Application.builder()
    .updater(None)
    .token(config.telegram_bot_token)
    .read_timeout(7)
    .get_updates_read_timeout(42)
    .build()
)
application.add_handler(start_command_handler)
application.add_handler(stop_command_handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await application.bot.setWebhook(
        url=f"{config.public_url}/tg_webhook",
    )
    async with application:
        await application.start()
        yield
        await application.stop()

app = FastAPI(
    title="🎇 Flare server application",
    description="Flare — Real-time alert relay from Logfire to Telegram chats, groups, and channels.",
    lifespan=lifespan
)


@app.post("/tg_webhook")
async def process_update(request: Request):
    try:
        logger.info("Received update from Telegram")
        req = await request.json()
        update = Update.de_json(req, application.bot)
        await application.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error processing Telegram update: {e}")
        return {"status": "error", "message": "Failed to process update"}


@app.get("/health", tags=["Health"])
async def health_check():
    logger.info("Health check endpoint called.")
    return {"status": "ok"}


@app.post("/alert", tags = ["Alerts"])
async def receive_alert(logfire_alert: dict):
    try:
        logfire_alert = LogfireAlertPayload(**logfire_alert)

        logger.info(f"Received alert: {logfire_alert}")
        chat_id = config.chat_id
        await application.bot.send_message(
            chat_id=chat_id,
            text=logfire_alert.to_markdown_message(),
            parse_mode="MarkdownV2",
        )
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Invalid alert payload: {e}")
        return {"status": "error", "message": "Invalid alert payload"}


async def main():
    # config and run uvicorn server
    server_config = uvicorn.Config(
        app,
        host=config.service_host,
        port=config.service_port,
        log_level=config.log_level.lower()
    )
    uvicorn_server = uvicorn.Server(server_config)
    await uvicorn_server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.error("Service stopped by user.")
    except Exception as e:
        logger.critical(f"An error occurred while starting the service: {e}")