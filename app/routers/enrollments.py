from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, student_required, admin_required
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse
from app.services.enrollment_service import EnrollmentService


router = APIRouter(
    prefix="/enrollments",
    tags=["enrollments"]
)


@router.post("/", response_model=EnrollmentResponse)
def enroll(
    payload: EnrollmentCreate,
    db: Session = Depends(get_db),
    user=Depends(student_required)
):
    return EnrollmentService.enroll(db, user.id, payload.course_id)


@router.delete("/self/{course_id}", response_model=EnrollmentResponse)
def deregister(
    course_id: int,
    db: Session = Depends(get_db),
    user=Depends(student_required)
):
    return EnrollmentService.deregister(db, user.id, course_id)


@router.get("/", response_model=list[EnrollmentResponse])
def list_enrollments(
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    return EnrollmentService.list_all(db)


@router.get("/course/{course_id}", response_model=list[EnrollmentResponse])
def list_course_enrollments(
    course_id: int,
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    return EnrollmentService.list_by_course(db, course_id)


@router.delete("/{enrollment_id}", response_model=EnrollmentResponse)
def remove_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    return EnrollmentService.remove(db, enrollment_id)