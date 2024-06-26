import enum

class OrderStatus(enum.Enum):
  NEW = 'NEW'
  SEND = 'SEND'
  COMPLETE = 'COMPLETE'