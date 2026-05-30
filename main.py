import requests
import time
import os

# --- SETTINGS ---
FB_PAGE_ID = os.getenv('FB_PAGE_ID')
FB_PAGE_ACCESS_TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN')

# Nayi API details (Zyada stable aur asaan)
API_KEY = "a82aedbb32msh60b092ca8d33832p1230d3jsnab12f1b758b9"
URL = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

def get_cricket_score():
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }
    try:
        response = requests.get(URL, headers=headers)
        data = response.json()
        
        # Logs check karne ke liye
        print("API Response Check:", data)

        if 'typeMatches' in data:
            for match_type in data['typeMatches']:
                for series_data in match_type.get('seriesMatches', []):
                    series_name = series_data.get('seriesAdWrapper', {}).get('seriesName', 'Cricket Series')
                    
                    for match in series_data.get('seriesAdWrapper', {}).get('matches', []):
                        home = match.get('team1', {}).get('teamName', 'Team A')
                        away = match.get('team2', {}).get('teamName', 'Team B')
                        status = match.get('status', 'Live')
                        
                        # Pakistan ya Australia ka match filter
                        target_keywords = ["pak", "aus", "australia", "pakistan", "international"]
                        full_info = (series_name + home + away).lower()
                        
                        if any(word in full_info for word in target_keywords):
                            score_text = f"🏏 Live Match Alert:\n🏆 {series_name}\n⚔️ {home} vs {away}\n📢 Status: {status}"
                            return score_text
            
            return "No PAK/AUS matches live right now on Cricbuzz."
        return "No matches found."
    except Exception as e:
        print(f"Error: {e}")
        return None

def post_to_facebook(message):
    fb_url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
    payload = {'message': message, 'access_token': FB_PAGE_ACCESS_TOKEN}
    try:
        r = requests.post(fb_url, data=payload)
        print(f"FB Post Response: {r.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Bot is starting with Cricbuzz API...")
    while True:
        score = get_cricket_score()
        if score and "Live Match" in score:
            post_to_facebook(score)
            print("Successfully posted score!")
        else:
            print(f"Skipping: {score}")
        
        print("Waiting 15 minutes...")
        time.sleep(900)
