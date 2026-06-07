from fastapi import FastAPI

from app.routers import auth, courses, enrollments


app = FastAPI(title="Course Enrollment API")

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(enrollments.router)