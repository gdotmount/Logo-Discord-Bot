import discord
import random
import smtplib, ssl
from discord.ext import commands

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


@client.command(pass_context=True)
async def confirm(ctx, tagline):
    if str(ctx.channel) == 'welcome-verify':
        print(f'.confirm method called, cross-referencing tagline({tagline}) with registered taglines...')
        v_student_list = open("verified_student_list.txt", 'r')
        user_tagline_list = v_student_list.read().split(';\n')
        cross_taglines = []
        for user_tagline in user_tagline_list:
            tag = user_tagline[slice(user_tagline.find(':')+2, len(user_tagline))]
            cross_taglines.append(tag)
        if tagline.lower() not in cross_taglines:
            print('Unregistered tagline, beginning verification process...')
            ctx.author.tagline = tagline
            ctx.author.classyear = tagline[slice(len(tagline) - 2, len(tagline))]
            clientemail = tagline + '@mail.strakejesuit.org'
            print('Client: ' + tagline)
            await ctx.send("Thanks, {0.author.mention}".format(ctx) + ". We'll send an email to " + clientemail)
            ctx.author.v_code = random.randrange(100000, 999999, 1)
            print(f'Generated random code for {ctx.author} at {clientemail}: {ctx.author.v_code}')
            emailcontents = f"Subject: SJ Discord Verification\n\nHere is your verification code for SJ's Discord: {ctx.author.v_code}" + f'\nPlease type ".code {ctx.author.v_code}" in the Discord chat to verify.'
            print(f'Email Contents:\n{emailcontents}\n')
            await client.send_email(clientemail, emailcontents)
        else:
            print('Tagline is already registered')
            await ctx.channel.send("This tagline has already been registered. If there's an issue, please reach out to one of the moderators or admins")
    v_student_list.close()

@client.command(pass_context=True)
async def hack(ctx):
    await ctx.channel.send('**HACKING THE MAINFRAME...**\n')
    for k in range(0, 30):
        await ctx.channel.send(str(random.randrange(10000000000000000,99999999999999999,1)))
    await ctx.channel.send('**MAINFRAME HACKED...**')


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
    if str(ctx.channel) == 'welcome-verify':
        print(f'Code received by {ctx.author}, checking authenticity against {ctx.author.v_code}...')
        if code_entry == str(ctx.author.v_code) and code_entry != '0':
            print('Correct code, user verified\nAdding user member role...')
            await ctx.send(f'Thanks for verifying, {ctx.author.mention}, welcome to the server!')
            if ctx.author.classyear =='20':
                classrole = 'Senman'
            elif ctx.author.classyear == '21':
                classrole = 'Junman'
            elif ctx.author.classyear == '22':
                classrole = 'Sophman'
            else: classrole = 'Freshman'

            role = discord.utils.get(ctx.guild.roles, name=classrole)
            print(f'Role identified: {classrole}')
            await ctx.author.add_roles(role)
            print('Role assigned')
            v_student_list = open("verified_student_list.txt", "a")
            v_student_list.write(f'{ctx.author}: {ctx.author.tagline.lower()};\n')
            v_student_list.close()
        else:
            print('Code not accepted')
            await ctx.send('Your code was not accepted, please either enter your code again or request a new one')


@client.command(pass_context=True)
async def clear(ctx, amount=1):
    a = 0
    print(f"Deleting messages\nMessage ID's:")
    channel = ctx.message.channel
    print (channel.history(limit = int(amount)))
    async for msg in channel.history(limit = int(amount)):
        print(f'"{msg.content}"')
        a += 1
        await msg.delete()
    print(f'{amount} message(s) deleted')
    await channel.send(f'{a} message(s) deleted')

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    if str(message.channel) == 'welcome-verify' and str(message.author).lower() != 'mee6#4876':
        await message.delete()
    if 'logo' and 'bot' and 'who is your dad' in message.content and message.channel.id:
        await message.channel.send("They're literally listed to the fucking right")
    await client.process_commands(message)



client.run('TOKEN')
