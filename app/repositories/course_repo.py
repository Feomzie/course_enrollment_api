from app.models.course import Course


class CourseRepository:

    @staticmethod
    def get_all(db):
        return db.query(Course).all()
    
    @staticmethod
    def get_by_id(db, course_id):
        return db.query(Course).filter(Course.id == course_id).first()
    
    @staticmethod
    def create(db, course):
        db.add(course)
        db.commit()
        db.refresh(course)
        return course