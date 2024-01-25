from hashlib import new
from pydoc import cli
from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
import sqlite3

root = Tk()
root.title('COMP3005 Final Project')
root.geometry("300x200")

click = StringVar()

def searchForUsers():
    conn = sqlite3.connect('store_database.db')
    c=conn.cursor()
    c.execute("SELECT * FROM user")
    users = c.fetchall()
    conn.commit()
    conn.close()
    return users

def listAllProducts():
    conn = sqlite3.connect('store_database.db')
    c=conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.commit()
    conn.close()
    return products

def searchUserOrder():
    conn = sqlite3.connect('store_database.db')
    c=conn.cursor()
    c.execute("Select product_name from products WHERE product_id in (Select product_id from user_orders WHERE username='%s')"%str(click.get()))
    products = c.fetchall()
    conn.commit()
    conn.close()
    newWindow = Toplevel(root)
    newWindow.title(click.get()+" Order List")
    newWindow.geometry("300x300")
    for product in products:
        Label(newWindow,text=product[0]).pack()

def searchAllOrders():
    conn = sqlite3.connect('store_database.db')
    c=conn.cursor()
    c.execute("Select * from products WHERE product_id in (Select product_id from user_orders)")
    products = c.fetchall()
    conn.commit()
    conn.close()

def searchStoreEmployees():
    conn = sqlite3.connect('store_database.db')
    c=conn.cursor()
    c.execute("Select * from employees WHERE work_location in (Select st_id from store)")
    results = c.fetchall()
    print(results)
    conn.commit()
    conn.close()

def searchWarehouseEmployees():
    conn = sqlite3.connect('store_database.db')
    c=conn.cursor()
    c.execute("Select * from employees WHERE work_location in (Select wh_id from warehouse)")
    results = c.fetchall()
    print(results)
    conn.commit()
    conn.close()

def searchAllEmployees():
    conn = sqlite3.connect('store_database.db')
    c=conn.cursor()
    c.execute("Select * from employees")
    results = c.fetchall()
    conn.commit()
    conn.close()
    return results

def getWh_id():
    conn = sqlite3.connect('store_database.db')
    c=conn.cursor()
    c.execute("Select wh_id from warehouse")
    results = c.fetchall()
    conn.commit()
    conn.close()
    return results

def getSt_id():
    conn = sqlite3.connect('store_database.db')
    c=conn.cursor()
    c.execute("Select st_id from store")
    results = c.fetchall()
    conn.commit()
    conn.close()
    return results

def searchWarehouseAddress():
    conn = sqlite3.connect('store_database.db')
    c=conn.cursor()
    c.execute("Select wh_location FROM warehouse WHERE wh_id='%s'"%click.get())
    results = c.fetchall()
    conn.commit()
    conn.close()
    newWindow = Toplevel(root)
    newWindow.title(click.get()+" Order List")
    newWindow.geometry("300x300")
    Label(newWindow,text="Address: "+results[0][0]).pack()

def searchStoreAddress():
    conn = sqlite3.connect('store_database.db')
    c=conn.cursor()
    c.execute("Select st_location FROM store WHERE st_id='%s'"%click.get())
    results = c.fetchall()
    conn.commit()
    conn.close()
    newWindow = Toplevel(root)
    newWindow.title(click.get()+" Order List")
    newWindow.geometry("300x300")
    Label(newWindow,text="Address: "+results[0][0]).pack()

def displayWarehouse():
    warehouseIDS = getWh_id()
    ids = []
    for id in warehouseIDS:
            ids.append(id[0])
        
    newWindow = Toplevel(root)
    newWindow.title("Warehouse ID's")
    newWindow.geometry("200x200")
    click.set(id[0])
    dmenu = OptionMenu(newWindow,click,*ids)
    dmenu.pack()
    btn = Button(newWindow,text="Search For Address",command=searchWarehouseAddress).pack()

def displayStore():
    storeIDS = getSt_id()
    ids = []
    for id in storeIDS:
            ids.append(id[0])
        
    newWindow = Toplevel(root)
    newWindow.title("Store ID's")
    newWindow.geometry("200x200")
    click.set(id[0])
    dmenu = OptionMenu(newWindow,click,*ids)
    dmenu.pack()
    btn = Button(newWindow,text="Search For Address",command=searchStoreAddress).pack()

def getOrder(name):
    conn = sqlite3.connect('store_database.db')
    c=conn.cursor()
    c.execute("Select product_name from products WHERE product_id in (Select product_id from user_orders WHERE username='%s')"%name)
    result = c.fetchall()
    conn.commit()
    conn.close()
    return result

def displayProducts():
    newWindow = Toplevel(root)
    newWindow.title("All Products")
    newWindow.geometry("500x600")
    main_frame = Frame(newWindow)
    main_frame.pack(fill=BOTH,expand=1)

    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT,fill=BOTH,expand=1)

    scrollBar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    scrollBar.pack(side=RIGHT,fill=Y)

    my_canvas.configure(yscrollcommand=scrollBar.set)
    my_canvas.bind('<Configure>',lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = Frame(my_canvas)

    my_canvas.create_window((0,0),window=second_frame,anchor="nw")

    products = listAllProducts()
    for product in products:
        Label(second_frame,text="Name: "+product[1]+" Amount: "+str(product[3])+" Location Stored At: "+product[2]).pack()

def displayAllOrders():
    newWindow = Toplevel(root)
    newWindow.title("All ORDERS")
    newWindow.geometry("500x600")
    m_frame = Frame(newWindow)
    m_frame.pack(fill=BOTH,expand=1)

    m_canvas = Canvas(m_frame)
    m_canvas.pack(side=LEFT,fill=BOTH,expand=1)

    scrollBar = ttk.Scrollbar(m_frame, orient=VERTICAL, command=m_canvas.yview)
    scrollBar.pack(side=RIGHT,fill=Y)

    m_canvas.configure(yscrollcommand=scrollBar.set)
    m_canvas.bind('<Configure>',lambda e: m_canvas.configure(scrollregion=m_canvas.bbox("all")))

    s_frame = Frame(m_canvas)

    m_canvas.create_window((0,0),window=s_frame,anchor="nw")

    users = searchForUsers()
    for user in users:
        Label(s_frame,text= user[0]+" Order List:").pack(pady=20, side= TOP, anchor="w")
        order = getOrder(user[0])
        for product in order:
            Label(s_frame,text="\tProduct Name: "+product[0]).pack(side= TOP, anchor="w")


def show():
    if clicked.get()=="Search For Users":
        newWindow = Toplevel(root)
        newWindow.title("All Users")
        newWindow.geometry("200x200")
        users = searchForUsers()
        usernames = []
        for user in users:
            usernames.append(user[0])
        
        click.set(usernames[0])
        dmenu = OptionMenu(newWindow,click,*usernames)
        dmenu.pack()
        btn = Button(newWindow,text="Search User Orders",command=searchUserOrder).pack()
    elif clicked.get()=="Search For Employees":
        newWindow = Toplevel(root)
        newWindow.title("All Employee's")
        newWindow.geometry("850x600")
        employeeList = searchAllEmployees()
    
        for employee in employeeList:
            Label(newWindow,text="Name: "+employee[0]+" Employee ID:"+str(employee[1])+" Address:"+employee[3]+" Phone Number: "+ employee[4]+" Work Location: "+employee[5]).pack()
    elif clicked.get()=="Search For Products":
        displayProducts()
    elif clicked.get()=="Search For Warehouse Locations":
        displayWarehouse()
    elif clicked.get()=="Search For Store Locations":
        displayStore()
    elif clicked.get()=="Search For All User Orders":
        displayAllOrders()
    


clicked = StringVar()
clicked.set("Search For Users")

drop = OptionMenu(root,clicked,"Search For Users","Search For Employees","Search For Products","Search For Warehouse Locations","Search For Store Locations","Search For All User Orders")
drop.pack()

btn = Button(root,text="Search",command=show).pack()

root.mainloop()