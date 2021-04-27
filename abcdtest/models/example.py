from sqlalchemy import (String, Integer, Boolean, Float, 
                                Numeric, DateTime, Date, Table, Column, 
                                PrimaryKeyConstraint, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()

example_metadata = DeclarativeBase.metadata


example_user_table = Table('example_user_table', 
            example_metadata,
            Column('id',Integer,primary_key=True),
            Column('firstname',String(50),nullable=False),
            Column('lastname',String(50)),
                         
        )


example_meta_table = Table('example_meta_table', 
            example_metadata,
            Column('meta_id',Integer,ForeignKey('example_user_table.id')),
            Column('address',String(250)),
            Column('contact',Numeric,unique=True),
                         
        )
