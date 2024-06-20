# RSS Feed to Discord
This is a simple script that reads the feed from a site and outputs the content to a Discord channel through a channel webhook url.

## HOW TO RUN
Clone the repository and `cd` into it.
Then I recommend to create a virtual environment by running:
```bash
python -m venv env
source env/bin/activate
```
and install the required libraries:
```bash
pip install -r requirements.txt
```

Then all you have to do is create a `.env` file inside the cloned directory with following fields:
```bash
DISCORD_CHANNEL_WEBHOOK_URL="PASTE WEBHOOK URL HERE"
FEED_URL="PASTE RSS FEED URL HERE"
```
and run:
```
python main.py
```

## SETTING UP A CRON JOB
If you are using linux, you can set up a CRON job to run the script every so often.
This command opens CRONtab editor, if it is your first time using it, it will ask you to choose a default text editor. My usual choice is `nano` editor. Choose your default editor.
```bash
crontab -e
```
After that you can append something like this at the end of the file and save.
```
*/10 * * * * /path_to_cloned_directory/env/bin/python /path_to_cloned_directory/main.py
```
This will tell to run the script every 10 minutes.
