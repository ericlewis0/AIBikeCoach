from .models import AthleteProfile, RideSummary, normalize_activity
import json
from datetime import date

def test_athlete() -> AthleteProfile:
    test_ride = RideSummary(
        id='1001',
        athlete_id='i1',
        date=date(2026, 6, 20),
        name="Morning Crit Simulation",
        type="Ride",
        training_load=98,
        acute_load=72.4,
        chronic_load=58.1,
        ftp_at_time=248,
        joules=542000,
        elevation_gain=210.5,
        normalized_power=241,
        distance_km=38.4,
        duration_min=68.5,
        max_heartrate=189,
        average_heartrate=162.0,
        average_cadence=88.3,
        perceived_exertion=7.5,
        interval_summary=[
            "3x 2m00s 285w",
            "2x 30s 420w",
            "1x 5m00s 255w",
            "4x 1m00s 310w"
        ],
        power_zone_times=[
            {"id": "Z1", "secs": 820},
            {"id": "Z2", "secs": 1040},
            {"id": "Z3", "secs": 680},
            {"id": "Z4", "secs": 920},
            {"id": "Z5", "secs": 540},
            {"id": "Z6", "secs": 380},
            {"id": "Z7", "secs": 230}
        ],
        hr_zone_times=[740, 1210, 580, 890, 440, 250, 0],
        polarization_index=1.62,
        decoupling=5.2,
        hr_load=61,
        hr_load_type="HRSS",
        intensity=97.2,
        efficiency_factor=1.31,
        average_watts=132.0,
        variablility_index=1.28,
        strain_score=318.7
    )
    
    with open(R"C:\Users\ericl\Desktop\PersonalProjects\AIBikeCoachProject\src\Packages\test_ride.json", 'r', encoding='utf-8') as file:
        raw_ride = json.load(file)
    
    return AthleteProfile(
        id='1',
        max_hr=192,
        resting_hr=49,
        ftp=250,
        vo2_max=400,
        max_power=1300,
        goal="Win a category 3 Criterium race on July 21st, 2026",
        weekly_hours=13,
        days_available= "Monday, Tuesday, Thursday, Friday, Sunday",
        experience_level='Intermediate',
        rides=[test_ride, normalize_activity(raw=raw_ride)]
    )


def test_ride() -> RideSummary:
    return RideSummary(
        id='1001',
        athlete_id='i1',
        date=date(2026, 6, 20),
        name="Morning Crit Simulation",
        type="Ride",
        training_load=98,
        acute_load=72.4,
        chronic_load=58.1,
        ftp_at_time=248,
        joules=542000,
        elevation_gain=210.5,
        normalized_power=241,
        distance_km=38.4,
        duration_min=68.5,
        max_heartrate=189,
        average_heartrate=162.0,
        average_cadence=88.3,
        perceived_exertion=7.5,
        interval_summary=[
            "3x 2m00s 285w",
            "2x 30s 420w",
            "1x 5m00s 255w",
            "4x 1m00s 310w"
        ],
        power_zone_times=[
            {"id": "Z1", "secs": 820},
            {"id": "Z2", "secs": 1040},
            {"id": "Z3", "secs": 680},
            {"id": "Z4", "secs": 920},
            {"id": "Z5", "secs": 540},
            {"id": "Z6", "secs": 380},
            {"id": "Z7", "secs": 230}
        ],
        hr_zone_times=[740, 1210, 580, 890, 440, 250, 0],
        polarization_index=1.62,
        decoupling=5.2,
        hr_load=61,
        hr_load_type="HRSS",
        intensity=97.2,
        efficiency_factor=1.31,
        average_watts=132.0,
        variablility_index=1.28,
        strain_score=318.7
    )

if __name__== '__main__':
    athlete = test_athlete()