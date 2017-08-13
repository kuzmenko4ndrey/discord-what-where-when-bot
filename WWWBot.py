import discord
from discord.ext.commands import Bot
from discord.ext import commands
from threading import Timer
import asyncio

class Timer:

    def __init__( self, timeout, callback, channel ):
        self._timeout = timeout
        self._callback = callback
        self._channel = channel
        self._task = asyncio.ensure_future( self._job() )

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback( self._channel )

    def cancel(self):
        self._task.cancel()

client = discord.Client()
bot_prefix = "w."

@client.event
async def on_ready():
    print( "Bot online" )

async def tenSecs( channel ):
    await client.send_message( channel, "10 seconds left!" )

async def timeUp( channel ):
    await client.send_message( channel, "Time up!" )
    channels = channel.server.channels
    members = channel.server.members
    general_channel = None
    for c in channels:
        if c.name == "General":
            general_channel = c
            break
    for m in members:
        await client.move_member( m, general_channel )

@client.event
async def on_message( message ):
    if ( message.content == bot_prefix + "go" ):
        master = False
        for role in message.author.roles:
            if role.name == "Master":
                master = True
                break
        if master == False:
            await client.send_message( message.channel, "No, no, no, " + message.author.mention )
            return
        server = message.server
        channels = server.channels
        members = server.members
        for m in members:
            roles = m.roles
            for role in roles:
                if "Team" in role.name:
                    for channel in channels:
                        if channel.name == role.name:
                            await client.move_member( m, channel )
        await client.send_message( message.channel, "Your minute started!" )
        t1 = Timer( 50.0, tenSecs, message.channel )
        t2 = Timer( 60.0, timeUp, message.channel )
        # some shit, that throws warnings to console, but bot don't wanna work without it
        await client.process_commands( message )

client.run( "your token here" )
