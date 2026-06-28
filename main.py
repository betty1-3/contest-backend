from fastapi import FastAPI
from database import engine, SessionLocal
from models import Base, User
from schemas import ProblemUpdate, UserCreate
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()

def log_activity(db, action):

    activity = Activity(
        action=action
    )

    db.add(activity)
    db.commit()

@app.get("/")
def home():
    return {"message": "Contest Control Center API"}


@app.post("/users")
def create_user(user: UserCreate):

    db = SessionLocal()

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    log_activity(
    db,
    f"User {new_user.username} created"
)
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username
    }

from models import Contest, Problem, Registration, Submission, Activity
from schemas import (
    ContestCreate,
    ProblemCreate,
    RegistrationCreate,
    SubmissionCreate,
    ContestUpdate,
    ProblemUpdate
)

@app.post("/contests")
def create_contest(contest: ContestCreate):

    currentime = datetime.now()

    db = SessionLocal()

    if contest.end_time <= contest.start_time:
     return {
        "error": "End time must be greater than start time"
    }

    status = "Draft"

    if contest.start_time <= currentime <= contest.end_time:
        status = "Live"

    elif currentime > contest.end_time:
        status = "Ended"    

    else:
        status = "Scheduled"


    new_contest = Contest(
        name=contest.name,
        description=contest.description,
        start_time=contest.start_time,
        end_time=contest.end_time,
        status=status
    )

    

    db.add(new_contest)
    db.commit()
    log_activity(
    db,
    f"Contest {new_contest.name} created"
)
    db.refresh(new_contest)

    return {
        "id": new_contest.id,
        "name": new_contest.name,
        "status": new_contest.status
    }

@app.get("/contests/{contest_id}")
def get_contest(contest_id: int):

    db = SessionLocal()

    contest = db.query(Contest).filter(
        Contest.id == contest_id
    ).first()

    if not contest:
        return {"error": "Contest not found"}

    return contest

@app.patch("/contests/{contest_id}")
def update_contest(
    contest_id: int,
    updated: ContestUpdate
):

    db = SessionLocal()

    contest = db.query(Contest).filter(
        Contest.id == contest_id
    ).first()

    if not contest:
        return {"error": "Contest not found"}
    
    if updated.end_time <= updated.start_time:
        return {
        "error": "End time must be greater than start time"
    }

    if contest.status == "Ended":
        return {
        "error": "Cannot edit ended contest"
    }

    contest.name = updated.name
    contest.description = updated.description
    contest.start_time = updated.start_time
    contest.end_time = updated.end_time

    db.commit()

    return contest

@app.post("/contests/{contest_id}/start")
def start_contest(contest_id: int):

    db = SessionLocal()

    contest = db.query(Contest).filter(
        Contest.id == contest_id
    ).first()

    if not contest:
        return {"error": "Contest not found"}

    if contest.status == "Live":
        return {
            "error": "Contest already started"
        }
    
    elif contest.status == "Ended":
        return {"error": "Contest already ended"}

    contest.status = "Live"

    db.commit()

    return {
        "message": "Contest started"
    }

@app.post("/contests/{contest_id}/end")
def end_contest(contest_id: int):

    db = SessionLocal()

    contest = db.query(Contest).filter(
        Contest.id == contest_id
    ).first()

    if not contest:
        return {"error": "Contest not found"}
    
    if contest.status == "Ended":
        return {"error": "Contest already ended"}

    contest.status = "Ended"

    db.commit()


    return {
        "message": "Contest ended"
    }

@app.post("/problems")
def create_problem(problem: ProblemCreate):

    db = SessionLocal()

    existing_problem = db.query(Problem).filter(
        Problem.contest_id == problem.contest_id,
        Problem.title == problem.title
).first()

    if existing_problem:
        return {
        "error": "Problem title already exists in this contest"
    }

    contest = db.query(Contest).filter(
        Contest.id == problem.contest_id
    ).first()

    if not contest:
        return {"error": "Contest not found"}

    if problem.points < 0:
        return {"error": "Points cannot be negative"}

    new_problem = Problem(
        contest_id=problem.contest_id,
        title=problem.title,
        difficulty=problem.difficulty,
        points=problem.points
    )

    db.add(new_problem)
    db.commit()
    log_activity(
    db,
    f"Problem {new_problem.title} created"
)
    db.refresh(new_problem)

    return {
        "id": new_problem.id,
        "title": new_problem.title
    }

@app.get("/problems/{problem_id}")
def get_problem(problem_id: int):

    db = SessionLocal()

    problem = db.query(Problem).filter(
        Problem.id == problem_id
    ).first()

    if not problem:
        return {"error": "Problem not found"}

    return problem

@app.patch("/problems/{problem_id}")
def update_problem(
    problem_id: int,
    updated: ProblemUpdate
):

    db = SessionLocal()

    problem = db.query(Problem).filter(
        Problem.id == problem_id
    ).first()

    if not problem:
        return {"error": "Problem not found"}

    if updated.points < 0:
        return {
            "error": "Points cannot be negative"
        }

    problem.title = updated.title
    problem.difficulty = updated.difficulty
    problem.points = updated.points

    db.commit()

    return problem

@app.delete("/problems/{problem_id}")
def delete_problem(problem_id: int):

    db = SessionLocal()

    problem = db.query(Problem).filter(
        Problem.id == problem_id
    ).first()

    if not problem:
        return {"error": "Problem not found"}

    db.delete(problem)
    db.commit()

    return {
        "message": "Problem deleted"
    }

@app.post("/register")
def register_participant(registration: RegistrationCreate):

    db = SessionLocal()

    user = db.query(User).filter(
        User.id == registration.user_id
    ).first()

    if not user:
        return {"error": "User not found"}

    contest = db.query(Contest).filter(
        Contest.id == registration.contest_id
    ).first()

    if not contest:
        return {"error": "Contest not found"}
    
    if contest.status == "Live":
        return {
        "error": "Registration closed"
    }

    existing = db.query(Registration).filter(
        Registration.user_id == registration.user_id,
        Registration.contest_id == registration.contest_id
    ).first()

    if existing:
        return {"error": "Already registered"}

    new_registration = Registration(
        user_id=registration.user_id,
        contest_id=registration.contest_id
    )

    db.add(new_registration)
    db.commit()
    log_activity(
    db,
    f"User {registration.user_id} registered"
)

    return {"message": "Registration successful"}

@app.get("/participants/{user_id}")
def get_participant(user_id: int):

    db = SessionLocal()

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        return {"error": "Participant not found"}

    return user

@app.get("/participants")
def get_registered_participants():

    db = SessionLocal()

    registrations = db.query(Registration).all()

    return registrations

@app.post("/submissions")
def create_submission(submission: SubmissionCreate):

    db = SessionLocal()
    from datetime import datetime

    user = db.query(User).filter(
        User.id == submission.user_id
    ).first()

    if not user:
        return {"error": "User not found"}

    problem = db.query(Problem).filter(
        Problem.id == submission.problem_id
    ).first()

    if not problem:
        return {"error": "Problem not found"}
    registration = db.query(Registration).filter(
    Registration.user_id == submission.user_id
).first()

    if not registration:
        return {
            "error": "Participant not registered"
        }
    
    contest = db.query(Contest).filter(
    Contest.id == problem.contest_id
).first()

    if contest.status == "Ended":
        return {
            "error": "Contest ended"
        }
    
    elif contest.status != "Live":
        return {
        "error": "Contest is not live"
    }

    new_submission = Submission(
    user_id=submission.user_id,
    problem_id=submission.problem_id,
    language=submission.language,
    verdict="Accepted",
    submission_time=datetime.now()
)

    db.add(new_submission)
    db.commit()
    log_activity(
    db,
    f"Submission by user {submission.user_id}"
)
    db.refresh(new_submission)

    return {
        "submission_id": new_submission.id,
        "verdict": new_submission.verdict
    }

@app.get("/submissions/{submission_id}")
def get_submission(submission_id: int):

    db = SessionLocal()

    submission = db.query(Submission).filter(
        Submission.id == submission_id
    ).first()

    if not submission:
        return {"error": "Submission not found"}

    return submission

@app.get("/participants/{user_id}/submissions")
def get_participant_submissions(user_id: int):

    db = SessionLocal()

    submissions = db.query(Submission).filter(
        Submission.user_id == user_id
    ).all()

    return submissions

@app.get("/problems/{problem_id}/submissions")
def get_problem_submissions(problem_id: int):

    db = SessionLocal()

    submissions = db.query(Submission).filter(
        Submission.problem_id == problem_id
    ).all()

    return submissions

@app.get("/leaderboard")
def get_leaderboard():

    db = SessionLocal()

    users = db.query(User).all()

    leaderboard = []

    for user in users:

        accepted_submissions = db.query(Submission).filter(
            Submission.user_id == user.id,
            Submission.verdict == "Accepted"
        ).all()

        solved_problems = set()

        total_points = 0
        total_penalty = 0

        for submission in accepted_submissions:

            if submission.problem_id in solved_problems:
                continue

            solved_problems.add(submission.problem_id)

            problem = db.query(Problem).filter(
                Problem.id == submission.problem_id
            ).first()

            contest = db.query(Contest).filter(
                Contest.id == problem.contest_id
            ).first()

            total_points += problem.points

            penalty_minutes = (
                submission.submission_time -
                contest.start_time
            ).total_seconds() / 60

            total_penalty += penalty_minutes

        leaderboard.append({
            "user_id": user.id,
            "username": user.username,
            "points": total_points,
            "penalty": round(total_penalty, 2)
        })

    leaderboard.sort(
        key=lambda x: (
            -x["points"],
            x["penalty"]
        )
    )

    return leaderboard

@app.get("/activities")
def get_activities():

    db = SessionLocal()

    activities = db.query(Activity).all()

    return activities

@app.get("/leaderboard/rank/{user_id}")
def get_rank(user_id: int):

    db = SessionLocal()

    users = db.query(User).all()

    leaderboard = []

    for user in users:

        accepted_submissions = db.query(Submission).filter(
            Submission.user_id == user.id,
            Submission.verdict == "Accepted"
        ).all()

        solved_problems = set()

        total_points = 0
        total_penalty = 0

        for submission in accepted_submissions:

            if submission.problem_id in solved_problems:
                continue

            solved_problems.add(submission.problem_id)

            problem = db.query(Problem).filter(
                Problem.id == submission.problem_id
            ).first()

            contest = db.query(Contest).filter(
                Contest.id == problem.contest_id
            ).first()

            total_points += problem.points

            penalty_minutes = (
                submission.submission_time -
                contest.start_time
            ).total_seconds() / 60

            total_penalty += penalty_minutes

        leaderboard.append({
            "user_id": user.id,
            "username": user.username,
            "points": total_points,
            "penalty": round(total_penalty, 2)
        })

    leaderboard.sort(
        key=lambda x: (
            -x["points"],
            x["penalty"]
        )
    )

    for rank, entry in enumerate(leaderboard, start=1):
        if entry["user_id"] == user_id:
            return {
                "rank": rank,
                "username": entry["username"],
                "points": entry["points"]
            }
            

    return {"error": "User not found"}

@app.get("/activities/{activity_id}")
def get_activity(activity_id: int):

    db = SessionLocal()

    activity = db.query(Activity).filter(
        Activity.id == activity_id
    ).first()

    if not activity:
        return {"error": "Activity not found"}

    return activity