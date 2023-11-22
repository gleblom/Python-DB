import sqlite3
from tkinter import *  
from tkinter import ttk
import re

conn = sqlite3.connect('Database.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS Machine(
            MachineID int PRIMARY KEY,
            Machine text);""")
cur.execute("""CREATE TABLE IF NOT EXISTS MachineMaterial(
            ID int PRIMARY KEY,
            MachineID int,
            MaterialID int);""")
cur.execute("""CREATE TABLE IF NOT EXISTS Material(
            MaterialID int PRIMARY KEY,
            Material text);""")
cur.execute("""INSERT INTO Machine(MachineID, Machine) VALUES
            (1, "S1AR2"), (2, "D2D10A"), (3, "FR10A4");""")
cur.execute("""INSERT INTO Material(MaterialID, Material) VALUES
            (1, "Steel"), (2, "Aluminum"), (3, "Bronze"), (4, "Tin"),
            (5, "Copper"), (6, "Lead");""")
cur.execute("""INSERT INTO MachineMaterial(ID, MachineID, MaterialID) VALUES
            (1, 1, 1), (2, 1, 2), (3, 2, 3), (4, 2, 4),
            (5, 3, 5), (6, 3, 6), (7, 2, 5);""")
def Add_Machine():
    value = entry.get()
    value2 = entry.get()
    Machine = (value, value2)
    return cur.execute("INSERT INTO Machine(MachineID, Machine)VALUES(?, ?)", Machine)
def Add_Matertial():
    value3 = entry3.get()
    value4 = entry4.get()
    Material = (value3, value4)
    return cur.execute("INSERT INTO Material(MaterialID, Material)VALUES(?, ?)", Material)
def Add_MachineMatertial():
    value5 = entry5.get()
    value6 = entry6.get()
    value7 = entry7.get()
    MachineMaterial = (value3, value4)
    return cur.execute("INSERT INTO MachineMaterial(ID, MachineID, MaterialID)VALUES(?, ?, ?)", MachineMaterial)
def IsValid(newval):
    return re.match('^\0{0,1}\d{0,999999}$', newval) is not None
   
root = Tk()
root.title("Интерфейс БД")
root.geometry("600x500")

check = (root.register(IsValid), "%P")

tab_control = ttk.Notebook(root)  
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Ввод данных')  
tab_control.add(tab2, text='Просмотр данных') 

label = ttk.Label(tab1, text = "Таблица Станки")
label.pack(anchor=N, padx=6, pady=6)
label = ttk.Label(tab1, text = "ID Станка")
label.place(x = 180, y = 40)
label = ttk.Label(tab1, text = "Название Станка")
label.place(x = 140, y = 80)

entry = ttk.Entry(tab1, validate = "key", validatecommand = check)
entry2 = ttk.Entry(tab1)
entry.pack(anchor = N, padx = 8, pady = 9)
entry2.pack(anchor = N, padx = 8, pady = 9)

btn = ttk.Button(tab1, text = "Добавить", command = Add_Machine)
btn.pack(anchor = N, padx = 6, pady = 6)

label = ttk.Label(tab1, text = "Таблица Материалы")
label.pack(anchor = N, padx = 6, pady = 6)
label = ttk.Label(tab1, text = "ID Материала")
label.place(x = 155, y = 185)
label = ttk.Label(tab1, text = "Название Материала")
label.place(x = 115, y = 225)

entry3 = ttk.Entry(tab1, validate = "key", validatecommand = check)
entry4 = ttk.Entry(tab1)
entry3.pack(anchor = N, padx = 8, pady = 9)
entry4.pack(anchor = N, padx = 8, pady = 9)

btn = ttk.Button(tab1, text = "Добавить", command = Add_Matertial)
btn.pack(anchor = N, padx = 6, pady = 6)

label = ttk.Label(tab1, text = "Таблица ID Материалов и Станков")
label.pack(anchor=N, padx=6, pady=6)
label = ttk.Label(tab1, text = "ID Связи")
label.place(x = 185, y = 330)
label = ttk.Label(tab1, text = "ID Станка")
label.place(x = 180, y = 370)
label = ttk.Label(tab1, text = "ID Материала")
label.place(x = 155, y = 410)
            
entry5 = ttk.Entry(tab1, validate = "key", validatecommand = check)
entry6 = ttk.Entry(tab1, validate = "key", validatecommand = check)
entry7 = ttk.Entry(tab1, validate = "key", validatecommand = check)

entry5.pack(anchor = N, padx = 8, pady = 9)
entry6.pack(anchor = N, padx = 8, pady = 9)
entry7.pack(anchor = N, padx = 8, pady = 9)

btn = ttk.Button(tab1, text = "Добавить", command = Add_MachineMatertial)
btn.pack(anchor = N, padx = 6, pady = 6)

cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
            Machine.MachineID = MachineMaterial.MachineID)
            JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID);""") 
data = cur.fetchall()
cur.execute("SELECT Machine FROM Machine;")
mch = cur.fetchall()
cur.execute("Select Material FROM Material;")
mtl = cur.fetchall()
combobox = ttk.Combobox(tab2, values = mch)
combobox.pack(anchor = N, padx = 6, pady = 6)
combobox2 = ttk.Combobox(tab2, values = mtl)
combobox2.pack(anchor = N, padx = 6, pady = 6)

def sort():
    selection = combobox.get()
    selection2 = combobox2.get()
    if selection != "" and selection2 != "":
                cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
                Machine.MachineID = MachineMaterial.MachineID)
                JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID
                Where Machine = selection, Material = selection2);""")
    if selection != "" and selection2 == "":
                cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
                Machine.MachineID = MachineMaterial.MachineID)
                JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID
                Where Machine = selection);""")
    if selection == "" and selection2 != "":
                cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
                Machine.MachineID = MachineMaterial.MachineID)
                JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID
                Where Material = selection2);""")
    if selection == "" and selection2 == "":
                cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
                Machine.MachineID = MachineMaterial.MachineID)
                JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID);""") 
                
    [tree.delete(i) for i in tree.get_children()]
    [tree.insert("", END, values = row) for row in cur.fetchall()]
btn = ttk.Button(tab2, text = "Применить")
btn.pack(anchor = N, padx = 6, pady = 6)  

columns = ("Станок", "Материал")
tree = ttk.Treeview(tab2, columns = columns, show = "headings")
tree.pack(fill = BOTH, expand = 1)
tree.heading("Станок", text = "Станок")
tree.heading("Материал", text = "Материал")

tree.column("#1", anchor = N)
tree.column("#2", anchor = N)

for stanok in data:
    tree.insert("", END, values = stanok)


tab_control.pack(expand = 1, fill = 'both')

root.mainloop()

