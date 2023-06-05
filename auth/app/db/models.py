
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class GrantedPermissionEntity(Base):
    __tablename__ = 'permission_table'

    user_id = Column(Integer, primary_key=True)
    permission = Column(String, primary_key=True)
