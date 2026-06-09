from app.models.course import Course


class CourseRepository:

    @staticmethod
    def get_courses(db, skip: int = 0, limit: int = 10, search: str | None = None):
        query = db.query(Course).filter(Course.is_active == True)
        if search:
            pattern = f"%{search}%"
            query = query.filter(
                (Course.title.ilike(pattern)) | (Course.code.ilike(pattern))
            )
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_all_active(db):
        return db.query(Course).filter(Course.is_active == True).all()

    @staticmethod
    def get_by_id(db, course_id):
        return db.query(Course).filter(Course.id == course_id).first()

    @staticmethod
    def get_by_code(db, code):
        return db.query(Course).filter(Course.code == code).first()

    @staticmethod
    def create(db, course):
        db.add(course)
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def update(db, course):
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def deactivate(db, course):
        course.is_active = False
        db.commit()
        db.refresh(course)
        return course