import discord
import random
import smtplib, ssl
from discord.ext import commands
import logging

logging.basicConfig(level=logging.INFO)

smtp_server = "smtp.gmail.com"
port = '587'  # For starttls
server = smtplib.SMTP(smtp_server, port)
sender_email = "sjstucoprojects@gmail.com"
password = "mag1s8900"

context = ssl.create_default_context()
client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Bot is logged in')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = 'Welcome {0.mention} to {1.name}! Please reply to me with the command, ".confirm ", followed by \
the beginning tagline of your Strake Jesuit email to begin verification of your identity.'.format(member, guild)
        await guild.system_channel.send(to_send)
        await guild.system_channel.send('As an example, if your Strake Jesuit email was\
 "gmmount20@mail.strakejesuit.org", you would reply ".confirm gmmount20"')


@client.command(pass_context=True)
async def confirm(ctx, tagline):
    print('Data found')
    ctx.message.author.classyear = tagline[slice(len(tagline) - 2, len(tagline))]
    clientemail = tagline + '@mail.strakejesuit.org'
    print('Client: ' + tagline)
    await ctx.send("Thanks, {0.author.mention}".format(ctx) + ". We'll send an email to " + clientemail)
    #for the v_code and classyear to be set as an attribute to the member object, you must go to the "Member" class at the the file hosted at site-packages\discord\member.py
    #you must then add ", 'v_code', 'classyear'" as the last items in the "__slots__" list; you must also add "self.v_code = 0" underneath the "__init__" method below
    ctx.message.author.v_code = random.randrange(100000, 999999, 1)
    print(f'Generated random code for {ctx.message.author} at {clientemail}: {ctx.message.author.v_code}')
    emailcontents = f"Subject: SJ Discord Verification\n\nHere is your verification code for SJ's Discord: {ctx.message.author.v_code}"
    print(f'Email Contents:\n {emailcontents}')
    await client.send_email(clientemail, emailcontents)


@client.event
async def send_email(cemail, emailc):
    # Try to log in to server and send email
    try:
        server.connect(smtp_server, port)
        server.starttls(context=context)  # Secure the connection
        server.login(sender_email, password)
        server.sendmail('sjstucoprojects@gmail.com', cemail, emailc)
    except Exception as e:
        # Print any error messages to stdout
        print('STMP Package Error:')
        print(e)
    finally:
        server.quit()


@client.command(pass_context=True)
async def code(ctx, code_entry):
    print(f'Code received, checking authenticity against {ctx.message.author.v_code}...')
    if code_entry == str(ctx.message.author.v_code):
        print('Correct code, accepted\nChanging member role...')
        await ctx.send(f'Thanks for verifying, {ctx.author.mention}, welcome to the server!')
        if ctx.message.author.classyear =='20':
            classrole = 'Senior'
        elif ctx.message.author.classyear == '21':
            classrole = 'Junior'
        elif ctx.message.author.classyear == '22':
            classrole = 'Sophman'
        elif ctx.message.author.classyear == '23':
            classrole = 'Freshboi'
        role = discord.utils.get(ctx.message.author.guild.roles, name=classrole)
        print(f'Correct role identified: {classrole}')
        await ctx.message.author.add_roles(role)
        print('Role assigned')
    else:
        print('Code not accepted')
        await ctx.send('Your code was not accepted, please either enter your code again or request a new one')


client.run('TOKEN')
