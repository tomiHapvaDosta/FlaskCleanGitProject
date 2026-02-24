from fastapi import FastAPI, HTTPException, Form, Depends, status, Request
from contextlib import asynccontextmanager
import uuid
from datetime import datetime
from pydantic import BaseModel
from fastapi_users import schemas, BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from collections.abc import AsyncGenerator
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID
import uvicorn
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
