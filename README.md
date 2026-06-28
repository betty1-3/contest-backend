# CodeChef Contest Control Center

## Overview

CodeChef Contest Control Center is a backend system built using FastAPI and SQLite for managing programming contests. The system supports contest creation, problem management, participant registration, submissions, leaderboard generation, and activity tracking.

The project was developed as part of a backend recruitment assignment and focuses on implementing core contest-management workflows with proper validation and business rules.

---

## Tech Stack

* Python 3.13
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Uvicorn

---

## Project Structure

```
contest-backend/
│
├── database.py       # Database configuration
├── models.py         # SQLAlchemy database models
├── schemas.py        # Request/response schemas
├── main.py           # API routes and business logic
│
├── contest.db        # SQLite database
└── README.md
```

---

## Features Implemented

### Contest Management

* Create Contest
* Get Contest Details
* Update Contest
* Start Contest
* End Contest
* Contest Status Management
* Contest Time Validation

### Problem Management

* Create Problem
* Get Problem Details
* Update Problem
* Delete Problem
* Unique Problem Title Validation
* Points Validation

### Participant Registration

* Register Participants
* Get Participant Details
* Get Registered Participants
* Duplicate Registration Prevention
* Registration Closure After Contest Goes Live

### Submission System

* Create Submission
* Get Submission Details
* Get Participant Submissions
* Get Problem Submissions
* Contest Status Validation
* Registration Validation
* Activity Logging

### Leaderboard

* Dynamic Leaderboard Generation
* Points-Based Ranking
* Penalty Time Tie-Breaker
* Participant Rank Retrieval

### Activity Logs

* Automatic Activity Tracking
* Retrieve All Activities
* Retrieve Activity By ID

---

## Database Design

### User

* id
* username
* email

### Contest

* id
* name
* description
* start_time
* end_time
* status

### Problem

* id
* contest_id
* title
* difficulty
* points

### Registration

* id
* user_id
* contest_id

### Submission

* id
* user_id
* problem_id
* language
* verdict
* submission_time

### Activity

* id
* action

---

## Business Rules

* Contest end time must be greater than start time.
* Contest status transitions follow Scheduled → Live → Ended.
* Problem titles must be unique within a contest.
* Problem points cannot be negative.
* Duplicate registrations are not allowed.
* Registration closes once a contest becomes Live.
* Submissions are allowed only for registered participants.
* Submissions are allowed only while a contest is Live.
* Submissions are blocked after contest completion.

---

## Leaderboard Logic

Leaderboard rankings are generated dynamically from submission data.

Ranking Rules:

1. Higher total points rank higher.
2. If total points are equal, lower penalty time ranks higher.

Penalty Calculation:

Penalty time is calculated as the elapsed time between contest start time and accepted submission time.

To prevent duplicate scoring, each solved problem contributes points only once even if multiple accepted submissions exist.

---

## API Endpoints

### Contest APIs

* POST /contests
* GET /contests/{contest_id}
* PATCH /contests/{contest_id}
* POST /contests/{contest_id}/start
* POST /contests/{contest_id}/end

### Problem APIs

* POST /problems
* GET /problems/{problem_id}
* PATCH /problems/{problem_id}
* DELETE /problems/{problem_id}

### Registration APIs

* POST /register
* GET /participants
* GET /participants/{user_id}

### Submission APIs

* POST /submissions
* GET /submissions/{submission_id}
* GET /participants/{user_id}/submissions
* GET /problems/{problem_id}/submissions

### Leaderboard APIs

* GET /leaderboard
* GET /leaderboard/rank/{user_id}

### Activity APIs

* GET /activities
* GET /activities/{activity_id}

---

## Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/betty1-3/contest-backend.git
```

2. Navigate to the project directory

```bash
cd contest-backend
```

3. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

4. Start the server

```bash
uvicorn main:app --reload
```

5. Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## Future Improvements

* JWT Authentication
* Automated Code Judging System
* Rejudge Functionality
* Contest Freeze Mode
* Wrong Submission Penalty Handling
* Docker Deployment
* PostgreSQL Support
* Pagination and Filtering APIs

---

## Author

Developed as part of the CodeChef Contest Control Center Backend Assignment.
