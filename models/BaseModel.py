from sqlalchemy.orm import DeclarativeBase
from typing import Optional, List, Literal
from sqlalchemy import String, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
import datetime, json, copy
from sqlalchemy.orm import Session
from storage.database import engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import table
from sqlalchemy.sql import exists, select

class BaseModel(DeclarativeBase):
  
  @classmethod
  def primary_key(cls):
    return cls.id
  
  @classmethod
  def from_dict(cls, dict: dict):
    self = cls()
    for key in dict:
      self.__setattr__(key, dict[key])
    
    return self
  
  def save(self):
    with Session(engine) as session:
      obj = copy.deepcopy(self)
      stmt = select(exists(self.__class__).where(
        self.primary_key() == self.getAttribute('id')
      ))
      ex = session.execute(stmt).scalar()
      if ex:
        session.merge(obj)
      else:
        session.add(obj)
      
      session.commit()
  
  @classmethod
  def firstOrCreate(cls, attrs: dict):
    obj = cls.from_dict(attrs)
    record = cls.find(obj.getAttribute(cls.primary_key().name))
    
    if record:
      return record
    
    obj.save()
    return obj
  
  @classmethod
  def updateOrCreate(cls, attrs: dict, upd: list = []):
    obj = cls.from_dict(attrs)
    record = cls.find(obj.id)
    
    if record and len(upd):
      updation = { k: obj.getAttribute(k) for k in upd }
      with Session(engine) as session:
        session.query(cls).update(updation)
        
      for k in updation:
        record.setAttribute(k, updation[k])
      
      return record
    else:
      obj.save()
      return obj
  
  @classmethod
  def find(cls, id):
    with Session(engine) as session:
      return session.query(cls).where(cls.primary_key() == id).first()
    
  def update(self, upd=[]):
    attrs = self.getAttributes()
    if upd:
      for_update = {k: attrs[k] for k in upd }
    else:
      for_update = {k: attrs[k] for k in attrs if k != 'id' }
      
    with Session(engine)  as session:
      session.query(self.__class__).where(self.__class__.id==attrs['id']).update(for_update)
      session.commit()
    
    for k in upd:
      self.setAttribute(k, upd[k])
      
    return self
  
  @classmethod
  def rowExists(cls, id) -> bool:
    with Session(engine) as session:
      return session.query(exists(cls).where(cls.id == id)).scalar()
  
  def getAttributes(self) -> dict:
    return {k: self.__dict__[k] for k in self.__dict__ if k[:1] != '_'}
  
  def getAttribute(self, name) -> any:
    return self.__dict__[name] if name in self.__dict__ else None

  def setAttribute(self, name, val) -> None:
    self.__dict__[name] = val
  
  def __repr__(self) -> str:
    attrs = self.getAttributes()
    return "\n" + self.__class__.__name__ + "\n" + "\n".join([f"{key}: {attrs[key]}" for key in attrs]) + "\n"