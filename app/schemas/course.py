from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    title: str
    code: str
    capacity: int = Field(gt=0)

class CourseUpdate(BaseModel):
    title: str | None = None
    capacity: int | None = Field(default=None, gt=0)
    is_active: bool | None = None


class CourseResponse(BaseModel):
    id: int
    title: str
    code: str
    capacity: int
    is_active: bool

    class Config:
        from_attributes = True