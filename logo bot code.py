import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        
        
        if message.content.startswith('!fuckme'):
            await message.channel.send('no {0.author.mention}'.format(message))
        

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = 'Welcome {0.mention} to {1.name}! Please reply to me with the beginning tagline of your\
 Strake Jesuit email to begin verification of your identity.'.format(member, guild)
            await guild.system_channel.send(to_send)
            await guild.system_channel.send('As an example, if your Strake Jesuit email was\
 "gmmount20@mail.strakejesuit.org", you would reply "gmmount20"'.format(member, guild))


client = MyClient()
client.run("<Logo Bot's Token>")
