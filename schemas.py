from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str

from datetime import datetime

class ContestCreate(BaseModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime

class ProblemCreate(BaseModel):
    contest_id: int
    title: str
    difficulty: str
    points: int

class RegistrationCreate(BaseModel):
    user_id: int
    contest_id: int

class SubmissionCreate(BaseModel):
    user_id: int
    problem_id: int
    language: str

class ContestUpdate(BaseModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime

class ProblemUpdate(BaseModel):
    title: str
    difficulty: str
    points: int