import sqlite3
from tkinter import *  
from tkinter import ttk
import re
from tkinter.messagebox import showerror, showwarning, showinfo

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

def Datadd():
    cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
            Machine.MachineID = MachineMaterial.MachineID)
            JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID);""")
    data = cur.fetchall()
    for stanok in data:
        tree.insert("", END, values = stanok)

def Add_Machine():
    val = entry.get()
    mass = [(val)]
    cur.execute("""SELECT Machine FROM Machine""")
    tblv = cur.fetchall()
    nw = []
    for i in range(len(tblv)):
        for j in range(len(tblv[0])):
            nw.append(tblv[i][j])
    for i in nw:
        if all(elem in i for elem in mass):
            entry.delete(0, END)
            showerror(title="Ошибка", message="Ошибка: введённое значение уже присутствует в таблице!")
            return False
    cur.execute("""SELECT * FROM Machine""")
    M = cur.fetchall()
    value = M[len(M)-1][0]+1
    value2 = entry.get()
    Machine = (value, value2)
    cur.execute("INSERT INTO Machine(MachineID, Machine)VALUES(?, ?)", Machine)
    cur.execute("SELECT Machine FROM Machine")
    res = cur.fetchall()
    combobox['values'] = res
    combobox3['values'] = res
    combobox5['values'] = res
    entry.delete(0, END)
    

def Add_Matertial():
    val = entry2.get()
    mass = [(val)]
    cur.execute("""SELECT Material FROM Material""")
    tblv = cur.fetchall()
    nw = []
    for i in range(len(tblv)):
        for j in range(len(tblv[0])):
            nw.append(tblv[i][j])
    for i in nw:
        if all(elem in i for elem in mass):
            entry2.delete(0, END)
            showerror(title="Ошибка", message="Ошибка: введённое значение уже присутствует в таблице!")
            return False
    cur.execute("""SELECT * FROM Material""")
    M = cur.fetchall()
    value = M[len(M)-1][0]+1
    value2 = entry2.get()
    Material = (value, value2)
    cur.execute("INSERT INTO Material(MaterialID, Material)VALUES(?, ?)", Material)
    cur.execute("SELECT Material FROM Material")
    res = cur.fetchall()
    combobox2['values'] = res
    combobox4['values'] = res
    combobox6['values'] = res
    entry2.delete(0, END)

def Add_MachineMatertial():
    selection = combobox.get()
    selection2 = combobox2.get()
    new_values = [selection, selection2]
    cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
            Machine.MachineID = MachineMaterial.MachineID)
                JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID);""")
    tbl_values = cur.fetchall()
    for i in tbl_values:
        if all(elem in i for elem in new_values):
            combobox.set("")
            combobox2.set("")
            showerror(title="Ошибка", message="Ошибка: введённые значения уже присутствует в таблице!")
            return False
    cur.execute("""SELECT * FROM Machine WHERE Machine =:cbx""", {"cbx": selection})
    MCH = cur.fetchall()
    cur.execute("""SELECT * FROM Material WHERE Material =:cbx""", {"cbx": selection2})
    MTL = cur.fetchall()
    cur.execute("""SELECT * FROM MachineMaterial""")
    MCL = cur.fetchall()
    value = MCL[len(MCL)-1][0]+1
    value2 = MCH[0][0]
    value3 = MTL[0][0]
    MachineMaterial = (value, value2, value3)
    cur.execute("INSERT INTO MachineMaterial(ID, MachineID, MaterialID)VALUES(?, ?, ?)", MachineMaterial)
    cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
                Machine.MachineID = MachineMaterial.MachineID)
                JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID);""")
    [tree.delete(i) for i in tree.get_children()]
    [tree.insert("", END, values = row) for row in cur.fetchall()]
    combobox.set("")
    combobox2.set("")

def sort():
    selection = combobox3.get()
    selection2 = combobox4.get()
    if selection2 == "":
        cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
                    Machine.MachineID = MachineMaterial.MachineID)
                    JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID)
                    WHERE Machine =:selection""",
                    {"selection": selection})
    if selection == "":
            cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
                    Machine.MachineID = MachineMaterial.MachineID)
                    JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID)
                    WHERE Material =:selection2 """,
                    {"selection2": selection2})
    if selection != "" and selection2 != "":
        cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
                Machine.MachineID = MachineMaterial.MachineID)
                JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID)
                WHERE Machine =:selection AND Material =:selection2 """,
                {"selection": selection, "selection2": selection2})
    if selection == "" and selection2 == "":
            cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
                Machine.MachineID = MachineMaterial.MachineID)
                JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID);""")        
    [tree.delete(i) for i in tree.get_children()]
    [tree.insert("", END, values = row) for row in cur.fetchall()]

def sort_off():
    cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
                Machine.MachineID = MachineMaterial.MachineID)
                JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID);""")        
    [tree.delete(i) for i in tree.get_children()]
    [tree.insert("", END, values = row) for row in cur.fetchall()]
    combobox3.set("")
    combobox4.set("")
    
def data_box():
    cur.execute("SELECT Machine FROM Machine;")
    mch = cur.fetchall()
    cur.execute("Select Material FROM Material;")
    mtl = cur.fetchall()
    return mch, mtl

def delete_data():
    selection = combobox5.get()
    selection2 = combobox6.get()
    if selection != "" and selection2 == "":
        cur.execute("""DELETE FROM Machine WHERE Machine =:selection""", {"selection": selection})
        combobox5.set("")
        cur.execute("SELECT Machine FROM Machine")
        res = cur.fetchall()
        combobox['values'] = res
        combobox3['values'] = res
        combobox5['values'] = res
        cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
                Machine.MachineID = MachineMaterial.MachineID)
                JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID);""")
        [tree.delete(i) for i in tree.get_children()]
        [tree.insert("", END, values = row) for row in cur.fetchall()]
    if selection == "" and selection2 != "":
        cur.execute("""DELETE FROM Material WHERE Material =:selection2""", {"selection2": selection2})
        combobox6.set("")
        cur.execute("SELECT Material FROM Material")
        res = cur.fetchall()
        combobox2['values'] = res
        combobox4['values'] = res
        combobox6['values'] = res
        cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
                Machine.MachineID = MachineMaterial.MachineID)
                JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID);""")
        [tree.delete(i) for i in tree.get_children()]
        [tree.insert("", END, values = row) for row in cur.fetchall()]
    if selection != "" and selection2 != "":
        cur.execute("""DELETE FROM Machine WHERE Machine =:selection""", {"selection": selection})
        combobox5.set("")
        cur.execute("SELECT Machine FROM Machine")
        res = cur.fetchall()
        combobox['values'] = res
        combobox3['values'] = res
        combobox5['values'] = res
        cur.execute("""DELETE FROM Material WHERE Material =:selection2""", {"selection2": selection2})
        combobox6.set("")
        cur.execute("SELECT Material FROM Material")
        res = cur.fetchall()
        combobox2['values'] = res
        combobox4['values'] = res
        combobox6['values'] = res
        cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
                Machine.MachineID = MachineMaterial.MachineID)
                JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID);""")
        [tree.delete(i) for i in tree.get_children()]
        [tree.insert("", END, values = row) for row in cur.fetchall()]

def search():
    selection = entry3.get()
    if selection == "":
        cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
                Machine.MachineID = MachineMaterial.MachineID)
                JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID);""")        
        [tree.delete(i) for i in tree.get_children()]
        [tree.insert("", END, values = row) for row in cur.fetchall()]
    else:
        cur.execute("""SELECT Machine, Material FROM ((Machine JOIN MachineMaterial ON 
                Machine.MachineID = MachineMaterial.MachineID)
                JOIN Material ON Material.MaterialID = MachineMaterial.MaterialID)
                WHERE Machine LIKE """ + "'%" + selection + "%'" + """ OR
                Material LIKE """ + "'%" + selection + "%'" + """;""")
        [tree.delete(i) for i in tree.get_children()]
        [tree.insert("", END, values = row) for row in cur.fetchall()]
        
root = Tk()
root.title("Интерфейс БД")
root.geometry("600x500")

tab_control = ttk.Notebook(root)  
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Ввод данных')  
tab_control.add(tab2, text='Просмотр данных')
tab_control.add(tab3, text='Удаление данных')

label = ttk.Label(tab1, text = "Таблица Станки")
label.pack(anchor=N, padx=6, pady=6)
label = ttk.Label(tab1, text = "Название Станка")
label.place(x = 135, y = 40)

entry = ttk.Entry(tab1)
entry.pack(anchor = N, padx = 8, pady = 9)

btn = ttk.Button(tab1, text = "Добавить", command = Add_Machine)
btn.pack(anchor = N, padx = 6, pady = 6)

label = ttk.Label(tab1, text = "Таблица Материалы")
label.pack(anchor = N, padx = 6, pady = 6)
label = ttk.Label(tab1, text = "Название Материала")
label.place(x = 110, y = 145)

entry2 = ttk.Entry(tab1)
entry2.pack(anchor = N, padx = 8, pady = 9)

btn = ttk.Button(tab1, text = "Добавить", command = Add_Matertial)
btn.pack(anchor = N, padx = 6, pady = 6)

label = ttk.Label(tab1, text = "Главная таблица")
label.pack(anchor = N, padx = 6, pady = 6)
label = ttk.Label(tab1, text = "Станок")
label.place(x = 180, y = 250)
label = ttk.Label(tab1, text = "Материал")
label.place(x = 165, y = 285)

combobox = ttk.Combobox(tab1, values = data_box()[0])
combobox.pack(anchor = N, padx = 6, pady = 6)
combobox2 = ttk.Combobox(tab1, values = data_box()[1])
combobox2.pack(anchor = N, padx = 6, pady = 6)

btn_di = ttk.Button(tab1, text = "Добавить", command = Add_MachineMatertial)
btn_di.pack(anchor = N, padx = 6, pady = 6)

columns = ("Станок", "Материал")
tree = ttk.Treeview(tab2, columns = columns, show = "headings")
tree.pack(fill = BOTH, expand = 1)
tree.heading("Станок", text = "Станок")
tree.heading("Материал", text = "Материал")

combobox3 = ttk.Combobox(tab2, values = data_box()[0])
combobox3.pack(anchor = N, padx = 6, pady = 6)
combobox4 = ttk.Combobox(tab2, values = data_box()[1])
combobox4.pack(anchor = N, padx = 6, pady = 6)

btn = ttk.Button(tab2, text = "Применить фильтр", command = sort)
btn.pack(anchor = N, padx = 6, pady = 6)
btn = ttk.Button(tab2, text = "Снять фильтр", command = sort_off)
btn.pack(anchor = N, padx = 6, pady = 6)

tab_control.pack(expand = 1, fill = 'both')

label = ttk.Label(tab3, text = "Материал")
label.pack(anchor = N, padx = 6, pady = 6)

combobox6 = ttk.Combobox(tab3, values = data_box()[1])
combobox6.pack(anchor = S, padx = 6, pady = 6)

btn = ttk.Button(tab3, text = "Удалить", command = delete_data)
btn.pack(anchor = N, padx = 6, pady = 6)

label = ttk.Label(tab3, text = "Станок")
label.pack(anchor = N, padx = 6, pady = 6)

combobox5 = ttk.Combobox(tab3, values = data_box()[0])
combobox5.pack(anchor = N, padx = 6, pady = 6)

btn = ttk.Button(tab3, text = "Удалить", command = delete_data)
btn.pack(anchor = S, padx = 6, pady = 6)

entry3 = ttk.Entry(tab2)
entry3.place(x = 50, y = 340)

btn = ttk.Button(tab2, text = "Поиск", command = search)
btn.place(x = 75, y = 370)

Datadd()

root.mainloop()
