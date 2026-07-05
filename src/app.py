"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

import json
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities",
)

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount(
    "/static",
    StaticFiles(directory=current_dir / "static"),
    name="static",
)

DATA_FILE = current_dir / "data.json"


class StudentProfile(BaseModel):
    email: str
    name: str
    grade: str
    guardians: List[str] = Field(default_factory=list)
    status: str = "active"
    enrollments: List[str] = Field(default_factory=list)


def _default_student(email: str) -> Dict[str, object]:
    name = email.split("@")[0].replace(".", " ").title()
    return {
        "email": email,
        "name": name,
        "grade": "11",
        "guardians": [],
        "status": "active",
        "enrollments": [],
    }


DEFAULT_DATABASE = {
    "activities": {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"],
        },
        "Soccer Team": {
            "description": "Join the school soccer team and compete in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"],
        },
        "Basketball Team": {
            "description": "Practice and play basketball with the school team",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["ava@mergington.edu", "mia@mergington.edu"],
        },
        "Art Club": {
            "description": "Explore your creativity through painting and drawing",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["amelia@mergington.edu", "harper@mergington.edu"],
        },
        "Drama Club": {
            "description": "Act, direct, and produce plays and performances",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["ella@mergington.edu", "scarlett@mergington.edu"],
        },
        "Math Club": {
            "description": "Solve challenging problems and participate in math competitions",
            "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
            "max_participants": 10,
            "participants": ["james@mergington.edu", "benjamin@mergington.edu"],
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 12,
            "participants": ["charlotte@mergington.edu", "henry@mergington.edu"],
        },
    },
    "students": {
        "michael@mergington.edu": {
            "email": "michael@mergington.edu",
            "name": "Michael",
            "grade": "11",
            "guardians": [],
            "status": "active",
            "enrollments": ["Chess Club"],
        },
        "daniel@mergington.edu": {
            "email": "daniel@mergington.edu",
            "name": "Daniel",
            "grade": "11",
            "guardians": [],
            "status": "active",
            "enrollments": ["Chess Club"],
        },
        "emma@mergington.edu": {
            "email": "emma@mergington.edu",
            "name": "Emma",
            "grade": "10",
            "guardians": [],
            "status": "active",
            "enrollments": ["Programming Class"],
        },
        "sophia@mergington.edu": {
            "email": "sophia@mergington.edu",
            "name": "Sophia",
            "grade": "10",
            "guardians": [],
            "status": "active",
            "enrollments": ["Programming Class"],
        },
        "john@mergington.edu": {
            "email": "john@mergington.edu",
            "name": "John",
            "grade": "12",
            "guardians": [],
            "status": "active",
            "enrollments": ["Gym Class"],
        },
        "olivia@mergington.edu": {
            "email": "olivia@mergington.edu",
            "name": "Olivia",
            "grade": "11",
            "guardians": [],
            "status": "active",
            "enrollments": ["Gym Class"],
        },
        "liam@mergington.edu": {
            "email": "liam@mergington.edu",
            "name": "Liam",
            "grade": "11",
            "guardians": [],
            "status": "active",
            "enrollments": ["Soccer Team"],
        },
        "noah@mergington.edu": {
            "email": "noah@mergington.edu",
            "name": "Noah",
            "grade": "11",
            "guardians": [],
            "status": "active",
            "enrollments": ["Soccer Team"],
        },
        "ava@mergington.edu": {
            "email": "ava@mergington.edu",
            "name": "Ava",
            "grade": "10",
            "guardians": [],
            "status": "active",
            "enrollments": ["Basketball Team"],
        },
        "mia@mergington.edu": {
            "email": "mia@mergington.edu",
            "name": "Mia",
            "grade": "10",
            "guardians": [],
            "status": "active",
            "enrollments": ["Basketball Team"],
        },
        "amelia@mergington.edu": {
            "email": "amelia@mergington.edu",
            "name": "Amelia",
            "grade": "11",
            "guardians": [],
            "status": "active",
            "enrollments": ["Art Club"],
        },
        "harper@mergington.edu": {
            "email": "harper@mergington.edu",
            "name": "Harper",
            "grade": "10",
            "guardians": [],
            "status": "active",
            "enrollments": ["Art Club"],
        },
        "ella@mergington.edu": {
            "email": "ella@mergington.edu",
            "name": "Ella",
            "grade": "12",
            "guardians": [],
            "status": "active",
            "enrollments": ["Drama Club"],
        },
        "scarlett@mergington.edu": {
            "email": "scarlett@mergington.edu",
            "name": "Scarlett",
            "grade": "11",
            "guardians": [],
            "status": "active",
            "enrollments": ["Drama Club"],
        },
        "james@mergington.edu": {
            "email": "james@mergington.edu",
            "name": "James",
            "grade": "12",
            "guardians": [],
            "status": "active",
            "enrollments": ["Math Club"],
        },
        "benjamin@mergington.edu": {
            "email": "benjamin@mergington.edu",
            "name": "Benjamin",
            "grade": "12",
            "guardians": [],
            "status": "active",
            "enrollments": ["Math Club"],
        },
        "charlotte@mergington.edu": {
            "email": "charlotte@mergington.edu",
            "name": "Charlotte",
            "grade": "11",
            "guardians": [],
            "status": "active",
            "enrollments": ["Debate Team"],
        },
        "henry@mergington.edu": {
            "email": "henry@mergington.edu",
            "name": "Henry",
            "grade": "12",
            "guardians": [],
            "status": "active",
            "enrollments": ["Debate Team"],
        },
    },
}


def load_database() -> Dict[str, Dict]:
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as database_file:
            return json.load(database_file)

    save_database(DEFAULT_DATABASE)
    return DEFAULT_DATABASE


def save_database(database: Dict[str, Dict]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as database_file:
        json.dump(database, database_file, indent=2)


database = load_database()
activities = database["activities"]
students = database["students"]


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.get("/students")
def get_students():
    return students


@app.get("/students/{email}")
def get_student(email: str):
    if email not in students:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return students[email]


@app.post("/students")
def create_student(profile: StudentProfile):
    students[profile.email] = profile.dict()
    save_database(database)
    return {"message": f"Student profile for {profile.email} was created or updated."}


def ensure_student_profile(email: str) -> None:
    if email not in students:
        students[email] = _default_student(email)


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    ensure_student_profile(email)
    activity["participants"].append(email)

    if activity_name not in students[email]["enrollments"]:
        students[email]["enrollments"].append(activity_name)

    save_database(database)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

    activity["participants"].remove(email)

    if email in students and activity_name in students[email]["enrollments"]:
        students[email]["enrollments"].remove(activity_name)

    save_database(database)
    return {"message": f"Unregistered {email} from {activity_name}"}
