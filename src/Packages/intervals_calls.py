import requests

BASE_URL = 'https://intervals.icu/api/v1'

def get_recent_activities(auth: str, oldest: str, latest: str):
    """
    Pulls recent activities oldest, newest dates should be formatted YYYY-MM-DD
    """

    resp = requests.get(url=f"{BASE_URL}/athlete/0/activities", params={"oldest": oldest.strftime("%Y-%m-%d"), "newest": latest.strftime("%Y-%m-%d")}, auth=auth)
    resp.raise_for_status()
    return resp.json()

    
   

