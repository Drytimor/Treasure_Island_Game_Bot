from decimal import Decimal
from config.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Numeric, PrimaryKeyConstraint, ForeignKey


class Wallet(Base):
    __tablename__ = 'wallets'

    id: Mapped[int] = mapped_column(primary_key=True)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 5))


class Currencies(Base):
    __tablename__ = 'currencies'
    __table_args__ = (
        PrimaryKeyConstraint('name'),
        )

    name: Mapped[str] = mapped_column(String(255))
    well: Mapped[Decimal] = mapped_column(Numeric(10, 5))


class Teams(Base):
    __tablename__ = "teams"
    __table_args__ = (
        PrimaryKeyConstraint('name'),
        )

    name: Mapped[str] = mapped_column(String(255))
    aliases: Mapped[str] = mapped_column(String(255), unique=True)
    gold: Mapped[Decimal] = mapped_column(Numeric(10, 5))


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        )

    id: Mapped[int] = mapped_column(autoincrement=False)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    tris: Mapped[Decimal] = mapped_column(Numeric(10, 5))
    gold: Mapped[Decimal] = mapped_column(Numeric(10, 5))
    farm_gold: Mapped[Decimal] = mapped_column(Numeric(10, 5))
    rates: Mapped[list["Rates"]] = relationship()


class Rates(Base):
    __tablename__ = "rates"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
    )
    team_name: Mapped[str] = mapped_column(
        ForeignKey('teams.name', ondelete='CASCADE')
    )
    gold: Mapped[Decimal] = mapped_column(Numeric(10, 5))


