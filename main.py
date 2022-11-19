from dotenv import load_dotenv

import discord
import logging
import os
import config

load_dotenv()

token = os.getenv('TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default().all()
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_member_join(member):
    channel = client.get_channel(config.channel_welcome)
    embed = discord.Embed(title=f"{member.name} joined!",
                          description=f"Hey **{member.mention}** welcome to **{member.guild.name}**\n"
                                      f"  Do you want to read rules?{config.channel_rules}\n"
                                      f" Do you want to get role? {config.channel_get_role}\n ",
                          color=0x5f72ed)
    embed.set_image(
        url="https://cdn.discordapp.com/attachments/925876825907920937/1043632142078451836/E9BB151A-26CF-4621-BB1D-27C0AAF9D6D6.gif")
    await channel.send(embed=embed)


@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == config.ID_POST:
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = discord.utils.get(message.guild.members, id=payload.user_id)
        emoji = str(payload.emoji)

        try:
            role = discord.utils.get(message.guild.roles, id=config.ROLES_LIST[emoji])

            if len([i for i in user.roles if i.id not in config.USER_ROLES_LIST]) <= config.MAX_ROLES:
                await user.add_roles(role)
                print(f"{user.name} получил роль {role.name}")
            else:
                await message.remove_reaction(payload.emoji, user)
                print(f"Ошибка! пользователь {user.name} пытался получить слишком много ролей")

        except Exception as _ex:
            print(repr(_ex))


@client.event
async def on_raw_reaction_remove(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = discord.utils.get(message.guild.members, id=payload.user_id)

    try:
        emoji = str(payload.emoji)
        role = discord.utils.get(message.guild.roles, id=config.ROLES_LIST[emoji])
        await user.remove_roles(role)
    except Exception as _ex:
        print(repr(_ex))


client.run(token, log_handler=handler)
