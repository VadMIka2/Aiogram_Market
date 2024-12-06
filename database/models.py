from sqlalchemy import String, Integer, Text, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    """Модель для создания таблицы пользователей"""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    telegram_id: Mapped[int] = mapped_column(Integer)
    telegram_url: Mapped[str] = mapped_column(String(100))
    steam_login: Mapped[str] = mapped_column(String(100))


class Admin(Base):
    """Модель для создания таблицы админов"""
    __tablename__ = 'amdins'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    telegram_id: Mapped[int] = mapped_column(Integer)
    telegram_url: Mapped[str] = mapped_column(String(100))


class Catalog(Base):
    """Модель для создания таблицы каталогов"""
    __tablename__ = 'catalog'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    status: Mapped[int] = mapped_column(Integer)


class Basket(Base):
    """Модель для создания таблиц корзин пользователей"""
    __tablename__ = 'baskets'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer)
    product_id: Mapped[int] = mapped_column(Integer)
    