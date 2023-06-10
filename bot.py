import discord
import tweepy
import asyncio
import time

# Twitter API Credentials
consumer_key = 'YOUR_TWITTER_CONSUMER_KEY'
consumer_secret = 'YOUR_TWITTER_CONSUMER_SECRET'
access_token = 'YOUR_TWITTER_ACCESS_TOKEN'
access_token_secret = 'YOUR_TWITTER_ACCESS_SECRET'

# Discord Credentials
DISCORD_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
CHANNEL_ID = 'YOUR_DISCORD_CHANNEL_ID' 

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Authenticate to Discord
client = discord.Client()

tracked_users = {}  # To keep track of followed users by tracked users

async def check_followings():
    while True:
        for user in tracked_users.keys():
            try:
                # Fetch the IDs of the users that the user is following.
                current_following_ids = api.friends_ids(user)
                for following_id in current_following_ids:
                    # If this ID wasn't in the list before
                    if following_id not in tracked_users[user]:
                        tracked_users[user].append(following_id)
                        new_followed_user = api.get_user(following_id)
                        profile_info = f"Name: {new_followed_user.name}\nBio: {new_followed_user.description}\n" \
                                       f"Profile Picture URL: {new_followed_user.profile_image_url}\n" \
                                       f"Followers Count: {new_followed_user.followers_count}\n" \
                                       f"Tweets Count: {new_followed_user.statuses_count}\n"

                        channel = client.get_channel(CHANNEL_ID)
                        await channel.send(f'@{user} has just followed a new user: @{new_followed_user.screen_name}.\n{profile_info}')

            except Exception as e:
                print(f"Error: {str(e)}")
        time.sleep(300)  # wait for 5 minutes

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    client.loop.create_task(check_followings())

client.run(DISCORD_TOKEN)
