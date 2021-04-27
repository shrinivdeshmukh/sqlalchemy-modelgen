# coding: utf-8
from sqlalchemy import Column, DECIMAL, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ExampleUserTable(Base):
    __tablename__ = 'example_user_table'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50))


t_example_meta_table = Table(
    'example_meta_table', pqrs_metadata,
    Column('meta_id', ForeignKey('example_user_table.id'), index=True),
    Column('address', String(250)),
    Column('contact', DECIMAL(10, 0), unique=True)
)
