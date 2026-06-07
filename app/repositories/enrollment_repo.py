from app.models.enrollment import Enrollment


class EnrollmentRepository:

    @staticmethod
    def get(db, user_id, course_id):
        return db.query(Enrollment).filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id
        ).first()
    
    @staticmethod
    def create(db, user_id, course_id):
        enrollment = Enrollment(
            user_id=user_id,
            course_id=course_id
        )
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        return enrollment

    @staticmethod
    def count(db, course_id):
        return db.query(Enrollment).filter(
            Enrollment.course_id == course_id
        ).count()