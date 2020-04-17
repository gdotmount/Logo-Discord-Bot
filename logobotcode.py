from typing import TextIO, Optional, Any

import discord
import random
from discord.ext import commands
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time

client = commands.Bot(command_prefix='.')
global poll

@client.event
async def on_ready():
    print('Bot is logged in')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.command(pass_context=True)
async def confirm(ctx, tagline):
    consoleout = client.get_channel(698216599970381895)
    if str(ctx.channel) == 'welcome-verify':
        adminrole = discord.utils.get(ctx.guild.roles, name='The Board of Directors (Admin)')
        if ctx.author.emails >= 5 and adminrole not in ctx.author.roles:
            print(f' {ctx.author} emails sent: {ctx.author.emails}')
            ctx.author.emails = ctx.author.emails + 1
            print("confirm method called, but too many emails\n")
            await ctx.author.send(
                "You have reached Logo Bot's email limit. Reach out to an admin if your verification is failing - "
                "housecouncil@mail.strakejesuit.org")
            await consoleout.send(
                f'{ctx.author} has requested too many verifications. Total requested: {ctx.author.emails}')
            return
        print(f'.confirm method called, cross-referencing tagline({tagline}) with registered taglines...')
        if '@' in tagline:
            print('user did not enter tagline; instead entered email')
            await ctx.author.send('You entered an email. Enter in the tagline (the part that comes before the "@".')
            return
        v_student_list_confirm: TextIO = open("verified_student_list.txt", 'r')
        user_tagline_list = v_student_list_confirm.read().split(';\n')
        cross_taglines = []
        v_student_list_confirm.close()
        for user_tagline in user_tagline_list:
            tag = user_tagline[slice(user_tagline.find(':') + 2, len(user_tagline))]
            cross_taglines.append(tag)
        if tagline.lower() not in cross_taglines:
            print('Unregistered tagline, beginning verification process...')
            ctx.author.tagline = tagline
            ctx.author.classyear = tagline[slice(len(tagline) - 2, len(tagline))]
            clientemail = tagline + '@mail.strakejesuit.org'
            print('Client: ' + tagline)
            await ctx.author.send("Thanks, {0.author.mention}".format(
                ctx) + ". We'll send an email to " + clientemail + ". Do not respond to this DM; verify in the "
                                                                   "#welcome-verify channel. Check your email's spam "
                                                                   "folder if you don't see your code!")
            ctx.author.v_code = random.randrange(100000, 999999, 1)
            print(f'Generated random code for {ctx.author} at {clientemail}: {ctx.author.v_code}')
            await consoleout.send(
                f'Generated random code for {ctx.author} to be sent to:{clientemail}: {ctx.author.v_code}')
            print(f' {ctx.author} emails sent: {ctx.author.emails}\n')
            await consoleout.send(f'{ctx.author} has sent {ctx.author.emails}, which is too many.')
            await client.send_email(clientemail, ctx.author.v_code, f'{ctx.author}')
            ctx.author.emails = (ctx.author.emails) + 1
            await consoleout.send(f'Email sent to {clientemail}')
        else:
            print('Tagline is already registered\n')
            await consoleout.send(f'{ctx.author} submitted tagline {tagline}, which has already been registered.')
            await ctx.author.send(
                'This tagline has already been registered. If there\'s an issue, please send an email to '
                'housecouncil@mail.strakejesuit.org and we\'ll get in touch. This DM is not monitored.')


@client.command(pass_context=True)
async def hack(ctx):
    await ctx.channel.send('**HACKING THE MAINFRAME...**\n')
    for k in range(0, 30):
        await ctx.channel.send(str(random.randrange(10000000000000000, 99999999999999999, 1)))
    await ctx.channel.send('**MAINFRAME HACKED...**')


@client.event
async def send_email(cemail, v_code, author):
    consoleout = client.get_channel(698216599970381895)
    strFrom = 'The Atrium <housecouncil@mail.strakejesuit.org>'
    strTo = cemail
    print('starting msg creating')
    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'The Atrium Verification Code'
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText(f'''
    <!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><head>
            <title>

            </title>
            <!--[if !mso]><!-- -->
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <!--<![endif]-->
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style type="text/css">
              #outlook a {{ padding:0; }}
              .ReadMsgBody {{ width:100%; }}
              .ExternalClass {{ width:100%; }}
              .ExternalClass * {{ line-height:100%; }}
              body {{ margin:0;padding:0;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%; }}
              table, td {{ border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt; }}
              img {{ border:0;height:auto;line-height:100%; outline:none;text-decoration:none;-ms-interpolation-mode:bicubic; }}
              p {{ display:block;margin:13px 0; }}
            </style>
            <!--[if !mso]><!-->
            <style type="text/css">
              @media only screen and (max-width:480px) {{
                @-ms-viewport {{ width:320px; }}
                @viewport {{ width:320px; }}
              }}
            </style>
            <!--<![endif]-->
            <!--[if mso]>
            <xml>
            <o:OfficeDocumentSettings>
              <o:AllowPNG/>
              <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
            </xml>
            <![endif]-->
            <!--[if lte mso 11]>
            <style type="text/css">
              .outlook-group-fix {{ width:100% !important; }}
            </style>
            <![endif]-->

          <!--[if !mso]><!-->
            <link href="https://fonts.googleapis.com/css?family=Ubuntu:300,400,500,700" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Cabin:400,700" rel="stylesheet" type="text/css">
            <style type="text/css">
              @import url(https://fonts.googleapis.com/css?family=Ubuntu:300,400,500,700);
    @import url(https://fonts.googleapis.com/css?family=Cabin:400,700);
            </style>
          <!--<![endif]-->



        <style type="text/css">
          @media only screen and (min-width:480px) {{
            .mj-column-per-100 {{ width:100% !important; max-width: 100%; }}
          }}
        </style>


            <style type="text/css">



        @media only screen and (max-width:480px) {{
          table.full-width-mobile {{ width: 100% !important; }}
          td.full-width-mobile {{ width: auto !important; }}
        }}

            </style>
            <style type="text/css">.hide_on_mobile {{ display: none !important;}}
            @media only screen and (min-width: 480px) {{ .hide_on_mobile {{ display: block !important;}} }}
            .hide_section_on_mobile {{ display: none !important;}}
            @media only screen and (min-width: 480px) {{ .hide_section_on_mobile {{ display: table !important;}} }}
            .hide_on_desktop {{ display: block !important;}}
            @media only screen and (min-width: 480px) {{ .hide_on_desktop {{ display: none !important;}} }}
            .hide_section_on_desktop {{ display: table !important;}}
            @media only screen and (min-width: 480px) {{ .hide_section_on_desktop {{ display: none !important;}} }}
            [owa] .mj-column-per-100 {{
                width: 100%!important;
              }}
              [owa] .mj-column-per-50 {{
                width: 50%!important;
              }}
              [owa] .mj-column-per-33 {{
                width: 33.333333333333336%!important;
              }}
              p {{
                  margin: 0px;
              }}
              @media only print and (min-width:480px) {{
                .mj-column-per-100 {{ width:100%!important; }}
                .mj-column-per-40 {{ width:40%!important; }}
                .mj-column-per-60 {{ width:60%!important; }}
                .mj-column-per-50 {{ width: 50%!important; }}
                mj-column-per-33 {{ width: 33.333333333333336%!important; }}
                }}</style>

          </head>
          <body style="background-color:#FFFFFF;">


          <div style="background-color:#FFFFFF;">


          <!--[if mso | IE]>
          <table
             align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
          >
            <tr>
              <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
          <![endif]-->


          <div style="Margin:0px auto;max-width:600px;">

            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
              <tbody>
                <tr>
                  <td style="direction:ltr;font-size:0px;padding:9px 0px 9px 0px;text-align:center;vertical-align:top;">
                    <!--[if mso | IE]>
                      <table role="presentation" border="0" cellpadding="0" cellspacing="0">

            <tr>

                <td
                   class="" style="vertical-align:top;width:600px;"
                >
              <![endif]-->

          <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">

          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">

                <tbody><tr>
                  <td align="center" style="font-size:0px;padding:0px 0px 0px 0px;word-break:break-word;">

          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
            <tbody>
              <tr>
                <td style="width:102px;">

          <img height="auto" src="cid:image1" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;" width="102">

                </td>
              </tr>
            </tbody>
          </table>

                  </td>
                </tr>

                <tr>
                  <td align="left" style="font-size:0px;padding:15px 15px 15px 15px;word-break:break-word;">

          <div style="font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:11px;line-height:1.5;text-align:left;color:#000000;">
            <p style="text-align: center;"><span style="font-size: 13px;">Thanks for verifying, {author} . Welcome to The Atrium. Copy and paste this command in the #welcome-verify channel: <b>.code {v_code}</b>.</span></p>
          </div>
                  </td>
                </tr>

                <tr>
                  <td align="left" style="font-size:0px;padding:15px 15px 15px 15px;word-break:break-word;">

          <div style="font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:11px;line-height:1.5;text-align:left;color:#000000;">
            <p style="text-align: center;"><span style="font-family: terminal, monaco, monospace; font-size: 48px;">.code {v_code}</span></p>
          </div>

                  </td>
                </tr>

          </tbody></table>

          </div>

              <!--[if mso | IE]>
                </td>

            </tr>

                      </table>
                    <![endif]-->
                  </td>
                </tr>
              </tbody>
            </table>

          </div>


          <!--[if mso | IE]>
              </td>
            </tr>
          </table>
          <![endif]-->


          </div>



      </body></html>
    ''', 'html')

    msgAlternative.attach(msgText)
    print('starting logo open process')
    # This example assumes the image is in the current directory
    fp: object = open('logoHR.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)
    # Send the email (this example assumes SMTP authentication is required)
    print("starting STMP")
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.connect('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    print("connected to STMP")
    smtp.login('housecouncil@mail.strakejesuit.org', 'logobot!!')
    print("logged in")
    try:
        smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    except:
        print("sendmail failed")
    print("email sent!")
    smtp.quit()


@client.command(pass_context=True)
async def code(ctx, code_entry):
    consoleout = client.get_channel(698216599970381895)
    if str(ctx.channel) == 'welcome-verify':
        print(f'Code received by {ctx.author}, checking authenticity against {ctx.author.v_code}...')
        await consoleout.send(f'Code received by {ctx.author}, checking authenticity against {ctx.author.v_code}...')
        if code_entry == str(ctx.author.v_code) and code_entry != '0':
            print('Correct code, user verified\nAdding user member role...')
            await consoleout.send(f'Correct code, {ctx.author} verified. \nAdding user member role...')
            await ctx.author.send(
                f'Thanks for verifying, {ctx.author.mention}. Welcome to The Atrium - Designed for Students, '
                f'by Students. If you have any technical issues, reach out to any of our moderators or admins.')
            if ctx.author.classyear == '20':
                classrole = 'Senior'
            elif ctx.author.classyear == '21':
                classrole = 'Junior'
            elif ctx.author.classyear == '22':
                classrole = 'Sophomore'
            elif ctx.author.classyear == '23':
                classrole = 'Freshman'
            else:
                classrole = 'Under Review'
                await ctx.author.send(
                    f'We have detected an issue interpreting your class year from your tagline. This could be because you are an alumni or a faculty member; a moderator will review your account. This can take up to 24 hours!')
                reviewchannel = client.get_channel(698246842281885706)
                await reviewchannel.send(
                    f'{ctx.author} is requesting verification. Tagline:{ctx.author.tagline}. Provide them either a faculty or alumni roll! ')

            role: Optional[Any] = discord.utils.get(ctx.guild.roles, name=classrole)
            print(f'Role identified: {classrole}')
            await consoleout.send(f'{ctx.author} identified role: {classrole}')
            await ctx.author.add_roles(role)
            print('Role assigned')
            await consoleout.send(f'{ctx.author} assigned role: {classrole}')
            v_student_list_code: TextIO = open("verified_student_list.txt", 'a')
            v_student_list_code.write(f'{ctx.author}: {ctx.author.tagline.lower()};\n')
            await consoleout.send(f'Adding {ctx.author} with tagline {ctx.author.tagline.lower()} to database...')
            v_student_list_code.close()
            await consoleout.send(f'{ctx.author} info added to database. \n - ')
        else:
            print('Code not accepted')
            await consoleout.send(
                f'{ctx.author} entered an incorrect code. Email was sent to {ctx.author.tagline}. Recieved code: {code_entry}; Correct code: {ctx.author.v_code} \n - ')
            await ctx.author.send(
                'Your code was not accepted, please either enter your code again or request a new one by re-doing '
                'your .confirm command. Do not respond to this DM; re-verify in the #welcome-verify channel')


@client.command(pass_context=True)
async def clear(ctx, amount=1, authoroptional='none'):
    adminRole = discord.utils.get(ctx.guild.roles, name='The Board of Directors (Admin)')
    author = authoroptional
    if authoroptional == "logo":
        print("found logo, changing to logobot's user")
        author == "Logo#9050"
    if adminRole in ctx.author.roles:
        a = 0
        print(f"Deleting messages\nMessage ID's:")
        channel = ctx.message.channel
        msgcount = 0
        async for msg in channel.history(limit=int(amount)):
            if author != "none":
                if str(msg.author) == author:
                    a += 1
                    await msg.delete()
                    print(f'{msg.author}: {msg.content} was deleted.')

                else:
                    print(f'{msg.content} not deleted (not by {author})')
            else:
                await msg.delete()
                a += 1
                print(f'{msg.content} deleted with no author restriction')
        print(f'{a} message(s) deleted')
        clearconf = await channel.send(f'{a} message(s) deleted')
        time.sleep(10)
        await clearconf.delete()
    else:
        return


@client.command(pass_context=True)
async def search(ctx, search_user):
    if str(ctx.channel) == 'tagline-search-system':
        v_student_list_search: TextIO = open("verified_student_list.txt", 'r')
        linenum = 0
        found = False
        for line in v_student_list_search:
            tagtemp = line[slice(line.find(':') + 2, len(line) - 1)]
            if str(search_user).lower() in line:
                found = True
                tag = tagtemp
                linenum = linenum + 1
        if found:
            message = await ctx.channel.send(
                f"Discord user {search_user}'s tagline located in line {linenum} of database: {tag}")
        else:
            message = await ctx.channel.send(f'{search_user} is not associated with a tagline.')
        time.sleep(5)
        messageclear = await ctx.channel.send('Removing search result...')
        time.sleep(2)
        await message.delete()
        await messageclear.delete()
        v_student_list_search.close()
        return


@client.command(pass_context=True)
async def createemail(ctx, password, subject, contents):
    consoleout = client.get_channel(698216599970381895)
    passwordcheck = open("emailpassword.txt", "r")
    emailcount = 0
    if password not in passwordcheck:
        await ctx.channel.send("Email password not accepted")
        return
    email_list = []
    newsub = subject
    verifiedstudents = open("verified_student_list.txt", 'r')
    for line in verifiedstudents:
        tagtemp = line[slice(line.find(':') + 2, len(line) - 2)]
        tag = tagtemp + "@mail.strakejesuit.org"
        email_list.append(tag)
    print("starting STMP")
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.connect('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    print("connected to STMP")
    smtp.login('housecouncil@mail.strakejesuit.org', 'logobot!!')
    print("logged in")
    print("starting email send process")
    emailconfirmation = await ctx.channel.send('Sending emails.....')
    for recepient in email_list:
        strFrom = 'The Atrium <housecouncil@mail.strakejesuit.org>'
        strTo = recepient
        print('starting msg creating')
        # Create the root message and fill in the from, to, and subject headers
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = str(newsub)
        msgRoot['From'] = strFrom
        msgRoot['To'] = recepient
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        msgText = MIMEText('This is the alternative plain text message.')
        msgAlternative.attach(msgText)

    # We reference the image in the IMG SRC attribute by the ID we give it below
        msgText = MIMEText(f'''
        <!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><head>
                <title>

                </title>
                <!--[if !mso]><!-- -->
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <!--<![endif]-->
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style type="text/css">
                  #outlook a {{ padding:0; }}
                  .ReadMsgBody {{ width:100%; }}
                  .ExternalClass {{ width:100%; }}
                  .ExternalClass * {{ line-height:100%; }}
                  body {{ margin:0;padding:0;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%; }}
                  table, td {{ border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt; }}
                  img {{ border:0;height:auto;line-height:100%; outline:none;text-decoration:none;-ms-interpolation-mode:bicubic; }}
                  p {{ display:block;margin:13px 0; }}
                </style>
                <!--[if !mso]><!-->
                <style type="text/css">
                  @media only screen and (max-width:480px) {{
                    @-ms-viewport {{ width:320px; }}
                    @viewport {{ width:320px; }}
                  }}
                </style>
                <!--<![endif]-->
                <!--[if mso]>
                <xml>
                <o:OfficeDocumentSettings>
                  <o:AllowPNG/>
                  <o:PixelsPerInch>96</o:PixelsPerInch>
                </o:OfficeDocumentSettings>
                </xml>
                <![endif]-->
                <!--[if lte mso 11]>
                <style type="text/css">
                  .outlook-group-fix {{ width:100% !important; }}
                </style>
                <![endif]-->

              <!--[if !mso]><!-->
                <link href="https://fonts.googleapis.com/css?family=Ubuntu:300,400,500,700" rel="stylesheet" type="text/css">
        <link href="https://fonts.googleapis.com/css?family=Cabin:400,700" rel="stylesheet" type="text/css">
                <style type="text/css">
                  @import url(https://fonts.googleapis.com/css?family=Ubuntu:300,400,500,700);
        @import url(https://fonts.googleapis.com/css?family=Cabin:400,700);
                </style>
              <!--<![endif]-->



            <style type="text/css">
              @media only screen and (min-width:480px) {{
                .mj-column-per-100 {{ width:100% !important; max-width: 100%; }}
              }}
            </style>


                <style type="text/css">



            @media only screen and (max-width:480px) {{
              table.full-width-mobile {{ width: 100% !important; }}
              td.full-width-mobile {{ width: auto !important; }}
            }}

                </style>
                <style type="text/css">.hide_on_mobile {{ display: none !important;}}
                @media only screen and (min-width: 480px) {{ .hide_on_mobile {{ display: block !important;}} }}
                .hide_section_on_mobile {{ display: none !important;}}
                @media only screen and (min-width: 480px) {{ .hide_section_on_mobile {{ display: table !important;}} }}
                .hide_on_desktop {{ display: block !important;}}
                @media only screen and (min-width: 480px) {{ .hide_on_desktop {{ display: none !important;}} }}
                .hide_section_on_desktop {{ display: table !important;}}
                @media only screen and (min-width: 480px) {{ .hide_section_on_desktop {{ display: none !important;}} }}
                [owa] .mj-column-per-100 {{
                    width: 100%!important;
                  }}
                  [owa] .mj-column-per-50 {{
                    width: 50%!important;
                  }}
                  [owa] .mj-column-per-33 {{
                    width: 33.333333333333336%!important;
                  }}
                  p {{
                      margin: 0px;
                  }}
                  @media only print and (min-width:480px) {{
                    .mj-column-per-100 {{ width:100%!important; }}
                    .mj-column-per-40 {{ width:40%!important; }}
                    .mj-column-per-60 {{ width:60%!important; }}
                    .mj-column-per-50 {{ width: 50%!important; }}
                    mj-column-per-33 {{ width: 33.333333333333336%!important; }}
                    }}</style>

              </head>
              <body style="background-color:#FFFFFF;">


              <div style="background-color:#FFFFFF;">


              <!--[if mso | IE]>
              <table
                 align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600"
              >
                <tr>
                  <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
              <![endif]-->


              <div style="Margin:0px auto;max-width:600px;">

                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                  <tbody>
                    <tr>
                      <td style="direction:ltr;font-size:0px;padding:9px 0px 9px 0px;text-align:center;vertical-align:top;">
                        <!--[if mso | IE]>
                          <table role="presentation" border="0" cellpadding="0" cellspacing="0">

                <tr>

                    <td
                       class="" style="vertical-align:top;width:600px;"
                    >
                  <![endif]-->

              <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">

              <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:top;" width="100%">

                    <tbody><tr>
                      <td align="center" style="font-size:0px;padding:0px 0px 0px 0px;word-break:break-word;">

              <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                <tbody>
                  <tr>
                    <td style="width:102px;">

              <img height="auto" src="cid:image1" style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px;" width="102">

                    </td>
                  </tr>
                </tbody>
              </table>

                      </td>
                    </tr>

                    <tr>
                      <td align="left" style="font-size:0px;padding:15px 15px 15px 15px;word-break:break-word;">

              <div style="font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:11px;line-height:1.5;text-align:left;color:#000000;">
                <p style="text-align: center;"><span style="font-size: 13px;"> {contents}</span></p>
              </div>

                      </td>
                    </tr>

                    <tr>
                      <td align="left" style="font-size:0px;padding:15px 15px 15px 15px;word-break:break-word;">

                      </td>
                    </tr>

              </tbody></table>

              </div>

                  <!--[if mso | IE]>
                    </td>

                </tr>

                          </table>
                        <![endif]-->
                      </td>
                    </tr>
                  </tbody>
                </table>

              </div>


              <!--[if mso | IE]>
                  </td>
                </tr>
              </table>
              <![endif]-->


              </div>



          </body></html>
        ''', 'html')

        msgAlternative.attach(msgText)
        print('starting logo open process')
        # This example assumes the image is in the current directory
        fp: object = open('logoHR.png', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()

        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)
        # Send the email (this example assumes SMTP authentication is required)
        try:
            smtp.sendmail(strFrom, strTo, msgRoot.as_string())
            emailcount = emailcount+1
            await emailconfirmation.edit(content=f'Emails sent: [{emailcount}] of [{(email_list.__len__()-1)}]')
            print(f'email sent to: {recepient}')
        except Exception as e:
            print(e)
        print("Waiting to send next email-----")
        time.sleep(1)
    await ctx.channel.send(f'All emails sent to: {email_list}')
    smtp.quit()
    return
@client.command(pass_context=True)
async def poll(ctx, temptitle, numoptions, option1, option2, option3="none", option4="none"):
    adminrole = discord.utils.get(ctx.author.guild.roles, name='The Board of Directors (Admin)')
    votechannel = client.get_channel(699828255687180359)
    title = "Poll: " + temptitle
    if adminrole in ctx.author.roles:
        if ctx.channel == votechannel:
            async for msg in ctx.channel.history(limit=10):
                await msg.delete()
        else:
            async for msg in ctx.channel.history(limit=2):
                await msg.delete()
        clear = await ctx.channel.send(f'Creating poll...')
        time.sleep(1)
        await clear.delete()
        if int(numoptions) == 2:
            pollmsg = await ctx.channel.send(f'***{title}*** \n Option 1: **{option1}** \n Option 2: **{option2}** \n React with your vote! ')
            await pollmsg.add_reaction("1️⃣")
            await pollmsg.add_reaction("2️⃣")
        if int(numoptions) == 3:
            pollmsg = await ctx.channel.send(f'***{title}*** \n Option 1: **{option1}** \n Option 2: **{option2}** \n Option 3: **{option3}** \n React with your vote! ')
            await pollmsg.add_reaction("1️⃣")
            await pollmsg.add_reaction("2️⃣")
            await pollmsg.add_reaction("3️⃣")
        if int(numoptions) == 4:
            pollmsg = await ctx.channel.send(f'***{title}*** \n Option 1: **{option1}** \n Option 2: **{option2}** \n Option 3: **{option3}** \n Option 4: **{option4}** \n React with your vote! ')
            await pollmsg.add_reaction("1️⃣")
            await pollmsg.add_reaction("2️⃣")
            await pollmsg.add_reaction("3️⃣")
            await pollmsg.add_reaction("4️⃣")

    else:
        return

@client.command(pass_context =True)
async def timer(ctx,title,duration, msg_on_finish="timer done"):
    adminrole = discord.utils.get(ctx.author.guild.roles, name='The Board of Directors (Admin)')
    seconds = int(duration)*60
    counter = 0
    if adminrole in ctx.author.roles:
        async for msg in ctx.channel.history():
            if ((title in msg.content) and (msg.author == ctx.author)) or msg.author == ctx.author:
                await msg.delete()

        timermsg = await ctx.channel.send(f'{title} :')

        minutescounter = int(duration)-1
        while counter <= seconds:
            secondscounter = (seconds-counter)%60
            if (secondscounter) == 1:
                if minutescounter != 0:
                    minutescounter = minutescounter-1
            counter = counter + 1
            await timermsg.edit(content=(f'{title} : **{minutescounter} minutes {secondscounter} seconds left**'))
            time.sleep(1)
        if (secondscounter ==0) and (minutescounter == 0):
            await timermsg.edit(content=(f'**!!{msg_on_finish}!!**!poll'))
            time.sleep(20)
            await timermsg.delete()
            return
    else:
        return

@client.event
async def on_message(message):
    consoleout = client.get_channel(698216599970381895)
    #print(f'{message.author}: {message}')
    if message.author.id == client.user.id:
        return
    if str(message.channel) == 'welcome-verify' and str(message.author) != 'MEE6#4876' and str(
            message.author) != 'kpreg01#6968':
        await message.delete()
    if str(message.channel) =="room-commands":
        await message.delete()
    if str(message.channel) == 'tagline-search-system':
        await message.delete()
    if 'logo' and 'bot' and 'who is your dad' in message.content and message.channel.id:
        await message.channel.send("They're literally listed to the fucking right")
    await client.process_commands(message)
    #print(message.channel)
    if "Direct Message" in str(message.channel):
        await message.channel.send("Logo Bot does not accept commands over Direct Message. Return to the server to enter a verification code in the #welcome-verify channel: https://discordapp.com/channels/692021066163421224/697866372079681637")

@client.command(pass_context=True)
async def addmessage(ctx,message):
    await ctx.channel.send(f'{message}')

client.run('token')
