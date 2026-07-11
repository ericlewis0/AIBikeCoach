from .models import AthleteProfile, RideSummary
import random
from dotenv import load_dotenv
import os

load_dotenv()

def create_profile(rides: list[RideSummary]) -> AthleteProfile:
    '''
    Grabbing ftp, max_power, athlete id, etc. from the rides json 
    
    Also prompts the user for unattainable attributes
    '''
    # If there are rides, take the attributes for the profile from the latest ride, 
    # Otherwise, prompt the user for attributes to prevent NULLs
    latest_ride = max(rides, key=lambda obj: obj.date)

    if latest_ride: 
        max_hr = latest_ride.ath_max_hr
        resting_hr = latest_ride.ath_resting_hr
        ftp = latest_ride.ath_ftp
        max_power = latest_ride.ath_max_power
    else: 
        max_hr = input("Max Heartrate: ")
        resting_hr = input("Resting Heartrate: ")
        ftp = input("FTP: ")
        max_power = input("Max Power: ")

    vo2_max = input("VO2 Max : ")
    goal = input('Goal: ')
    weekly_hours = input("Hours per week available: ")
    days_available = input("Days available (""Monday, Wednesday,...""): ")
    experience_level = input("Experience level (Beginner, Intermediate, Expert): ")

    return AthleteProfile(
        id=os.getenv("INTERVALS_ID"),
        max_hr=max_hr,
        resting_hr=resting_hr,
        ftp=ftp,
        max_power=max_power,
        vo2_max=vo2_max,
        goal=goal,
        weekly_hours=weekly_hours,
        days_available=days_available,
        experience_level=experience_level,
        rides=rides
    )
