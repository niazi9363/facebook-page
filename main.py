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
            for match in data['results']:
                series = match.get('series_name', '')
                home_team = match.get('home_team_name', '')
                away_team = match.get('away_team_name', '')
                
                # --- TARGET FILTER ---
                # International keywords + Pakistan/Australia takay match miss na ho
                target_keywords = ["International", "ICC", "T20I", "ODI", "Test", "World Cup", "Pakistan", "Australia", "PAK", "AUS"]
                
                # Check karega ke series ya teams mein koi target lafz hai?
                is_match_found = any(word.lower() in (series + home_team + away_team).lower() for word in target_keywords)
                
                if is_match_found:
                    status = match.get('status', 'Live')
                    score_text = f"🏏 Live Match Update:\n🏆 {series}\n⚔️ {home_team} vs {away_team}\n📢 Status: {status}"
                    return score_text
            
            return "No Target (International/PAK/AUS) matches live right now."
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
    print("Bot is starting with Pakistan/Australia & International Filter...")
    while True:
        score = get_cricket_score()
        
        # Sirf tab post karega jab "Live Match Update" wala text milega
        if score and "Live Match Update" in score:
            post_to_facebook(score)
            print("Successfully posted score at:", time.ctime())
        else:
            print(f"Skipping: {score}")
        
        print("Waiting for 30 minutes...")
        time.sleep(1800) # 30 minutes
