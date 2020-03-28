import discord
import random
import smtplib, ssl
from discord.ext import commands
from discord.utils import get

class MyClient(discord.Client):
    smtp_server = "smtp.gmail.com"
    port = '587'  # For starttls
    server = smtplib.SMTP(smtp_server, port)
    sender_email = "sjstucoprojects@gmail.com"
    password = "mag1s8900"
    clientemail = ''
    emailcontents = ''
    classyear = ''
    v_code = ''
    classrole = ''
    context = ssl.create_default_context()
    client = commands.Bot(command_prefix='.')

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        async def on_member_join(self, member):
            guild = member.guild
            if guild.system_channel is not None:
                to_send = 'Welcome {0.mention} to {1.name}! Please reply to me with the command, "!confirm-", followed by \
    the beginning tagline of your Strake Jesuit email to begin verification of your identity.'.format(member, guild)
                await guild.system_channel.send(to_send)
                await guild.system_channel.send('As an example, if your Strake Jesuit email was\
     "gmmount20@mail.strakejesuit.org", you would reply "!confirm-gmmount20"'.format(member, guild))

    async def send_email(self):
        # Try to log in to server and send email
        try:
            self.server.connect(self.smtp_server, self.port)
            self.server.starttls(context=self.context)  # Secure the connection
            self.server.login(self.sender_email, self.password)
            self.server.sendmail('sjstucoprojects@gmail.com', self.clientemail, self.emailcontents)
        except Exception as e:
            # Print any error messages to stdout
            print('STMP Package Error:')
            print(e)
        finally:
            self.server.quit()

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!fuckme'):
            await message.channel.send('no {0.author.mention}'.format(message))

        if message.content.startswith("!confirm"):
            print("data found")
            tagline = message.content[slice(9, len(message.content))]
            self.classyear = tagline[slice(len(tagline) - 2, len(tagline))]
            self.clientemail = tagline + "@mail.strakejesuit.org"
            print('client: ' + tagline)
            await message.channel.send("Thanks, {0.author.mention}".format(message) + ". We'll send an email to " + self.clientemail)
            self.v_code = str(random.randrange(100000, 999999, 1))

            print('Generated random code: ' + self.v_code + '\n' + "Sending to " + self.clientemail)
            self.emailcontents = "Subject: SJ Discord Verification\n\n" + "Here is your verification code for SJ's Discord: " + self.v_code
            print('Email Contents: \n' + self.emailcontents)
            await client.send_email()


        if str(message.content) == self.v_code:
            print(self.classyear)
            if self.classyear == '20':
                self.classrole = "Senior"
            elif self.classyear == '21':
                self.classrole = "Junior"
            elif self.classyear == '22':
                self.classrole = "Sophman"
            elif self.classyear == '23':
                self.classrole = "Freshboi"
            await message.channel.send("You've been verified! Welcome to the server {0.author.mention}".format(message))

            @client.event
            @.command(pass_context=True)
            async def addrole(ctx):
                member = ctx.message.author
                role = get(member.guild.roles, name=self.classrole)
                await self.Bot.add_roles(member, role)

client = MyClient()
client.run('NjkyNDUzMzkxMDkxMzY4MDE3.Xn5Nmg.OeOssOQPMKnGEDa9UH_Z0dWeHmc')

