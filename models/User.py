from models.BaseModel import *

class User(BaseModel):
  __tablename__ = 'users'
  
  @classmethod
  def primary_key(cls):
    return cls.user_id
  
  user_id: Mapped[int] = mapped_column(primary_key=True)
  user_name: Mapped[Optional[str]]
  user_nickname: Mapped[Optional[str]]