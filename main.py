import requests
import time
import os

# --- SETTINGS ---
FB_PAGE_ID = os.getenv('FB_PAGE_ID')
FB_PAGE_ACCESS_TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN')
API_KEY = "a82aedbb32msh60b092ca8d33832p1230d3jsnab12f1b758b9"
URL = "https://cricket-live-data.p.rapidapi.com/match/live"

def get_cricket_score():
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "cricket-live-data.p.rapidapi.com"
    }
    try:
        response = requests.get(URL, headers=headers)
        data = response.json()
        
        # Logs mein check karne ke liye ke API kya bhej rahi hai
        print("Raw API Response:", data)

        if data.get('results') and len(data['results']) > 0:
            # Test ke liye: Pehla jo bhi match mile usay uthao
            match = data['results'][0]
            series = match.get('series_name', 'Cricket Series')
            home = match.get('home_team_name', 'Team A')
            away = match.get('away_team_name', 'Team B')
            status = match.get('status', 'Live')
            
            score_text = f"🏏 Cricket Test Update:\n🏆 {series}\n⚔️ {home} vs {away}\n📢 Status: {status}"
            return score_text
            
        return "API Results list is empty right now."
    except Exception as e:
        print(f"Error fetching score: {e}")
        return None

def post_to_facebook(message):
    fb_url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
    payload = {'message': message, 'access_token': FB_PAGE_ACCESS_TOKEN}
    try:
        r = requests.post(fb_url, data=payload)
        print(f"FB Post Response: {r.text}")
    except Exception as e:
        print(f"Error posting to FB: {e}")

if __name__ == "__main__":
    print("Bot is in TEST MODE - Posting any available match...")
    while True:
        score = get_cricket_score()
        
        if score and "Cricket Test Update" in score:
            post_to_facebook(score)
            print("Successfully posted at:", time.ctime())
        else:
            print(f"Skipping: {score}")
        
        # Test ke liye 2 minute ka wait taake foran result dikhe
        print("Waiting 2 minutes...")
        time.sleep(120)
