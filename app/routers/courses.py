from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_db, admin_required
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.services.course_service import CourseService


router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)


@router.get("/", response_model=list[CourseResponse])
def get_courses(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    q: str | None = Query(None, description="Search by course title or code"),
):
    skip = (page - 1) * limit
    return CourseService.get_all(db, skip=skip, limit=limit, search=q)


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    return CourseService.get_by_id(db, course_id)


@router.post("/", response_model=CourseResponse)
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    return CourseService.create(db, payload)


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    payload: CourseUpdate,
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    return CourseService.update(db, course_id, payload)


@router.delete("/{course_id}", response_model=CourseResponse)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    user=Depends(admin_required)
):
    return CourseService.deactivate(db, course_id)