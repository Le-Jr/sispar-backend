from sqlalchemy import Date, ForeignKey, func, text
from src.model import db
from sqlalchemy.schema import Column
from sqlalchemy.types import String, DECIMAL, Integer

class Refund(db.Model):
    __tablename__ = 'refund'
   
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee = Column(String(200), nullable=False)
    company = Column(String(50), nullable=False)
    installment_num = Column(Integer, nullable=False)
    description = Column(String(255))
    date = Column(Date, nullable=False, server_default=text('CURRENT_DATE()'))
    refund_type = Column(String(30), nullable=False)
    cost_center = Column(String(100), nullable=False)
    intern_order = Column(String(25))
    division = Column(String(25))
    pep = Column(String(25))
    currency = Column(String(10), nullable=False)
    km_distance = Column(String(255))
    km_value = Column(DECIMAL(10,2))
    incoming_value = Column(DECIMAL(10,2), nullable=False)
    expenses = Column(DECIMAL(10,2))
    id_employee = Column(Integer, ForeignKey('employee.id'), nullable=False)
    status = Column(String(30), nullable=False)


    
    def __init__(self, employee, company, installment_num, description, date, refund_type, cost_center, intern_order, division, pep, currency, km_distance,km_value, incoming_value, expenses, id_employee, status):
        
        self.employee = employee
        self.company = company
        self.installment_num = installment_num
        self.description = description
        self.date = date
        self.refund_type = refund_type
        self.cost_center = cost_center
        self.intern_order = intern_order
        self.division = division
        self.pep = pep
        self.currency = currency
        self.km_distance = km_distance
        self.km_value = km_value
        self.incoming_value = incoming_value
        self.expenses = expenses
        self.id_employee = id_employee
        self.status = status
    
    
    def to_dict(self) -> dict:
        return {
            "employee": self.employee,
            "company": self.company,
            "installment_num": self.installment_num,
            "description": self.description,
            "date": self.date,
            "refund_type": self.refund_type,
            "cost_center": self.cost_center,  
            "intern_order": self.intern_order, 
            "division": self.division, 
            "pep": self.pep, 
            "currency": self.currency,
            "km_distance": self.km_distance, 
            "km_value": self.km_value, 
            "incoming_value": self.incoming_value,
            "expenses": self.expenses, 
            "id_employee": self.id_employee, 
            "status": self.status, 
        }
        
    