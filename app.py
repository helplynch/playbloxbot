import discord
import json
import random
import string
from discord.ext.commands import Bot
from urllib.request import urlopen
from discord.utils import get

token = 'MTA5MjA2MDIyMzMwMjI4NzQ4NA.GDuiUC.YbZKcUtiZNlX12EnveWGDqhPe3gfslZk4GXl2A'
prefix = 'p!'
server_id = '1091873095918297168'
website = 'https://play-blox.000webhostapp.com'
intents = discord.Intents.all()
intents.members = True

client = Bot(prefix,intents=intents)


def getAPI(ep):
    url = ep
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json


def randS(length):
    result_str = ''.join(
        random.choice(string.ascii_letters) for i in range(length))
    return result_str


@client.event
async def on_ready():
    print("Bot is ready!")
    print(f'{client.user} has connected to Discord!')


@client.command()
async def user(m, username):
    username = getAPI("" + website +
                      """/api/user/getUserInfo.php?username=""" + username +
                      "")
    if username["response"] == "404":
        await m.send('The user you are looking for does not exist.')
    else:
        embed = discord.Embed(title=username["username"],
                              url="" + website + "/profile/" +
                              username["username"] + "",
                              color=0xfe8447)
        embed.set_thumbnail(url=website + username["avatar"])
        embed.add_field(name="Information:",
                        value="ID: " + str(username["id"]) + "\n Bio:\n " +
                        username["bio"] + " \n Forum Posts: " +
                        str(username["forum_posts"]) + " \n Profile Views: " +
                        str(username["profile_views"]) + "",
                        inline=False)
        embed.set_footer(
            text=
            "View the rest of this user's information on the Playblox website!"
        )
        await m.send(embed=embed)


@client.command()
async def users(m):
    uC = getAPI("" + website + """/api/getUserCount.php""")
    await m.send("Playblox currently has " + str(uC["users"]) + " users.")


@client.command()
async def john(m):
    await m.send("John is God. John is everything.")


@client.command()
async def verify(message, user):
    server = client.get_guild(1091873095918297168)
    role = discord.utils.get(server.roles, name="Verified")

    if role in message.author.roles:
        await message.send("You are already verified.")
    else:

        user = getAPI("" + website +
                      """/api/user/getUserInfo.php?username=""" + user + "")
        if user["response"] == "404":
            await message.send(
                'The user you are trying to verify does not exist.')
        else:
            code = randS(21)
            embed = discord.Embed(title="Playblox Verification",
                                  color=0xfe8447)
            embed.add_field(
                name=
                "------------------------------------------------------------------",
                value=
                "Please insert the verification code onto your bio. After that, please send the command p!confirm in the #verify channel.\n Code: "
                + code + "",
                inline=False)
            await message.author.send(embed=embed)

        msg = await client.wait_for(
        "message",
        check=lambda x: x.channel.id == message.channel.id
        and message.author.id == x.author.id
        and x.content.lower() == "p!confirm"
        or x.content.lower() == "p!cancel",
        timeout=None,
    )
        if msg.content.lower() == "p!confirm":
            user2 = getAPI("" + website +
                           """/api/user/getUserInfo.php?username=""" +
                           user["username"] + "")
            bio = user2["bio"]
            print(user2["bio"])
            print(code)
            print(bio.count(code))
            if bio.count(code) == 0:
                await message.send(
                    "You did not put the verification code onto your bio, the verification process has been cancelled."
                )
            else:
                member = await server.fetch_member(message.author.id)
                await member.add_roles(role)
                await member.edit(nick=user2["username"])
                await message.send("Successfully have been verified!")
        else:
            await message.send("You have cancelled the verification process.")


client.run(token)
