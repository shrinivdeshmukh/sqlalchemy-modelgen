from sqlalchemy import (String, Integer, Boolean, Float, 
                                Numeric, DateTime, Date, Table, Column, 
                                PrimaryKeyConstraint, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()

userinfo_metadata = DeclarativeBase.metadata


userinfo = Table('userinfo', 
            userinfo_metadata,
            Column('user_id',Integer,primary_key=True),
            Column('firstname',String(50),nullable=False),
            Column('lastname',String(50)),
            Column('dob',Date),
            Column('contact',Numeric,unique=True,nullable=False),
            Column('address',String(250)),
                         
        )


orders = Table('orders', 
            userinfo_metadata,
            Column('order_date',String(25)),
            Column('order_id',Integer,primary_key=True),
            Column('uid',Integer,ForeignKey('userinfo.user_id')),
            Column('vendor',String(10)),
            Column('address',String(250)),
                         
        )
