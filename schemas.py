from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime


# Base schemas for user
class UserBase(BaseModel):
    first_name: str
    last_name: Optional[str]
    profile_picture: Optional[str]
    phonenumber: Optional[str]


class UserCreate(UserBase):
    emailid: str
    password: str


# Client schemas
class ClientBase(BaseModel):
    company_name: str
    full_name: str
    contact_number: str
    email: str
    address: Optional[str]
    pincode: Optional[str]
    subscription_type: str
    onboarding_status: str
    payment_status: str
    plan_due_date: date
    billing_period: str
    assigned_salesperson_id: Optional[int]

    class Config:
        from_attributes = True


class ClientListItem(BaseModel):
    id: int
    full_name: str
    client_status: str
    subscription_type: Optional[str]
    onboarding_status: Optional[str]

    class Config:
        from_attributes = True


# Appointment schemas
class AppointmentBase(BaseModel):
    title: str
    description: Optional[str]
    appointment_time: datetime
    email: str
    meeting_link: Optional[str]
    company_id: int
    assigned_to_id: Optional[int]

    class Config:
        from_attributes = True


# Dashboard schemas
class PerformanceChart(BaseModel):
    month: str
    target: int
    achieved: int


class UpcomingAppointment(BaseModel):
    title: str
    description: Optional[str]
    meeting_link: Optional[str]


class AdminDashboardOverview(BaseModel):
    totalAppointments: int
    totalLeads: int
    totalSalesManager: int
    totalSalesRepresentative: int
    performanceChart: List[PerformanceChart]
    upcomingAppointments: List[UpcomingAppointment]


class ManagerDashboardOverview(BaseModel):
    totalAppointments: int
    totalLeads: int
    totalSalesRepresentative: int
    performanceChart: List[PerformanceChart]
    upcomingAppointments: List[UpcomingAppointment]


class RepDashboardOverview(BaseModel):
    totalAppointments: int
    totalLeads: int
    totalSubscriptions: int
    totalTarget: float
    performanceChart: List[PerformanceChart]
    upcomingAppointments: List[UpcomingAppointment]


# Sales personnel schemas
class SalesPersonUnderManager(BaseModel):
    id: int
    full_name: str
    emailid: str
    totalLeads: int
    totalSubscriptions: int
    feedback: Optional[str]
    date_of_hiring: Optional[date]
    status: str

    class Config:
        from_attributes = True


class SalesManagerListOut(BaseModel):
    first_name: str
    last_name: Optional[str]
    phonenumber: Optional[str]
    emailid: str
    targetSales: int
    sales: int
    subscription: int
    convPercentage: float
    rating: float
    revenue: int
    targetRevenue: int
    achieved: int
    achievedPercentage: float
    address: Optional[str]
    pincode: Optional[str]
    showAllSalesPerson: bool

    class Config:
        from_attributes = True


class SalesManager(BaseModel):
    full_name: str
    emailid: str
    totalSalesRep: int
    totalSubscriptions: int
    feedback: Optional[str]
    date_of_hiring: Optional[date]
    status: str


class SalesRepresentative(BaseModel):
    full_name: str
    emailid: str
    totalLeads: int
    totalSubscriptions: int
    feedback: Optional[str]
    date_of_hiring: Optional[date]
    status: str


class SalesRepWithTarget(BaseModel):
    id: int
    full_name: str
    emailid: str
    totalLeads: int
    totalSubscriptions: int
    target: Optional[int] = None

    class Config:
        from_attributes = True


class BulkTargetUpdate(BaseModel):
    rep_ids: Optional[List[int]]
    target: int


class BulkDeleteReps(BaseModel):
    rep_ids: Optional[List[int]]


class SalesRepresentativeDetailOut(BaseModel):
    first_name: str
    last_name: Optional[str]
    phonenumber: Optional[str]
    emailid: str
    role: str
    targetLeads: int
    leads: int
    subscription: int
    convPercentage: float
    targetRevenue: int
    revenue: int
    achieved: int
    achievedPercentage: float
    archived: int
    archivedPercentage: float
    rating: float
    address: Optional[str]
    pincode: Optional[str]
    showAllLeads: bool

    class Config:
        from_attributes = True


# Settings
class ChangePassword(BaseModel):
    oldPassword: str
    newPassword: str


class UpdateName(BaseModel):
    first_name: str
    last_name: Optional[str] = None


class AdminProfileResponse(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    emailid: str
    phonenumber: Optional[str]
    profile_picture: Optional[str]

    class Config:
        orm_mode = True
