from .models import AthleteProfile
from datetime import date

def build_prompt(profile: AthleteProfile) -> str:
    '''
    Builds prompt, includes the ride attributes, the athlete's profile, and instructions for the ai 
    
    Parameters:
      profile - AthleteProfile
    
    Returns:
      the built prompt
    '''
    today = date.today()
    # TODO make a prompt builder to where it'll ignore NULL attributes
    rides_text = "\n".join(
        f"- {r.date}: {r.name}, {r.duration_min} min, {r.distance_km} km, "
        f"training load: {r.training_load}, acute_load: {r.acute_load}, chronic_load: {r.chronic_load}, "
        f"ftp at the time: {r.ftp_at_time}W, work: {round(r.joules / 1000) if r.joules is not None else 'N/A'}, climbing (ft): {r.elevation_gain}, "
        f"normalized power: {r.normalized_power}, max heartrate: {r.max_heartrate}, "
        f"average heartrate: {r.average_heartrate}, average cadence: {r.average_cadence}, perceived extertion: {r.perceived_exertion}, "
        f"interval summary: {r.interval_summary}, seconds in power zones: {r.power_zone_times}, "
        f"heartrate zone times (Z1-Z7): {r.hr_zone_times}, polarization: {r.polarization_index}, decoupling: {r.decoupling}, "
        f"heartrate load: {r.hr_load}, heartrate load type: {r.hr_load_type}, intensity: {r.intensity}, efficiency factor: {r.efficiency_factor}, "
        f"average wattage: {r.average_watts}, variability: {r.variablility_index}, strain score: {r.strain_score}"
        for r in profile.rides
    )
    return f"""Build a personalized training plan for the following Athlete.

    ATHLETE PROFILE
    FTP: {profile.ftp}W
    Max HR: {profile.max_hr}
    Resting HR: {profile.resting_hr}
    VO2 Max: {profile.vo2_max}
    Max Power: {profile.max_power}W
    Goal: {profile.goal}
    Goal Date: {profile.goal_date}
    Weekly hours available: {profile.weekly_hours}
    Day's available: {profile.days_available}
    Experience: {profile.experience_level}
    Today's Date: {today.strftime( "%B %d, %Y")}

    RECENT RIDES (last 7 days)
    {rides_text}

    INSTRUCTIONS
    1. Build a week-by-week training plan from today up to and including the race week.
    2. Each week is a list of workout objects, one per available training day.
    3. If the first or last week is partial (fewer than usual available days), include only the remaining available days in that week.
    4. Each training week will start on Monday and end on Sunday. 
    5. Label each week clearly: "Week 1 (Jul 3–5)", "Week 2 (Jul 6–12)", ... , "Race Week (Aug 3–9)" etc.
    6. For interval sessions, set "intervals" to an object with the target % of FTP, target wattage, and very brief detail on how to perform them. For non-interval sessions, set "intervals" to null.
    7. You don't need to fulfill every available day with a ride, ex. when leading up to a race
    Return ONLY valid JSON matching this structure:
    {{
  "summary": "paragraph explaining the overall plan focus and periodization",
  "weeks": [
    {{
      "label": "Week 1 (Jul 3–5)",
      "workouts": [
        {{
          "date": "2026-07-03",
          "day": "Thursday",
          "type": "endurance",
          "duration_min": 60,
          "intervals": null,
          "intensity": "Zone 2",
          "purpose": "aerobic base building"
        }},
        {{
          "date": "2026-07-04",
          "day": "Friday",
          "type": "intervals",
          "duration_min": 75,
          "intervals": {{
            "percent_ftp": 105,
            "target_watt": 260,
            "instructions": "6x4min @ target watt, 3min recovery between reps"
          }},
          "intensity": "Zone 4",
          "purpose": "threshold development"
        }}
      ]
    }}
  ]
}}"""