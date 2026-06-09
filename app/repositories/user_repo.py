from app.models.user import User


class UserRepository:

    @staticmethod
    def get_by_email(db, email):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_id(db, user_id):
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def create(db, user):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user