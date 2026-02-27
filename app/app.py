from settings import *
from app.db import create_db_tables, get_async_session
from app.users import auth_backend, current_active_user, fastapi_users, User
from app.schemas import UserRead, UserCreate, UserUpdate, HabitSchema

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post('/habit')
async def post_habit(habit: HabitSchema, session: AsyncSession = Depends(get_async_session)
               ):
    habit_obj = habit
    if 1 < habit_obj.target_per_week <= 7:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Target per week must be between 1 and 7... ')
    
    session.add(habit_obj)
    await session.commit(habit_obj)
    await session.refresh(habit_obj)

    

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=['auth'])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix='/auth', tags=['auth'])
app.include_router(fastapi_users.get_reset_password_router(), prefix='/auth', tags=['auth'])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix='/auth', tags=['auth'])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix='/auth', tags=['users'])