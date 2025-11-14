import sqlite3

class EmployeeDB:
    def __init__(self, db_name="employees.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            department TEXT,
            salary REAL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_employee(self, name, age, department, salary):
        query = "INSERT INTO employees (name, age, department, salary) VALUES (?, ?, ?, ?)"
        self.conn.execute(query, (name, age, department, salary))
        self.conn.commit()

    def get_employees(self):
        cursor = self.conn.execute("SELECT * FROM employees")
        return cursor.fetchall()

    def update_employee(self, emp_id, name, age, department, salary):
        query = "UPDATE employees SET name=?, age=?, department=?, salary=? WHERE id=?"
        self.conn.execute(query, (name, age, department, salary, emp_id))
        self.conn.commit()

    def delete_employee(self, emp_id):
        query = "DELETE FROM employees WHERE id=?"
        self.conn.execute(query, (emp_id,))
        self.conn.commit()
import streamlit as st


db = EmployeeDB()

st.title("Employee Management System ")

menu = ["Add Employee", "View Employees", "Update Employee", "Delete Employee"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- Add Employee ----------------
if choice == "Add Employee":
    st.subheader("Add New Employee")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18, max_value=70, step=1)
    department = st.text_input("Department")
    salary = st.number_input("Salary", min_value=0.0)

    if st.button("Add"):
        db.add_employee(name, age, department, salary)
        st.success(f"Employee '{name}' added successfully!")

# ---------------- View Employees ----------------
elif choice == "View Employees":
    st.subheader("Employee List")
    data = db.get_employees()
    st.table(data)

# ---------------- Update Employee ----------------
elif choice == "Update Employee":
    st.subheader("Update Employee")

    data = db.get_employees()
    emp_ids = [row[0] for row in data]

    emp_id = st.selectbox("Select Employee ID", emp_ids)

    name = st.text_input("New Name")
    age = st.number_input("New Age", min_value=18, max_value=70, step=1)
    department = st.text_input("New Department")
    salary = st.number_input("New Salary", min_value=0.0)

    if st.button("Update"):
        db.update_employee(emp_id, name, age, department, salary)
        st.success("Employee updated successfully!")

# ---------------- Delete Employee ----------------
elif choice == "Delete Employee":
    st.subheader("Delete Employee")

    data = db.get_employees()
    emp_ids = [row[0] for row in data]

    emp_id = st.selectbox("Select Employee ID to Delete", emp_ids)

    if st.button("Delete"):
        db.delete_employee(emp_id)
        st.warning("Employee deleted successfully!")
