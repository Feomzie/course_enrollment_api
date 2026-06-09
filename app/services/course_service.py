from fastapi import HTTPException

from app.models.course import Course
from app.repositories.course_repo import CourseRepository


class CourseService:

    @staticmethod
    def create(db, payload):
        if CourseRepository.get_by_code(db, payload.code):
            raise HTTPException(400, "Course code already exists")

        course = Course(**payload.dict())
        return CourseRepository.create(db, course)
    
    @staticmethod
    def get_all(db, skip: int = 0, limit: int = 10, search: str | None = None):
        return CourseRepository.get_courses(db, skip=skip, limit=limit, search=search)

    @staticmethod
    def get_by_id(db, course_id):
        course = CourseRepository.get_by_id(db, course_id)
        if course is None:
            raise HTTPException(404, "Course not found")
        return course

    @staticmethod
    def update(db, course_id, payload):
        course = CourseRepository.get_by_id(db, course_id)
        if course is None:
            raise HTTPException(404, "Course not found")

        if payload.title is not None:
            course.title = payload.title
        if payload.capacity is not None:
            course.capacity = payload.capacity
        if payload.is_active is not None:
            course.is_active = payload.is_active

        return CourseRepository.update(db, course)

    @staticmethod
    def deactivate(db, course_id):
        course = CourseRepository.get_by_id(db, course_id)
        if course is None:
            raise HTTPException(404, "Course not found")

        return CourseRepository.deactivate(db, course)
