from app.models.enrollment import Enrollment


class EnrollmentRepository:

    @staticmethod
    def get(db, user_id, course_id):
        return db.query(Enrollment).filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id
        ).first()