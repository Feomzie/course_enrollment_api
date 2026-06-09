from fastapi import HTTPException

from app.repositories.course_repo import CourseRepository
from app.repositories.enrollment_repo import EnrollmentRepository


class EnrollmentService:

    @staticmethod
    def enroll(db, user_id, course_id):

        course = CourseRepository.get_by_id(db, course_id)

        if course is None:
            raise HTTPException(404, "Course not found")
        
        if not course.is_active:
            raise HTTPException(400, "Course is inactive")

        if EnrollmentRepository.get(db, user_id, course_id):
            raise HTTPException(400, "Already enrolled in this course")
        
        if EnrollmentRepository.count(db, course_id) >= course.capacity:
            raise HTTPException(400, "Course is full")
        
        return EnrollmentRepository.create(db, user_id, course_id)

    @staticmethod
    def deregister(db, user_id, course_id):
        enrollment = EnrollmentRepository.get(db, user_id, course_id)
        if enrollment is None:
            raise HTTPException(404, "Enrollment not found")

        return EnrollmentRepository.delete(db, enrollment)

    @staticmethod
    def list_all(db):
        return EnrollmentRepository.list_all(db)

    @staticmethod
    def list_by_course(db, course_id):
        course = CourseRepository.get_by_id(db, course_id)
        if course is None:
            raise HTTPException(404, "Course not found")
        return EnrollmentRepository.list_by_course(db, course_id)

    @staticmethod
    def remove(db, enrollment_id):
        enrollment = EnrollmentRepository.get_by_id(db, enrollment_id)
        if enrollment is None:
            raise HTTPException(404, "Enrollment not found")
        return EnrollmentRepository.delete(db, enrollment)
