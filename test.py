import discord
import asyncio
from extract import extract_boss_records


CHANNEL_NAME = 'general'


class MyClient(discord.Client):

    def get_listening_channels(self):
        listeners = []

        channels = client.get_all_channels()
        for channel in channels:
            if isinstance(channel, discord.TextChannel) and channel.name == CHANNEL_NAME:
                listeners.append(channel)
        return listeners

    async def update_channel(self):
        boss_records = extract_boss_records()
        boss_records = [boss for boss in boss_records if 5 < boss["remaining_time"] <= 10]
        listeners = self.get_listening_channels()
        for listener in listeners:
            for boss in boss_records:
                info = "{} will respawn in {}min.".format(boss["name"], boss["remaining_time"])
                await listener.send(info)

    async def on_ready(self):
        print('Logged on as', self.user)
        while True:
            await self.update_channel()
            await asyncio.sleep(5)


intents = discord.Intents.default()
client = MyClient(intents=intents)
client.run('')
