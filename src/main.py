from dotenv import load_dotenv
from Packages import get_recent_activities, create_profile, normalize_activity, generate_plan, test_athlete
from datetime import datetime, date, timedelta
import os

load_dotenv()

def athlete_plan():
    
    intervals_auth = ("API_KEY", os.getenv("INTERVALS_API_KEY"))    
    raw_activities = get_recent_activities(auth=intervals_auth, oldest=date.today() - timedelta(days=7), latest=date.today())
    rides = [normalize_activity(activity) for activity in raw_activities]
    
    profile = create_profile(rides=rides)
     
    plan = generate_plan(profile)
    print(plan.summary)
    for week in plan.weeks:
        print(week.label)
        for workout in week.workouts:
            print(f"{workout.date} {workout.day}: {workout.type} - {workout.duration_min} min - {workout.intensity} {workout.purpose}")

    print(f"Success! {datetime.now()}")


if __name__ == '__main__':
    athlete_plan()