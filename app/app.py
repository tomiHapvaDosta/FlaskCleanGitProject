from settings import *
from app.db import create_db_tables, get_async_session
from app.users import auth_backend, current_active_user, fastapi_users, User
from app.schemas import UserRead, UserCreate, UserUpdate, HabitSchema, LogSchema

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post('/habit')
async def post_habit(habit_schema: HabitSchema, session: AsyncSession = Depends(get_async_session)
               ):
    habit_obj = habit_schema

    if not habit_obj:
        raise HTTPException(status_code=404, detail='Habit object not found... ')

    if not 1 <= habit_obj.target_per_week <= 7:
        raise HTTPException(status_code=422, detail='Target per week must be between 1 and 7... ')
    
    session.add(habit_obj)
    await session.commit()
    await session.refresh(habit_obj)

@app.post('/log/{habit_id}')
async def log_daily_progress(log_schema: LogSchema, habit_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    log_obj = log_schema

    if not log_obj:
        raise HTTPException(status_code=404, detail='Log object not found... ')
    
    if not 1 <= log_obj.mood <= 10:
        raise HTTPException(status_code=422, detail='Mood must be between 1 and 10')
    
    log_obj.habit_id = habit_id

    session.add(log_obj) 
    await session.commit()
    await session.refresh(log_obj)
    

    

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=['auth'])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix='/auth', tags=['auth'])
app.include_router(fastapi_users.get_reset_password_router(), prefix='/auth', tags=['auth'])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix='/auth', tags=['auth'])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix='/auth', tags=['users'])