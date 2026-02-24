from settings import *

DATABASE_URL = 'sqlite+aiosqlite:///./test.db'

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    pass

class BudgetProfile(Base):
    __tablename__ = 'budget_profile'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)

    monthly_income = Column(DECIMAL(12, 2), nullable=False)
    min_savings_rate = Column(DECIMAL(5, 4), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    fixed_expenses = relationship('FixedExpense', back_populates='budget_profile')

class FixedExpense(Base):
    __tablename__ = 'fixed_expense'

    id = Column(UUID(as_uuid=True), primary_key=True)
    budget_profile_id = Column(UUID(as_uuid=True), ForeignKey('budget_profile.id'), nullable=False)

    name = Column(String(100), nullable=False)
    amount = Column(DECIMAL(12, 2), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    budget_profile = relationship('BudgetProfile', back_populates='fixed_expense')

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