import requests
import json

class Meme:
    def __init__(self, title, image_url, source):
        self.Title = title
        self.ImageUrl = image_url
        self.Source = source

def get_memes_from_reddit(subreddit, amount):
    memes = []

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"
    }

    endpoint = f"https://www.reddit.com/r/{subreddit}/.json?limit={amount}"
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        reddit_response = json.loads(response.text)

        for child in reddit_response["data"]["children"]:
            meme = Meme(
                title=child["data"]["title"],
                image_url=child["data"]["url"],
                source=child["data"]["permalink"]
            )
            print(meme.ImageUrl)
            memes.append(meme)
    else:
        print(f"Error: {response.status_code} - {response.reason}")

    return memes

def send_memes_to_discord_webhook(memes, webhook):
    webhook_url = webhook

    for meme in memes:
        message = {
            "content": f"{meme.Title} {meme.ImageUrl}"
        }
        embed = {
            "title": meme.Title,
            "image": {
                "url": meme.ImageUrl
            }
        }

        data = {
            "content": json.dumps(message),
            "embeds": [embed]
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(webhook_url, data=json.dumps(data), headers=headers)

def main():
    webhook = input("Enter your Discord webhook: ")
    is_webhook = webhook.startswith("https://discord.com/api/webhooks")

    while not is_webhook:
        print("Invalid input (valid example input: https://discord.com/api/webhooks...)")
        webhook = input("Enter your Discord webhook: ")
        is_webhook = webhook.startswith("https://discord.com/api/webhooks")

    subreddit = input("Enter subreddit: ")
    amount = int(input("Enter amount: "))

    try:
        memes = get_memes_from_reddit(subreddit, amount)
        webhook = webhook.strip()
        send_memes_to_discord_webhook(memes, webhook)
    except Exception as e:
        print("You are being rate limited. Try requesting a lower amount of posts. The posts won't send to the webhook")

if __name__ == "__main__":
    main()