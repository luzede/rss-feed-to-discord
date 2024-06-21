import requests
import feedparser
from markdownify import markdownify
from discord_webhook import DiscordWebhook, DiscordEmbed
from inspect import getsourcefile
from os import path
import time
import datetime
from dotenv import dotenv_values

# Get the directory of this file
current_dir = path.dirname(path.abspath(getsourcefile(lambda: 0)))

config = dotenv_values(path.join(current_dir, ".env"))

response = requests.get(config["FEED_URL"])

try:
    with open(path.join(current_dir, "last_known_post_date.txt"), "r") as f:
        last_known_post_date = time.strptime(f.read(), "%Y-%m-%dT%H:%M:%SZ")
        print(last_known_post_date)
except FileNotFoundError:
    last_known_post_date = None


feed = feedparser.parse(response.content)

posts_for_discord = []
latest_post_date = last_known_post_date

for entry in feed.entries:
    # Finding the latest post date in the feed
    if latest_post_date is None or entry.published_parsed > latest_post_date:
        latest_post_date = entry.published_parsed
    # Checking if the post is already sent by comparing the post date with the last known sent post date
    if (
        last_known_post_date is not None
        and entry.published_parsed <= last_known_post_date
    ):
        continue

    posts_for_discord.append(
        DiscordEmbed(
            title=entry.title,
            url=entry.link,
            description=markdownify(
                "".join(map(lambda c: c.value, entry.content))
                if "content" in entry
                else entry.description,
                strip=["img"],
            ),
            timestamp=datetime.datetime.fromtimestamp(
                time.mktime(entry.published_parsed)
            ),
            color=0x58B9FF,
        )
    )

with open(path.join(current_dir, "last_known_post_date.txt"), "w") as f:
    f.write(time.strftime("%Y-%m-%dT%H:%M:%SZ", latest_post_date))

print()

webhook = DiscordWebhook(
    url=config["DISCORD_CHANNEL_WEBHOOK_URL"],
    rate_limit_retry=True,
)

while len(posts_for_discord) > 0:
    webhook.add_embed(posts_for_discord.pop())
    webhook.execute(remove_embeds=True)
