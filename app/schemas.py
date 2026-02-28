from settings import *

class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str

class UserCreate(schemas.BaseUserCreate):
    username: str

class UserUpdate(schemas.BaseUserUpdate):
    username: str | None = None

class HabitSchema(BaseModel):
    name: str
    target_per_week: int

class LogSchema(BaseModel):
    done: bool
    mood: int
    notes: str
    date: datetime.date
    habit_id: uuid.UUID | None = None