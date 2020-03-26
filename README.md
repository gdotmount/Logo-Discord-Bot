# Logo-Discord-Bot
Login bot for Strake Jesuit discord server (coded in python)
*assuming import of discord.py*

When a user joins the Strake Jesuit discord server (name tbd), they will automatically be restricted to the welcome page based on their role (they will have no role).
There, Logo Bot will greet them and instruct them to send the first tagline of their Strake Jesuit email to begin the verification process.
  Note: Nearly all Strake Jesuit emails are made according to this format:
  <first initial><middle initial><lastname><last 2 digits of class year>@mail.strakejesuit.org
  ex. if a student has the email, "chbowring22@mail.strakejesuit.org", they would respond to Logo Bot, "chbowring22"
Upon the user sending their tagline, the Logo Bot will cross=reference with a 2D array list containing all taglines of the student body.
   The columns of the list will organize the class year; the rows will list off the students within their respective class.
   The program will substring the last two digits of the tagline to determine which column inside the array list to consult; the program      will then have to traverse the column until it finds a matching tagline.
Upon matching the tagline with its correspondent in the list, the program will access an email server and send the student's email a code, which the user will reply to the bot (in Discord) with to confirm their identity.
Upon verification of the student's identity, Logo Bot will change the student's roll to the corresponding role for their class year, which will then grant the user permissions to enter and use the server to the role's granted extent.
