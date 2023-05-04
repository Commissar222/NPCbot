import discord
import random
import re


def run_bot():
    token = 'MTEwMzU2Mjg4ODY1ODAzNDY4OA.GDJFns.p1xWzEzFBUVLVo7HddduhqHAA4_gfdtH-ilpAo'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    # A dictionary to keep track of the order of users in the channel
    user_order = {}


    @client.event
    async def on_ready():
        print("Logged in as {0.user}".format(client))


    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith("!roll"):
            # Parse the command and extract the values for x, y and z
            roll_regex = re.compile(r"(\d+)d(\d+)\s*(?:\+\s*(\d+))?")
            match = roll_regex.search(message.content)
            if match is None:
                await message.channel.send("Invalid roll command. Usage: !roll xdy+z")
                return

            x = int(match.group(1))
            y = int(match.group(2))
            z = int(match.group(3) or 0)

            # Roll the dice and calculate the total sum
            rolls = [random.randint(1, y) for _ in range(x)]
            total = sum(rolls) + z

            # Send a message with the individual dice rolls and the total sum
            rolls_str = ", ".join(str(r) for r in rolls)
            await message.channel.send(f"{message.author.mention} rolled {x}d{y}+{z}: {rolls_str} = {total}")

        elif message.content.startswith("!list"):
            # List the users in the channel and assign them to a random order
            users = list(message.channel.members)
            random.shuffle(users)
            user_order[message.guild.id] = users

            # Send a message with the new user order
            order_str = "\n".join(f"{i + 1}. {u.display_name}" for i, u in enumerate(users))
            await message.channel.send(f"User order for this channel:\n{order_str}")

        elif message.content.startswith("!clear"):
            # Clear the user order for this channel
            if message.guild.id in user_order:
                del user_order[message.guild.id]
                await message.channel.send("User order cleared.")

        elif message.content.startswith("!order"):
            # Show the current user order for this channel
            if message.guild.id in user_order:
                users = user_order[message.guild.id]
                order_str = "\n".join(f"{i + 1}. {u.display_name}" for i, u in enumerate(users))
                await message.channel.send(f"Current user order for this channel:\n{order_str}")
            else:
                await message.channel.send("No user order is currently set for this channel.")

    client.run(token)
