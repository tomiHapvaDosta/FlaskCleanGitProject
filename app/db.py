from settings import *

DATABASE_URL = 'sqlite+aiosqlite:///./test.db'

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    pass

class Habit(Base):
    __tablename__ = 'habit'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    name = Column(String(100), nullable=False)
    target_per_week = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    logs = relationship('Logs', back_populates='habit')

class Logs(Base):
    __tablename__ = 'logs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    habit_id = Column(UUID(as_uuid=True), ForeignKey('habit.id'), nullable=False)
    done = Column(Boolean, nullable=False)
    mood = Column(Integer, nullable=False)
    notes = Column(Text, nullable=True)
    date = Column(Date, nullable=False)

    habit = relationship('Habit', back_populates='logs')



engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)