import streamlit as st
from streamlit_calendar import calendar
import datetime
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Packages.intervals_calls import get_recent_activities
from Packages.models import normalize_activity, AthleteProfile, TrainingPlan
from Packages.testprofile import test_ride
from Packages.gemini_parser import generate_plan

import json
from pathlib import Path

load_dotenv()

st.set_page_config(page_title="AI Bike Coach")

# Initialize session state
if "profile_saved" not in st.session_state:
    st.session_state.profile_saved = False
if "profile" not in st.session_state:
    st.session_state.profile = None
if "plan" not in st.session_state:
    st.session_state.plan = None

# Profile sidebar
st.sidebar.title("Athlete Profile")
with st.sidebar.form(key="athlete_profile_form"):
    ftp = st.number_input(label="FTP",min_value=50, max_value=600, value=220)
    vo2_max = st.number_input(label=r"VO2 Max Power (typically between 106-120% of FTP)",value=360, min_value=0, max_value=1000,step=10)
    max_hr = st.number_input(label="Max Heartrate",min_value=120, max_value=205, value=198)
    resting_hr = st.number_input(label="Resting Heartrate", min_value=20, max_value=140, value=50)
    max_power = st.number_input(label="Max Power", min_value=100, max_value=3000, value=1400)
    goal = st.text_area(label="What is your goal? (400 character limit)", max_chars=400)
    goal_date = st.date_input("Goal date", min_value=datetime.date.today()+datetime.timedelta(days=2), value=datetime.date.today() + datetime.timedelta(weeks=4))
    weekly_hours = st.number_input(label="How many hours do you have available per week for training?",value=10, min_value=1, max_value=42,step=1)
    st.write("What days are available during the week?")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    selected = {day: st.checkbox(day) for day in days}
    days_available = [day for day, checked in selected.items() if checked]    
    experience_level = st.selectbox(label="What's your experience level?",options=["Beginner","Intermediate","Expert"])
    st.write("Ride fetch range")
    oldest_date = st.date_input(label="From", value=datetime.date.today()-datetime.timedelta(weeks=4),max_value=datetime.date.today() - datetime.timedelta(days=1), min_value=datetime.date.today()-datetime.timedelta(weeks=8))
    latest_date = st.date_input(label="To", value=datetime.date.today(), max_value=datetime.date.today(), min_value=oldest_date)
    # When pressed, save the attributes to the Athlete's Profile
    save_button = st.form_submit_button(label="Save")

# Upon saving form:
if save_button:
    st.session_state.profile ={
        "id" : None,
        "ftp": ftp,
        "max_hr": max_hr,
        "resting_hr": resting_hr,
        "vo2_max" :vo2_max,
        "max_power": max_power,
        "goal": goal,
        "goal_date": goal_date,
        "weekly_hours": weekly_hours,
        "days_available": days_available,
        "experience_level": experience_level,
        "oldest_date": oldest_date,
        "latest_date": latest_date,
        "rides": None
    }
    # Change session profile state
    st.session_state.profile_saved = True
    st.sidebar.success("Profile saved!")

# If the user wants to test the app
use_test_athlete = st.sidebar.toggle("Use test athlete")

if use_test_athlete:
    st.session_state.profile = {
        "id" : None,
        "ftp": 248,
        "max_hr": 192,
        "vo2_max": 390,
        "resting_hr": 49,
        "max_power": 400,
        "goal": "Win a category 4 Criterium race",
        "goal_date": datetime.date.today()+datetime.timedelta(weeks=4), 
        "weekly_hours": 9,
        "days_available": ["Tuesday", "Thursday", "Friday", "Sunday"],
        "experience_level": "Beginner",
        "oldest_date": None,   # signals to skip Intervals.icu fetch
        "latest_date": None,
        "rides": None
    }
    st.session_state.profile_saved = True
    st.sidebar.success("Test athlete loaded!")

# Main page
st.title("AI Bike Coach - Training Plan Generator")
st.write("Welcome to my AI bike coach app. To start, fill out your profile on the sidebar.\n After filling out your profile, hit save and you're ready to generate your personalized training plan!\n To note, this app currently assumes you've used and posted a ride to intervals.icu.")



generate = st.button("Generate Plan", use_container_width=True)

if generate:
    # Stop if there's no profile saved
    if not st.session_state.profile_saved:
        st.warning("Please fill out and save your profile first.")
        st.stop()
    
    profile = st.session_state.profile

    # If test athlete is chosen (checked by the flagged none date)
    if profile['oldest_date'] is None:
        profile['rides'] = [test_ride()] 
        st.success(f"Loaded Test Ride.")
        profile['id'] = 'i1'  
    else:
        try:
        # fetch from Intervals.icu using profile dates
            auth = ("API_KEY", os.getenv("INTERVALS_API_KEY"))
            rides = [normalize_activity(r) for r in get_recent_activities(auth, profile["oldest_date"], profile["latest_date"])]
            profile['rides'] = rides
            profile['id'] = os.getenv("INTERVALS_ID")
            st.success(f"Fetched {len(rides)} rides.")
        except Exception as e:
            st.error(f"Failed to fetch rides: {e}")
            st.stop()

    ath_profile = AthleteProfile(
                                id=profile['id'],
                                ftp=profile['ftp'],
                                max_hr=profile['max_hr'],
                                resting_hr=profile['resting_hr'],
                                vo2_max=profile['vo2_max'],
                                max_power=profile['max_power'],
                                goal=profile['goal'],
                                goal_date=profile['goal_date'],
                                weekly_hours=profile['weekly_hours'],
                                days_available=profile['days_available'],
                                experience_level=profile['experience_level'],
                                rides=profile['rides']
            )    
    st.write("Generating plan")
    st.session_state.plan = generate_plan(ath_profile)
    st.success("Plan generated")
    save_plan = st.button(label="Save Plan")
    if save_plan:
        Path("Plans").mkdir(exist_ok=True)
        data_to_save = {
            "profile": st.session_state.profile,
            "plan": st.session_state.plan.model_dump(),
        }
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"Plans/saved_data_{timestamp}.json", "w") as f:
            json.dump(data_to_save, f, default=str)
        st.success("Saved plan to the 'Plans' folder")

st.write("OR you can load your most recently saved plan by hitting the load plan button")
load_plan = st.button(label="Load Plan",use_container_width=True)

if load_plan:
    folder_path = Path("Plans")
    files = [f for f in folder_path.iterdir() if f.is_file()] if folder_path.is_dir() else []
    if files:
        most_recent_file = max(files, key=lambda f: f.stat().st_mtime)
        with open(most_recent_file, "r") as file:
            loaded_data = json.load(file)
            st.session_state.profile = loaded_data["profile"]
            st.session_state.plan = TrainingPlan.model_validate(loaded_data["plan"])
            st.session_state.profile_saved = True
    else:
        st.error("No Saved Plans")
        st.stop()

plan = st.session_state.plan

if plan:
    st.divider()
    st.subheader("Your Training Plan")
    st.write(plan.summary)
    st.divider()

    # Map workout types to colors
    COLORS = {
        "endurance": "#3b82f6",    # blue
        "intervals": "#ef4444",    # red
        "tempo": "#f97316",        # orange
        "threshold": "#381B07",    # brown
        "recovery": "#22c55e",     # green
        "rest": "#6b7280",         # gray
        "long ride": "#8b5cf6",    # purple
        "race": "#fbbf24",         # yellow
    }

    def get_color(workout_type: str) -> str:
        return COLORS.get(workout_type.lower(), "#3b82f6")   

    events = []
    for week in plan.weeks:
        for workout in week.workouts:
            events.append({
                "title": f"{workout.type.title()} | {workout.duration_min}min",
                "start": workout.date if isinstance(workout.date, str) else workout.date.strftime("%Y-%m-%d"),
                "end": workout.date if isinstance(workout.date, str) else workout.date.strftime("%Y-%m-%d"),
                "color": get_color(workout.type),
                "extendedProps": {
                    "intensity": workout.intensity,
                    "purpose": workout.purpose,
                    "duration": workout.duration_min,
                    "type": workout.type,
                    "intervals": workout.intervals.model_dump() if workout.intervals else None
                }
            })

    calendar_options = {
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,dayGridWeek"
        },
        "initialView": "dayGridMonth",
        "editable": False,
        "selectable": False,
        "eventDisplay": "block",
    }

    cal = calendar(events=events, options=calendar_options, key="training_calendar")

    if cal and cal.get("eventClick"):
        event = cal["eventClick"]["event"]
        props = event.get("extendedProps", {})

        st.markdown(f"### {event['title']}")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Duration", f"{props.get('duration')} min")
        with col2:
            st.metric("Intensity", props.get("intensity"))

        st.write(f"**Purpose:** {props.get('purpose')}")

        intervals = props.get("intervals")
        if intervals:
            st.divider()
            st.write("**Interval Instructions**")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Target Power", f"{intervals.get('target_watt')}W")
            with col2:
                st.metric("% FTP", f"{intervals.get('percent_ftp')}%")
            st.info(intervals.get("instructions"))
    
    st.divider()
    st.subheader("Weekly Breakdown")
    for week in plan.weeks:
        with st.expander(week.label, expanded=False):
            for workout in week.workouts:
                color = get_color(workout.type)
                st.markdown(
                    f"""
                    <div style="
                        border-left: 4px solid {color};
                        padding: 8px 12px;
                        margin-bottom: 8px;
                        border-radius: 4px;
                        background-color: rgba(0,0,0,0.05)
                    ">
                        <strong>{workout.day} {workout.date}</strong> — 
                        {workout.type.title()} | {workout.duration_min} min |
                        {workout.intensity}<br/>
                        {f"{workout.intervals.percent_ftp} % FTP @ {workout.intervals.target_watt} Watts | {workout.intervals.instructions}<br/>" if workout.intervals else "No Intervals <br/>"}
                        {workout.purpose}
                    </div>
                    """,
                    unsafe_allow_html=True
                )