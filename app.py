from agent import generateTweet
from main import post_on_twitter
import schedule
import time
import random
import json

# Define time slots (24-hour format)
tweet_times = ["11:00", "15:00", "19:00", "23:00"]

# Define Promotional Lines
promo_lines = [
    "Learn Arabic with fun & ease with Fluentyx!",
    "Boost your Arabic vocabulary daily!",
    "Discover Arabic, unlock new worlds!",
    "Fluentyx makes Arabic learning simple.",
    "Start mastering Arabic today at Fluentyx!",
    "Speak Arabic, connect deeper.",
    "Learn Arabic naturally with Fluentyx!",
    "Learning Arabic? We’ve got you covered!"
]

# Format and post tweet
def run():
    try:
        tweet_data = generateTweet()
        print(tweet_data)

        # Parse if it's a JSON string
        if isinstance(tweet_data, str):
            tweet_data = json.loads(tweet_data)

        # Extract first item if it's a list
        if isinstance(tweet_data, list):
            tweet_data = tweet_data[0]

        question = tweet_data["question"]
        options = tweet_data["options"]

        promo = random.choice(promo_lines)
        link = "fluentyx.vercel.app"

        formatted_tweet = f"{question}\n\n"
        for i, opt in enumerate(options):
            formatted_tweet += f"{chr(65+i)}) {opt}\n"
            
        formatted_tweet += f"\n{promo}\n{link}"

        post_on_twitter(formatted_tweet.strip())
        print("Tweet posted successfully.")
    except Exception as e:
        print(f"Error: {e}")

# # Schedule for each time
# for t in tweet_times:
#     schedule.every().day.at(t).do(run)

# # Keep running
# while True:
#     schedule.run_pending()
#     time.sleep(30)


if __name__ == "__main__":
    run()