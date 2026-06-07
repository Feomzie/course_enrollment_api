from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, admin_required
from app.schemas.course import CourseCreate
from app.services.course_service import CourseService


router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)


@router.get("/")
def get_courses(db: Session = Depends(get_db)):
    return CourseService.get_all(db)

@router.post("/")
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db),
   user = Depends(admin_required)
):
    return CourseService.create(db, payload)