from src.model import db
from sqlalchemy.schema import Column
from sqlalchemy.types import String, DECIMAL, Integer


class Employee(db.Model):

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))    
    email = Column(String(100))
    password = Column(String(60))
    job = Column(String(100))
    salary = Column(DECIMAL(10, 2))
    
    
    def __init__(self, name, email, password, job, salary):
        self.name = name
        self.email = email
        self.password = password
        self.job = job
        self.salary = salary
        
    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "password": self.password
        } 
        


    def all_data(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "job": self.job,
            "salary": self.salary
        }

