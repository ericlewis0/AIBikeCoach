# AI Bike Coach

A Streamlit app that generates a personalized cycling training plan using your Intervals.icu ride history and Google's Gemini API.

## Features

- Build an athlete profile (FTP, max/resting heart rate, max power, VO2 max, goal, available training days/hours, experience level) via a sidebar form
- Optionally load a built-in test athlete profile for quick trials without an Intervals.icu account
- Pull recent rides from [Intervals.icu](https://intervals.icu) for the profile's chosen date range
- Generate an AI-written multi-week training plan (summary, weekly breakdown, and per-workout intervals) via Gemini
- View the plan as a calendar of scheduled rides, plus an expandable weekly breakdown with workout details
- Save a generated plan to the `Plans/` folder as JSON, and reload the most recently saved plan later

## Project Structure

```
src/
  App/app.py             # Streamlit app entry point
  main.py                # CLI script that runs the plan pipeline and prints it
  Packages/
    models.py             # Pydantic models (AthleteProfile, RideSummary, Workout, Week, TrainingPlan)
    intervals_calls.py     # Intervals.icu API client
    gemini_parser.py        # Calls Gemini to generate a TrainingPlan
    prompts.py              # Builds the prompt sent to Gemini
    profile_creation.py     # Helper to build an AthleteProfile from rides
    testprofile.py          # Test athlete/ride fixtures
Plans/                    # Saved training plans (JSON), created at runtime
```

## Setup

1. Install dependencies:
   ```bash
   pip install streamlit streamlit-calendar python-dotenv requests pydantic google-genai
   ```
2. Create a `.env` file in `src/` with:
   ```
   INTERVALS_API_KEY=your_intervals_icu_api_key
   INTERVALS_ID=your_intervals_icu_athlete_id
   GEMINI_API_KEY=your_gemini_api_key
   ```

## Running the App

```bash
streamlit run src/App/app.py
```

1. Fill out and save your athlete profile in the sidebar (or toggle "Use test athlete" to skip straight to a demo profile).
2. Click **Generate Plan** to fetch recent rides (unless using the test athlete) and generate a training plan.
3. Click **Save Plan** to store it under `Plans/`, or **Load Plan** to reload the most recently saved one.

## Notes

- The app assumes you've already logged and synced at least one ride to Intervals.icu when using a real profile.
- `Plans/` is created automatically the first time a plan is saved.