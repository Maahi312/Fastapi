from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Column
from enum import Enum

def enum_column(enum_cls, name, default=None, nullable=False):
    return Column(
        SQLEnum(*[e.value for e in enum_cls], name=name, create_type=True),
        default=default.value if default else None,
        nullable=nullable
    )
class ClientStatus(str, Enum):
    active = "Active"
    inactive = "Inactive"
   
class ActivePlan(str, Enum):
    free = "free"
    standard = "standard"
    premium = "premium"

class PaymentStatus(str, Enum):
    pending = "Pending"
    paid = "Paid"
    overdue = "Overdue"

class BillingPeriod(str, Enum):
    monthly = "Monthly"
    quarterly = "Quarterly"
    yearly = "Yearly"

class AppointmentStatus(str, Enum):
    scheduled = "Scheduled"
    completed = "Completed"
    cancelled = "Cancelled"

class SubscriptionStatus(str, Enum):
    pending = "Pending"
    active = "Active"
    cancelled = "Cancelled"
    
class UserTypeEnum(str, Enum):
    client = "client"
    sales_rep = "sales_rep"
    sales_manager = "sales_manager"
    sales_admin = "sales_admin"
    super_admin = "super_admin"
    admin = "admin"
    approver = "approver"


    
class OnboardingStatusEnum(str, Enum):
    to_be_onboarded = "to-be-onboarded"
    onboarding_in_progress = "on-boarding-in-progress"
    onboarding_done = "on-boarding-done"

    
class EntityTypeEnum(str, Enum):
    limited_liability_company = "Limited Liability Company (LLC)"
    c_corporation = "C Corporation"
    s_corporation = "S Corporation"
    non_profit_organization = "Non-profit Organization"
    trust_estate = "Trust/Estate"
    government_entity = "Government Entity"
    foreign_entity = "Foreign Entity (Non-U.S.)"
    other = "Other"

    
class OwnershipEnum(str, Enum):
    privately_owned = "Privately Owned"
    publicly_traded = "Publicly Traded"
    government_owned = "Government-Owned"
    non_profit = "Non-Profit"
    woman_owned = "Woman-Owned"
    minority_owned = "Minority-Owned"
    veteran_owned = "Veteran-Owned"
    joint_venture = "Joint Venture"
    family_owned = "Family-Owned"
    other = "Other"
