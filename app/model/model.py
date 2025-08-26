from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer,String,DateTime,func
from ..database.database import Base
from datetime import datetime


class User(Base):
    __tablename__= "userr"
    
    id: Mapped [int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped [str] = mapped_column(String, nullable=False)
    user_name: Mapped [str] = mapped_column(String, nullable=False,unique=True)
    password: Mapped [str] = mapped_column(String,nullable=False,unique=True)
    email: Mapped [str] = mapped_column(String, nullable=False,unique=True)
    phone_no: Mapped [str] = mapped_column(String, unique=True,nullable=False)
    gender: Mapped [str] = mapped_column(String)
    created_at: Mapped[datetime]= mapped_column(DateTime(timezone=True),server_default=func.now())
    update_ar: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    
    
    