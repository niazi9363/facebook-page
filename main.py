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
        
        if data.get('results'):
            # Pehla live match uthana
            match = data['results'][0]
            series = match.get('series_name', 'Cricket Match')
            team1 = match.get('home_team_name', 'Team A')
            team2 = match.get('away_team_name', 'Team B')
            status = match.get('status', 'Live')
            
            score_text = f"🏏 Live Update:\n🏆 {series}\n⚔️ {team1} vs {team2}\n📢 Status: {status}"
            return score_text
        return "No live matches at the moment."
    except Exception as e:
        print(f"Error fetching score: {e}")
        return None

def post_to_facebook(message):
    fb_url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
    payload = {'message': message, 'access_token': FB_PAGE_ACCESS_TOKEN}
    try:
        r = requests.post(fb_url, data=payload)
        print(f"Post Response: {r.text}")
    except Exception as e:
        print(f"Error posting to FB: {e}")

if __name__ == "__main__":
    print("Bot is starting...")
    while True:
        score = get_cricket_score()
        if score:
            post_to_facebook(score)
            print("Successfully posted at:", time.ctime())
        
        print("Waiting for 15 minutes...")
        time.sleep(900)
