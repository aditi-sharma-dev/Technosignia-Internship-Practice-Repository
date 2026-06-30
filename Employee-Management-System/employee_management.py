import mysql.connector
try:
    conn=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aditi9770380",
        database="employee_db",
        port=3306
    )
    if conn.is_connected():
        print("Database Connected Successfully")
except Exception as e:
    print("Error:",e)



def add_employee():
    try:
        conn=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aditi9770380",
        database="employee_db",
        port=3306
    )
        cursor=conn.cursor()
        Emp_Id=int(input("Enter Employee Id:"))
        Name=input("Enter name of employee:")
        Email=input("Enter email of employee:")
        Phone_No=input("Enter phone no of employee:")
        Address=input("Enter address of employee:")
        Department=input("Enter department of employee:")
        Designation=input("Enter job profile of employee:")
        Salary=float(input("Enter salary of employee:"))
        
        employee={
            "Emp_Id":Emp_Id,
            "Name":Name,
            "Email":Email,
            "Phone_No":Phone_No,
            "Address":Address,
            "Department":Department,
            "Designation":Designation,
            "Salary":Salary
        }
        query = """
        Insert into employee values(%s,%s,%s,%s,%s,%s,%s,%s)"""
        values=(employee["Emp_Id"],
                employee["Name"],
                employee["Email"],
                employee["Phone_No"],
                employee["Address"],
                employee["Department"],
                employee["Designation"],
                employee["Salary"]
                )
       
        cursor.execute(query,values)
        conn.commit()
        print("Employee added succesfully")
        
    except Exception as e:
        print("Error",e)
    finally:
        if conn.is_connected():
            conn.close()


def view_employee():
    try:
        conn=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aditi9770380",
        database="employee_db",
        port=3306
    )
        cursor=conn.cursor()
        query="select * from employee"
        cursor.execute(query)
        records=cursor.fetchall()
        print("Employee Records")
        for row in records:
            print(row)
    
    except Exception as e:
        print("Error:",e)
    finally:
        if conn.is_connected():
            conn.close()
        


def search_employee():
    try:
        conn=mysql.connector.connect(
            host="localhost",
            user="root",
            password="Aditi9770380",
            database="employee_db",
            port=3306
        )
        cursor=conn.cursor()
        Emp_Id=int(input("Enter the employee id:"))
        query="Select * from employee where Emp_Id=%s"
        cursor.execute(query,(Emp_Id,))
        record=cursor.fetchone()
        if record:
            print("Employee Found")
            print(record)
        else:
            print("Emoloyee Not Found")
    except Exception as e:
        print("Error:",e)
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
  


def update_employee():
    try:
        conn=mysql.connector.connect(
            host="localhost",
            user="root",
            password="Aditi9770380",
            database="employee_db",
            port=3306
        )
        cursor=conn.cursor()
        Emp_Id=int(input("Enter Employee id to update:"))
        
        Name=input("Enter new name:")
        Email=input("Enter new email:")
        Phone_No=input("Enter new phone no:")
        Address=input("Enter new address:")
        Department=input("Enter new department:")
        Designation=input("Enter new designation:")
        Salary=float(input("Enter new salary:"))
        
        query=""" update employee 
        set Name=%s,
             Email=%s,
             Phone_No=%s,
             Address=%s,
             Department=%s,
             Designation=%s,
             Salary=%s  
        where Emp_Id=%s"""
        values=(Name,Email,Phone_No,Address,Department,Designation,Salary,Emp_Id)
        cursor.execute(query,values)
        conn.commit()
        if cursor.rowcount>0:
            print("Employee update successfully")
        else:
            print("Employee id not found")
    except Exception as e:
        print("Error:",e)
    finally:
        if conn.is_connected():
            conn.close()


def delete_employee():
      try:
        conn=mysql.connector.connect(
            host="localhost",
            user="root",
            password="Aditi9770380",
            database="employee_db",
            port=3306
        )
        cursor=conn.cursor()
        Emp_Id=int(input("Enter Employee id to delete:"))
        query="Delete  from employee where Emp_Id=%s"
        cursor.execute(query,(Emp_Id,))
        conn.commit()
        if cursor.rowcount>0:
            print("Employee delete successfully")
        else:
            print("Employee id not found")
        
      except Exception as e:
        print("Error:",e)
      finally:
        if conn.is_connected():
            conn.close()

def menu():
    while True:
        print("Employee Management System")
        print("1.Add Employee")
        print("2.View Employee")
        print("3.Search Employee")
        print("4. Update Employee")
        print("5.Delete Employee")
        print("6.Exit")
        choice=int(input("Enter your choice:"))
        if choice==1:
            add_employee()
        elif choice==2:
            view_employee()
        elif choice==3:
            search_employee()
        elif choice==4:
            update_employee()
        elif choice==5:
            delete_employee()
        elif choice==6:
            print("Thank you for using Employee Management System")
            break
        else:
            print("Invalid Choice! Plz try again")
menu()
