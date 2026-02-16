from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, DateTime, Float, Boolean
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base
from enums import *  # Assuming all enums are imported from a single place
from utils import is_valid_email, is_valid_url, is_valid_company_name, is_valid_tax_id, is_valid_naics
from enums import enum_column

Base = declarative_base()
from database import Base

class SalesAdminProfile(Base):
    __tablename__ = "sales_admin_profile"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    lvt_admin_id = Column(Integer, ForeignKey("user.id"))
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="admin_profile", foreign_keys=[user_id])
    lvt_admin = relationship("User", foreign_keys=[lvt_admin_id])


class SalesManagerProfile(Base):
    __tablename__ = "sales_manager_profile"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    admin_id = Column(Integer, ForeignKey("user.id"))
    target_leads = Column(Integer)
    feedback = Column(Text)

    user = relationship("User", back_populates="manager_profile")
    admin = relationship("User", foreign_keys=[admin_id])


class SalesRepProfile(Base):
    __tablename__ = "sales_rep_profile"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    manager_id = Column(Integer, ForeignKey("user.id"))
    target_leads = Column(Integer)
    feedback = Column(Text)

    user = relationship("User", back_populates="rep_profile")
    manager = relationship("User", foreign_keys=[manager_id])


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id"), unique=True)
    full_name = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    address = Column(Text)
    pincode = Column(String)
    contact_number = Column(String)
    email = Column(String, unique=True, nullable=False)
    subscription_type = enum_column(ActivePlan, "subscription_type_enum", default=ActivePlan.free)
    onboarding_status = enum_column(OnboardingStatusEnum, "onboarding_status_enum", default=OnboardingStatusEnum.to_be_onboarded)
    client_status = enum_column(ClientStatus, "client_status_enum", default=ClientStatus.inactive)
    payment_status = enum_column(SubscriptionStatus, "payment_status_enum", default=SubscriptionStatus.pending)
    plan_due_date = Column(Date)
    billing_period = enum_column(BillingPeriod, "billing_period_enum", default=BillingPeriod.monthly)
    rating = Column(Float)
    feedback = Column(Text)
    assigned_salesperson_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    assigned_salesperson = relationship("User", back_populates="clients", passive_deletes=True)
    company = relationship("Company", backref="sales_client", passive_deletes=True)
    appointments = relationship("Appointment", cascade="all, delete-orphan", passive_deletes=True)
    reports = relationship("ClientReport", cascade="all, delete-orphan", passive_deletes=True)
    

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    assigned_to_role = Column(String(100), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    email = Column(String(255))
    meeting_link = Column(Text)
    appointment_time = Column(DateTime(timezone=True), nullable=False)

    company = relationship("Company", back_populates="appointments")
    assigned_to = relationship("User", foreign_keys=[assigned_to_id], backref="appointments")

    @validates("email")
    def validate_email(self, key, value):
        if value and not is_valid_email(value):
            raise ValueError("Invalid email format.")
        return value.strip()


class PerformanceReport(Base):
    __tablename__ = "performance_report"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    leads = Column(Integer)
    subscription_count = Column(Integer)
    target_revenue = Column(Integer)
    achieved_revenue = Column(Integer)
    archived_amount = Column(Integer)
    archived_percentage = Column(Float)
    report_date = Column(Date)

    user = relationship("User", backref="performance_reports")


class ClientReport(Base):
    __tablename__ = "client_reports"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id', ondelete='CASCADE'), nullable=False)
    recent_subscription_date = Column(Date, nullable=True)
    subscription_type = Column(String, nullable=True)
    invoice_id = Column(String, nullable=True)
    total_subscription_amount = Column(Integer, nullable=True)
    status = enum_column(ClientStatus, "client_status_enum", default=ClientStatus.inactive)
    report_date = Column(Date, nullable=True)


class Company(Base):
    __tablename__ = "company"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=False)
    company_url = Column(String(512), nullable=True)
    tax_id_number = Column(String(20), nullable=False)
    entity_type = enum_column(EntityTypeEnum, "entity_type_enum", nullable=False)
    entity_type_other = Column(String(255), nullable=True)
    ownership = enum_column(OwnershipEnum, "ownership_enum", nullable=True)
    ownership_other = Column(String(255), nullable=True)
    naics_code = Column(String(6), nullable=True)
    naics_description = Column(String(1024), nullable=True)
    onboarding_status = enum_column(OnboardingStatusEnum, "onboarding_status_enum", nullable=False, default=OnboardingStatusEnum.to_be_onboarded)
    step_in_progress = Column(Integer, default=0)

    @validates("company_name")
    def validate_company_name(self, key, value):
        if not is_valid_company_name(value):
            raise ValueError("Company name must not be empty or whitespace.")
        return value

    @validates("company_url")
    def validate_company_url(self, key, value):
        if value and not is_valid_url(value):
            raise ValueError("Invalid URL provided for company_url.")
        return value

    @validates("tax_id_number")
    def validate_tax_id(self, key, value):
        if not is_valid_tax_id(value):
            raise ValueError("Invalid Tax ID format. Use 'NN-NNNNNNN' or 9-digit format.")
        return value

    @validates("naics_code")
    def validate_naics_code(self, key, value):
        if value and not is_valid_naics(value):
            raise ValueError("NAICS code must be a 6-digit number.")
        return value


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    emailid = Column(String(255), nullable=False, unique=True)
    phonenumber = Column(String(20), nullable=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    user_type = enum_column(UserTypeEnum, "user_type_enum", nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    profile_picture = Column(String(1024), nullable=True)
    is_active = Column(Boolean, default=True)
    status = enum_column(ClientStatus, "client_status_enum", nullable=False)
    date_of_hiring = Column(Date)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    login_attempts = Column(Integer, default=0)
    language = Column(String(50), nullable=True, default='English')
    timezone = Column(String(100), nullable=True, default='UTC')
    mfa_method = Column(String(50), nullable=True)
    last_agreed_date = Column(DateTime(timezone=True), nullable=True)

    role = relationship("Role", backref="users", foreign_keys=[role_id])
    admin_profile = relationship("SalesAdminProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    manager_profile = relationship("SalesManagerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    rep_profile = relationship("SalesRepProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    users = relationship("User", back_populates="role")
   
