from app.models.course import Course
from app.repositories.course_repo import CourseRepository


class CourseService:

    @staticmethod
    def create(db, payload):
        course = Course(**payload.dict())
        return CourseRepository.create(db, course)
    
    @staticmethod
    def get_all(db):
        return CourseRepository.get_all(db)