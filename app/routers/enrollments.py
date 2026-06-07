from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.schemas.enrollment import EnrollmentCreate
from app.services.enrollment_service import EnrollmentService


router = APIRouter(
    prefix="/enrollments",
    tags=["enrollments"]
)


@router.post("/")
def enroll(
    payload: EnrollmentCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return EnrollmentService.enroll(db, user.id, payload.course_id)