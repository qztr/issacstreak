#!/usr/lib/python3
import os  # for importing env vars for the bot to use
from twitchio.ext import commands
import csv
import urllib.request
from urllib.error import HTTPError
import requests
import threading
import sys
import os
import time
import cryptocode

import os
from dotenv import load_dotenv

load_dotenv()

# SECRET_KEY_API = os.environ.get('SECRET_KEY_API')
KEY_FOR_API = os.getenv("KEY_FOR_API")
SECRET_OAUTH = os.getenv("SECRET_OAUTH")
API_ISAAC = "https://isaac-streak.fun/api_bot"
PATH_TO_CSV = os.getenv("PATH_TO_CSV")

encoded = cryptocode.encrypt("some raw data", KEY_FOR_API)


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=f"{SECRET_OAUTH}",
            prefix=["BibleThump "],
            initial_channels=self.get_channels(),
        )

    # вывод в консоль ник аккаунта бота
    async def event_ready(self):
        print(f"Logged in as | {self.nick}")
        auth_log(f"bot started | {self.nick}")

    # получает ники каналов, к которым нужно подключиться
    def get_channels(self):
        while True:
            try:
                r = requests.get(url=f"{API_ISAAC}/names")
                data = r.json()
                names = []
                for name in data:
                    names.append(name)
                return names

            except:
                auth_log(f"cant connect to remote server  at {API_ISAAC}")
                time.sleep(300)

    # # пишет все сообщения из чата в консоль
    # async def event_message(self, message):
    #     if message.echo:
    #         return
    #     print(message.content)
    #     await self.handle_commands(message)

    # ----------------------------------------------------------------------
    # есть задержка, выставлена не мной, возм-но библиотекой twitchio - яхз
    # пропала задержка .... загадка...
    #
    # КОМАНДЫ
    #
    # ----------------------------------------------------------------------

    # отправить на сервер команду streak <set_streak>
    @commands.command()
    async def streak(self, ctx: commands.Context, arg):
        if ctx.author.is_mod:
            try:
                data = {
                    "last_fall": encoded,
                    "streak": arg,
                    "channel": ctx.message.channel.name,
                }
                r = requests.post(url=f"{API_ISAAC}/streak", json=data, data=data)
                auth_commands_log(
                    f"{ctx.message.channel.name} , streak:{arg} , {r.text}"
                )

                if r.text == "success":
                    await ctx.send(
                        f"Streak updated successfully, {ctx.author.name}! Leaderboard on isaac-streak.fun"
                    )
            except HTTPError as e:
                print(e.code)
            time.sleep(15)

        else:
            await ctx.send(
                f"Only mod can update TearGlove. Leaderboard on isaac-streak.fun"
            )
            time.sleep(15)

    @commands.command()
    async def best(self, ctx: commands.Context, arg):
        if ctx.author.is_mod:
            try:
                data = {
                    "last_fall": encoded,
                    "best": arg,
                    "channel": ctx.message.channel.name,
                }
                r = requests.post(url=f"{API_ISAAC}/best", json=data, data=data)
                auth_commands_log(f"{ctx.message.channel.name} , best:{arg} , {r.text}")

                if r.text == "success":
                    await ctx.send(
                        f"Personal best streak updated successfully, {ctx.author.name}! Leaderboard on isaac-streak.fun"
                    )
            except HTTPError as e:
                print(e.code)
            time.sleep(15)

        else:
            await ctx.send(
                f"Only mod can update TearGlove. Leaderboard on isaac-streak.fun"
            )
            time.sleep(15)

    # отправить на сервер команду category <set_category>
    @commands.command()
    async def category(self, ctx: commands.Context, arg):
        if ctx.author.is_mod:
            try:
                data = {
                    "last_fall": encoded,
                    "category": arg,
                    "channel": ctx.message.channel.name,
                }
                r = requests.post(url=f"{API_ISAAC}/category", json=data, data=data)
                auth_commands_log(
                    f"{ctx.message.channel.name} , category:{arg} , {r.text}"
                )
                if r.text == "success":
                    await ctx.send(
                        f"Category updated successfully, {ctx.author.name}! Leaderboard on isaac-streak.fun"
                    )
            except HTTPError as e:
                print(e.code)
            time.sleep(15)
        else:
            await ctx.send(
                f"Only mod can update TearGlove.  Leaderboard on isaac-streak.fun"
            )
            time.sleep(15)

    @commands.command()
    async def leaderboard(self, ctx: commands.Context):
        await ctx.send(f"Leaderboard on isaac-streak.fun")
        time.sleep(15)


bot = Bot()

#   ==============================================================================
#
#   СЕКЦИЯ ФУНКЦИЙ ПО ОБНОВЛЕНИЮ ФАЙЛА С НИКАМИ СТРИМЕРОВ, ПЕРЕЗАПУСК ФАЙЛА bot.py
#
#   ==============================================================================
def restart():
    # print("argv was",sys.argv)
    # print("sys.executable was", sys.executable)
    print("restart now")
    auth_log("restarted by func restart()")
    os.execv(sys.executable, ["python"] + sys.argv)


# перезапуск бота, чтобы он мог раз в 5 мин подключаться к каналам, которые стали ОНЛАЙН
def reload_bot():
    threading.Timer(
        300, restart
    ).start()  # время, через которое запускать функцию - в секундах.


def auth_log(msg):
    with open(f"{PATH_TO_CSV}/bot_restart_log.csv", "a", newline="") as csv_file:
        write_csv = csv.writer(csv_file, delimiter=",")
        write_csv.writerow([time.ctime(), msg])
        csv_file.close()


def auth_commands_log(msg):
    with open(f"{PATH_TO_CSV}/bot_commands_log.csv", "a", newline="") as csv_file:
        write_csv = csv.writer(csv_file, delimiter=",")
        write_csv.writerow([time.ctime(), msg])
        csv_file.close()


if __name__ == "__main__":
    reload_bot()
    bot.run()
