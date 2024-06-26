from storage.datatypes import OrderStatus 
from models.BaseModel import *
from typing import get_args

class Order(BaseModel):
  __tablename__ = 'orders'
  
  id: Mapped[int] = mapped_column(primary_key=True)
  short: Mapped[str] = mapped_column(nullable=False)
  link: Mapped[str] = mapped_column(nullable=False)
  watch: Mapped[int] = mapped_column(default=0)
  responses: Mapped[int] = mapped_column(default=0)
  price: Mapped[float] = mapped_column(default=0.00)
  created_at:Mapped[datetime.datetime] = mapped_column(
      DateTime(timezone='Europe/Moscow'), server_default=func.now()
  )
  status: Mapped[OrderStatus] = mapped_column(Enum(
    OrderStatus,
    name="order_status_enum",
    create_constraint=True,
    validate_strings=True,
  ))
