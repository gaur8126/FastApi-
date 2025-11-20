from fastapi import FastAPI,HTTPException
from models import Employee
from typing import List


employee_db: List[Employee]  = []

app = FastAPI()

# Read all employees
@app.get('/employees',response_model=List[Employee])
def get_employees():
    return employee_db


# Read specific employee
@app.get('/employees/{epm_id}',response_model=Employee)
def get_employee(emp_id: int):
    for index,employee in enumerate(employee_db):
        if employee.id == emp_id:
            return employee_db[index]
        
    raise HTTPException(status_code=404, detail="Employee not found")


# 3. Add an employee
@app.post('/add_employees',response_model=Employee)
def add_employee(new_emp: Employee):
    for employee in employee_db:
        if employee.id == new_emp.id:
            raise HTTPException(status_code=400, detail="Employee already exist")
        
    employee_db.append(new_emp)
    return new_emp
    

# 4. Update an employee
@app.put('/update_employee/{emp_id}',response_model=Employee)
def update_employee(emp_id:int, updated_employee:Employee):
    for index, employee in enumerate(employee_db):
        if employee.id == emp_id:
            employee_db[index] = updated_employee

    raise HTTPException(status_code=404, detail="Employee not found")


# 5. Delete Employee
@app.delete("/delete_employee/{emp_id}")
def delete_employee(emp_id:int):
    for index, employee in enumerate(employee_db):
        if employee.id == emp_id:
            del employee_db[index]
            return {'message':'Employee deleted successfully'}
        
    raise HTTPException(status_code= 404, detail="Employee not found")


