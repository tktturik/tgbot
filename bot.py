
from handlers import callbacks,commands, messags
from instance import app
import asyncio
from fastapi import FastAPI
from backend.api.routers import token,users
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

BASE_API = os.getenv('BASE_API')

def setup_bot_handlers():

    #MessagesHandlers

    app.add_handler(messags.contact_handler)
    app.add_handler(messags.darsik_messages_handler)
    app.add_handler(messags.messages_handler)


    #CommandsHandlers

    app.add_handler(commands.start_handler)
    app.add_handler(commands.gift_handler)
    app.add_handler(commands.but_handler)
    app.add_handler(commands.request_contact_handler)



    #CallBackHandlers

    app.add_handler(callbacks.callback_handler)


def create_api():
    fastApiApp = FastAPI(root_path="/api")
    fastApiApp.include_router(token.router)
    fastApiApp.include_router(users.router)

    return fastApiApp

async def start():
    setup_bot_handlers()
    api_app = create_api()
    config = uvicorn.Config(api_app, host=f"{BASE_API}", port=9000, log_level="info")
    server = uvicorn.Server(config)
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    server_task = asyncio.create_task(server.serve())

    try:
        await server_task
    except asyncio.CancelledError:
        pass
    finally:
        await app.updater.stop()
        await app.stop()
        print("Бот и FastAPI сервер остановлены")

if __name__ == "__main__":
    asyncio.run(start())
