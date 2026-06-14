# Full setup instruction for launching the Telegram bot

## 1. Requirements
- Python 3.11 or newer
- Telegram account
- Internet access
- macOS / Linux terminal (commands below are written for macOS/Linux)

## 2. Unpack the project
Unzip the archive and open the project folder in Terminal.

Example:
```bash
cd ~/Desktop/ceifbankstp_bot
```

## 3. Create your bot in Telegram
1. Open Telegram.
2. Search for **@BotFather**.
3. Send the command:
```text
/newbot
```
4. Enter a display name for the bot.
5. Enter a unique username for the bot. The username must end with `bot`, for example:
```text
my_credit_application_bot
```
6. BotFather will send you a **bot token**. Save it.

Example token format:
```text
123456789:AAExampleExampleExampleExampleExample
```

## 4. (Optional) Configure the bot in BotFather
Useful commands in @BotFather:
- `/setdescription` — set description
- `/setabouttext` — set short about text
- `/setuserpic` — set bot picture
- `/setcommands` — set command list

Recommended command list:
```text
start - start the bot
cancel - cancel the current application
myid - show your Telegram user ID
chatid - show the current chat ID
applications - show recent applications (admin chat only)
application - show one application by ID (admin chat only)
files - show files for an application (admin chat only)
setstatus - change application status (admin chat only)
bystatus - show applications by status (admin chat only)
```

## 5. Create a staff group for administrators
1. In Telegram create a group for bank staff or administrators.
2. Add your bot to this group.
3. It is recommended to make the bot an administrator in the group.
4. If you want to test the admin commands in the group, keep the bot in the group permanently.

## 6. Get the admin chat ID
After the bot is running, you will send `/chatid` **inside the staff group**. The bot will reply with the group chat ID. This value will be used as `ADMIN_CHAT_ID`.

For supergroups the ID usually looks like this:
```text
-1001234567890
```

## 7. Create a virtual environment
In the project folder run:
```bash
python3 -m venv venv
```

## 8. Activate the virtual environment
```bash
source venv/bin/activate
```

After activation, your terminal should start with `(venv)`.

## 9. Install dependencies
```bash
pip install -r requirements.txt
```

## 10. Create the .env file
Copy the template file:
```bash
cp .env.example .env
```

Open `.env` in nano:
```bash
nano .env
```

Paste your values:
```env
BOT_TOKEN=PASTE_YOUR_REAL_BOT_TOKEN_HERE
ADMIN_CHAT_ID=
```

At this moment, if you still do not know the admin chat ID, leave it empty and save the file.

Save in nano:
- `Control + O`
- `Enter`
- `Control + X`

## 11. Run the bot for the first time
```bash
python3 run.py
```

If everything is correct, the bot should start and wait for messages.

## 12. Check that the bot responds in Telegram
1. Open your bot in Telegram.
2. Press **Start** or send:
```text
/start
```
3. The bot should send a welcome message.

## 13. Get your user ID and group chat ID
### In the personal chat with the bot
Send:
```text
/myid
```
The bot will show your user ID and the current personal chat ID.

### In the staff group
Send:
```text
/chatid
```
The bot will show the group chat ID. Copy this number.

## 14. Put the admin chat ID into .env
Stop the bot in the terminal:
```text
Control + C
```

Open `.env` again:
```bash
nano .env
```

Insert the group ID:
```env
BOT_TOKEN=PASTE_YOUR_REAL_BOT_TOKEN_HERE
ADMIN_CHAT_ID=-1001234567890
```

Save the file and close nano.

## 15. Run the bot again
```bash
python3 run.py
```

## 16. Test the user scenario
In Telegram open the bot and complete a full application:
1. `/start`
2. `Start application`
3. Confirm that the application is submitted on behalf of a legal entity
4. Enter company data
5. Enter contact person data
6. Enter financing data
7. Add files if needed
8. Confirm personal data processing consent
9. Confirm NCND
10. Check Summary
11. Press `Submit application`

If the bot is configured correctly:
- the application will be saved in SQLite,
- the user will see a success message,
- the staff group will receive a notification.

## 17. Test the admin commands in the staff group
Send these commands in the admin group:
```text
/applications
/application 1
/files 1
/setstatus 1 in_review
/bystatus in_review
```

Available statuses:
- `new`
- `in_review`
- `contacted`
- `rejected`
- `approved_next_step`

## 18. Where the data is stored
The application data is stored in a local SQLite database file that is created automatically after the first successful run.

The database file appears here:
```text
data/applications.db
```

## 19. How to stop the bot
In the terminal where the bot is running:
```text
Control + C
```

## 20. Common problems and solutions
### Problem: `No module named 'aiogram'`
Solution:
1. Activate the virtual environment:
```bash
source venv/bin/activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Problem: `Bad Request: chat not found`
Solution:
- Make sure the bot is added to the staff group.
- Make sure the group chat ID in `.env` is correct.
- If the group was upgraded to a supergroup, get the new ID again via `/chatid`.

### Problem: the bot does not react after `/start`
Solution:
- Check that the bot is actually running in the terminal.
- Check the token in `.env`.
- Restart the bot.