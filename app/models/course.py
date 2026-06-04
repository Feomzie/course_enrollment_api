from sqlalchemy import Boolean, Column, Integer, String

from sqlalchemy.orm import relationship

from app.core.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    enrollments = relationship("Enrollment", back_populates="course")