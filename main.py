import requests
import time
import os

# --- SETTINGS ---
# In tokens ko aap Railway ke "Variables" tab mein add karenge
FB_PAGE_ID = os.getenv('FB_PAGE_ID')
FB_PAGE_ACCESS_TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN')
CRICBUZZ_API_URL = "YOUR_CRICBUZZ_API_LINK_HERE" # Apna API link yahan dalein

def get_cricket_score():
    try:
        # Cricbuzz ya kisi bhi API se data uthana
        response = requests.get(CRICBUZZ_API_URL)
        data = response.json()
        # Yahan aap score ko text format mein convert karenge
        # Misal ke taur par:
        score_text = f"Live Score Update:\n{data.get('score', 'No live match right now.')}"
        return score_text
    except Exception as e:
        print(f"Error fetching score: {e}")
        return None

def post_to_facebook(message):
    url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
    payload = {
        'message': message,
        'access_token': FB_PAGE_ACCESS_TOKEN
    }
    try:
        r = requests.post(url, data=payload)
        print(f"Post Response: {r.text}")
    except Exception as e:
        print(f"Error posting to FB: {e}")

# --- MAIN LOOP (Lifetime Run) ---
if __name__ == "__main__":
    print("Bot is starting...")
    while True:
        score = get_cricket_score()
        if score:
            post_to_facebook(score)
            print("Successfully posted at:", time.ctime())
        
        # 15 Minute Wait (900 seconds)
        print("Waiting for 15 minutes...")
        time.sleep(900)
