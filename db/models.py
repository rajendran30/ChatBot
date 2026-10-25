from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True)

    objectives: Mapped[list["Objective"]] = relationship(back_populates="store")
    kpis: Mapped[list["KPI"]] = relationship(back_populates="store")
    metrics: Mapped[list["Metric"]] = relationship(back_populates="store")


class Marketplace(Base):
    __tablename__ = "marketplaces"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)


class Objective(Base):
    __tablename__ = "objectives"

    id: Mapped[int] = mapped_column(primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    owner: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    store: Mapped["Store"] = relationship(back_populates="objectives")
    key_results: Mapped[list["KeyResult"]] = relationship(back_populates="objective")


class KeyResult(Base):
    __tablename__ = "key_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    objective_id: Mapped[int] = mapped_column(ForeignKey("objectives.id"))
    title: Mapped[str] = mapped_column(String(300))
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    target_value: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    current_value: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    objective: Mapped["Objective"] = relationship(back_populates="key_results")


class KPI(Base):
    __tablename__ = "kpis"

    id: Mapped[int] = mapped_column(primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))
    marketplace_id: Mapped[Optional[int]] = mapped_column(ForeignKey("marketplaces.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(200))
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    target_value: Mapped[Optional[float]] = mapped_column(Numeric, nullable=True)
    cadence: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    store: Mapped["Store"] = relationship(back_populates="kpis")
    marketplace: Mapped[Optional["Marketplace"]] = relationship()
    values: Mapped[list["KPIValue"]] = relationship(back_populates="kpi")


class KPIValue(Base):
    __tablename__ = "kpi_values"

    id: Mapped[int] = mapped_column(primary_key=True)
    kpi_id: Mapped[int] = mapped_column(ForeignKey("kpis.id"))
    period_start: Mapped[date] = mapped_column(Date)
    period_end: Mapped[date] = mapped_column(Date)
    value: Mapped[float] = mapped_column(Numeric)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    kpi: Mapped["KPI"] = relationship(back_populates="values")


class Metric(Base):
    __tablename__ = "metrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"))
    marketplace_id: Mapped[Optional[int]] = mapped_column(ForeignKey("marketplaces.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(200))
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    store: Mapped["Store"] = relationship(back_populates="metrics")
    marketplace: Mapped[Optional["Marketplace"]] = relationship()
    values: Mapped[list["MetricValue"]] = relationship(back_populates="metric")


class MetricValue(Base):
    __tablename__ = "metric_values"

    id: Mapped[int] = mapped_column(primary_key=True)
    metric_id: Mapped[int] = mapped_column(ForeignKey("metrics.id"))
    period_start: Mapped[date] = mapped_column(Date)
    period_end: Mapped[date] = mapped_column(Date)
    value: Mapped[float] = mapped_column(Numeric)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    metric: Mapped["Metric"] = relationship(back_populates="values")
