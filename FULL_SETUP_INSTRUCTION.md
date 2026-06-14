# Full setup instruction for launching the Telegram bot

## 1. Requirements

To launch the Telegram bot, you need:
- Python 3.11 or newer
- a Telegram account
- Internet access
- a command line or terminal

The commands below are provided separately for **macOS/Linux** and **Windows**.

## 2. Prepare the project

After receiving the archive with the program, unzip it and open the project folder in Terminal or Command Prompt.

Example:

### macOS / Linux
```bash
cd ~/Desktop/ceifbankstp_bot
```

### Windows
```bat
cd %USERPROFILE%\Desktop\ceifbankstp_bot
```

## 3. Create a Telegram bot

To create the bot:

1. Open Telegram.
2. Find **@BotFather**.
3. Send the command:
```text
/newbot
```
4. Enter the display name of the bot.
5. Enter a unique username for the bot. The username must end with `bot`.
6. BotFather will return a unique bot token. Save it.

Example token format:

```text
123456789:AAExampleExampleExampleExampleExample
```

If necessary, you can also configure the bot in BotFather:
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

## 4. Create a staff group for administrators

For the administrative workflow, create a separate Telegram group for bank staff or administrators.

Then:
1. add the bot to the group;
2. preferably make the bot an administrator;
3. keep the bot in the group if you want to use admin commands permanently.

This group will be used for:
- receiving notifications about new applications;
- using administrative commands.

## 5. Get the admin chat ID

After the bot is launched for the first time, send the command `/chatid` **inside the staff group**.

The bot will reply with the current group chat ID. This value must later be written into the `.env` file as `ADMIN_CHAT_ID`.

For supergroups the ID usually looks like this:

```text
-1001234567890
```

## 6. Create a virtual environment

In the project folder create a virtual environment.

### macOS / Linux
```bash
python3 -m venv venv
```

### Windows
```bat
python -m venv venv
```

## 7. Activate the virtual environment

After creating the environment, activate it.

### macOS / Linux
```bash
source venv/bin/activate
```

### Windows (Command Prompt)
```bat
venv\Scripts\activate
```

### Windows (PowerShell)
```powershell
venv\Scripts\Activate.ps1
```

If activation is successful, your terminal prompt will begin with `(venv)`.

## 8. Install dependencies

After activation, install the project dependencies.

### macOS / Linux
```bash
pip install -r requirements.txt
```

### Windows
```bat
pip install -r requirements.txt
```

## 9. Create the configuration file

Create the `.env` file from the `.env.example` template.

### macOS / Linux
```bash
cp .env.example .env
```

### Windows (Command Prompt)
```bat
copy .env.example .env
```

### Windows (PowerShell)
```powershell
Copy-Item .env.example .env
```

Then open `.env` for editing.

### macOS / Linux
```bash
nano .env
```

### Windows
Use one of the following:
- Notepad
- Visual Studio Code
- Notepad++
- or:
```bat
notepad .env
```

Insert the bot token and the admin chat ID.

At the first stage, if you do not know the admin group ID yet, leave `ADMIN_CHAT_ID` empty.

Example:

```env
BOT_TOKEN=PASTE_YOUR_REAL_BOT_TOKEN_HERE
ADMIN_CHAT_ID=
```

## 10. First launch of the program

Run the bot for the first time.

### macOS / Linux
```bash
python3 run.py
```

### Windows
```bat
python run.py
```

If the configuration and dependencies are correct, the bot will start and wait for messages.

After that:
1. open the bot in Telegram;
2. press **Start** or send `/start`;
3. check that the bot sends a welcome message.

## 11. Get your personal and group identifiers

In the personal chat with the bot send:

```text
/myid
```

The bot will show:
- your Telegram user ID;
- the current personal chat ID.

In the staff group send:

```text
/chatid
```

The bot will show the group chat ID.

Then stop the program.

### macOS / Linux
```text
Control + C
```

### Windows
```text
Ctrl + C
```

Open `.env` again and insert the received group ID:

```env
BOT_TOKEN=PASTE_YOUR_REAL_BOT_TOKEN_HERE
ADMIN_CHAT_ID=YOUR_REAL_ADMIN_CHAT_ID
```

Then run the bot again.

### macOS / Linux
```bash
python3 run.py
```

### Windows
```bat
python run.py
```

## 12. Test the user scenario

To test the user workflow, open the bot in Telegram and complete the full application process:

1. start the bot;
2. choose to begin the application;
3. confirm that the application is submitted on behalf of a legal entity;
4. enter company data;
5. enter contact person data;
6. enter financing data;
7. attach files if needed;
8. confirm personal data processing consent;
9. confirm NCND;
10. check the final summary;
11. press the submit button.

If everything is configured correctly:
- the application will be saved in SQLite;
- the user will receive a success message;
- the staff group will receive a notification about the new application.

## 13. Test the admin functions

In the staff group test these commands:

```text
/applications
/application 1
/files 1
/setstatus 1 in_review
/bystatus in_review
```

The following statuses are used in the project:
- `new`
- `in_review`
- `contacted`
- `rejected`
- `approved_next_step`

## 14. Data storage

After the first successful launch and the first saved application, the program automatically creates a local SQLite database.

The database file is located at:

```text
data/applications.db
```

It stores:
- application data;
- information about attached files.

## 15. Stop the program

To stop the bot, use:

### macOS / Linux
```text
Control + C
```

### Windows
```text
Ctrl + C
```

## 16. Common problems and solutions

### Problem: `No module named 'aiogram'`

**Solution:**
1. Make sure the virtual environment is activated.
2. Install dependencies again:

### macOS / Linux
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Windows
```bat
venv\Scripts\activate
pip install -r requirements.txt
```

### Problem: `Bad Request: chat not found`

**Solution:**
- Make sure the bot is added to the staff group.
- Make sure the `ADMIN_CHAT_ID` in `.env` is correct.
- If the group was converted into a supergroup, get the new ID again using `/chatid`.

### Problem: the bot does not react after `/start`

**Solution:**
- Check that the program is actually running in the terminal.
- Check that the bot token in `.env` is correct.
- Restart the bot.

### Problem: PowerShell does not allow activating `venv`

**Solution:**
If Windows PowerShell blocks the activation script, either use Command Prompt (`cmd`) or temporarily allow script execution with:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
venv\Scripts\Activate.ps1
```
