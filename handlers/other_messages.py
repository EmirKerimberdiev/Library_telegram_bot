from aiogram import Router, types
from aiogram.filters.command import Command


echo_router = Router()

@echo_router.message()
async def echo_handler(message):
    text = message.text
    await message.reply(text)