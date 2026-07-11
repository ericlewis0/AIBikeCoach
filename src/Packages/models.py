from pydantic import BaseModel
from datetime import date

class RideSummary(BaseModel):
    id: str
    athlete_id: str
    date: date
    name: str
    type: str 
    training_load: int 
    acute_load: float
    chronic_load: float
    ftp_at_time: int
    joules: int | None = None
    elevation_gain: float
    normalized_power: int | None = None
    distance_km: float
    duration_min: float
    max_heartrate: int
    average_heartrate: float
    average_cadence: float
    perceived_exertion: float | None = None
    interval_summary: list[str] | None = None
    power_zone_times: list[dict] | None = None
    hr_zone_times: list[int]
    polarization_index: float
    decoupling: float | None = None
    hr_load: int
    hr_load_type: str
    intensity: float
    efficiency_factor: float | None = None
    average_watts: float | None = None
    variablility_index: float | None = None
    strain_score: float | None = None


class AthleteProfile(BaseModel):
    id: str | None = None # 'icu_athlete_id'
    max_hr: int # 'athlete_max_hr'
    resting_hr: int | None = None # 'icu_resting_hr' 
    ftp: int #'icu_ftp'
    vo2_max: int
    max_power: int #'p_max' 
    goal: str
    goal_date: date | None = None
    weekly_hours: int
    days_available: list[str]
    experience_level: str
    rides: list[RideSummary] | None = None

class Interval_info(BaseModel):
    percent_ftp: int
    target_watt: int
    instructions: str


class Workout(BaseModel):
    date: str
    day: str 
    type: str # endurance, intervals, recovery, tempo
    duration_min: int
    intervals: Interval_info | None = None
    intensity: str
    purpose: str # description/target zone

class Week(BaseModel):
    label: str
    # TODO total_hours: float
    workouts: list[Workout]


class TrainingPlan(BaseModel):
    summary: str
    weeks: list[Week]


def normalize_activity(raw: dict) -> RideSummary:
    workout_type = raw.get("type")
    if workout_type == "Ride" or workout_type == "VirtualRide":
        return RideSummary(
            id=raw['id'],
            athlete_id=raw['icu_athlete_id'],
            date=raw['start_date_local'][:10],
            type=raw["type"],
            name=raw.get("name", "Untitled Ride"),
            training_load=raw['icu_training_load'],
            acute_load=raw['icu_atl'],
            chronic_load=raw['icu_ctl'],
            ftp_at_time=raw['icu_ftp'],
            joules=raw['icu_joules'],
            elevation_gain=raw['total_elevation_gain'],
            normalized_power=raw['icu_weighted_avg_watts'],
            distance_km=round(raw['distance']/1000,2),
            duration_min=round(raw['moving_time']/60,2),
            max_heartrate=raw['max_heartrate'],
            average_heartrate=raw['average_heartrate'],
            average_cadence=raw['average_cadence'],
            perceived_exertion=raw['perceived_exertion'],
            interval_summary=raw['interval_summary'],
            power_zone_times=raw['icu_zone_times'],
            hr_zone_times=raw['icu_hr_zone_times'],
            polarization_index=raw['polarization_index'],
            decoupling=raw['decoupling'],
            hr_load=raw['hr_load'],
            hr_load_type=raw['hr_load_type'],
            intensity=raw['icu_intensity'],
            efficiency_factor=raw['icu_efficiency_factor'],
            average_watts=raw['icu_average_watts'],
            variablility_index=raw['icu_variability_index'],
            strain_score=raw['strain_score'],
            ath_max_hr=raw['athlete_max_hr'],
            ath_resting_hr=raw['icu_resting_hr'],
            ath_ftp=raw['icu_ftp'],
            ath_max_power=raw['p_max']
        )
    else:
        pass
