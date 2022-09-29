# -*- coding: utf-8 -*-
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
from datetime import datetime
from tkinter import messagebox
import ctypes


u = ctypes.windll.LoadLibrary("user32.dll")
pf = getattr(u, "GetKeyboardLayout")

if hex(pf(0)) == '0x43f043f':
    current_datetime = datetime.now()
    year_now = current_datetime.year-4 

    def DisplayForm():
        display_screen = Tk()
        display_screen.geometry("1350x540")
        display_screen.title("Список сотрудников")
        display_screen.tk.call('wm', 'iconphoto', display_screen._w, tk.PhotoImage(file='cnpc.png'))
        display_screen.resizable(0, 0)
        global tree

        TopViewForm = Frame(display_screen, width=800, bd=1, relief=SOLID)
        TopViewForm.pack(side=TOP, fill=X)
        LeftViewForm = Frame(display_screen, width=800)
        LeftViewForm.pack(side=LEFT, fill=Y)
        MidViewForm = Frame(display_screen, width=800)
        MidViewForm.pack(side=RIGHT)
        lbl_text = Label(TopViewForm, text="Список сотрудников на обучение", font=('arial', 20), width=800,bg="#1C2833",fg="white")
        lbl_text.pack(fill=X)
        lbl_txtsearch = Label(LeftViewForm, text="", font=('arial', 18))
        lbl_txtsearch.pack(side=TOP, anchor=W)

        scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
        scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
        tree = ttk.Treeview(MidViewForm,columns=("table nom", "full name", "rank", "post","VOLS","rigger","electro"),selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)

        tree.heading('table nom', text="Табельный номер", anchor=W)
        tree.heading('full name', text="Ф. И. О.", anchor=W)
        tree.heading('rank', text="Разряд", anchor=W)
        tree.heading('post', text="Занимаемая Должность", anchor=W)
        tree.heading('VOLS', text="Разряд, ВОЛС", anchor=W)
        tree.heading('rigger', text="Вышкомонтажник", anchor=W)
        tree.heading('electro', text="Эл. пож. охр. сигн.", anchor=W)

        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=120)
        tree.column('#2', stretch=NO, minwidth=0, width=150)
        tree.column('#3', stretch=NO, minwidth=0, width=50)
        tree.column('#4', stretch=NO, minwidth=0, width=180)
        tree.column('#5', stretch=NO, minwidth=0, width=120)
        tree.column('#5', stretch=NO, minwidth=0, width=120)
        tree.pack()
        DisplayData()


    def DisplayData():
        conn = sqlite3.connect('database.db')
        cursor=conn.execute("SELECT * FROM players ORDER BY tabel_nom")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()


    def click_button0():
        conn = sqlite3.connect('database.db')
        cursor=conn.execute("SELECT * FROM players ORDER BY tabel_nom")
        fetch = cursor.fetchall()
        tree.delete(*tree.get_children())
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()


    def click_button1():
        conn = sqlite3.connect('database.db')
        cursor=conn.execute("SELECT * FROM players ORDER BY tabel_nom")
        fetch = cursor.fetchall()
        tree.delete(*tree.get_children())
        for data in fetch:
            if data[4] != '':
                if int(data[4]) <= year_now :
                    tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()


    def click_button2():
        conn = sqlite3.connect('database.db')
        cursor=conn.execute("SELECT * FROM players ORDER BY tabel_nom")
        fetch = cursor.fetchall()
        tree.delete(*tree.get_children())
        for data in fetch:
            if data[5] != '':
                if int(data[5]) <= year_now :
                    tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()


    def click_button3():
        conn = sqlite3.connect('database.db')
        cursor=conn.execute("SELECT * FROM players ORDER BY tabel_nom")
        fetch = cursor.fetchall()
        tree.delete(*tree.get_children())
        for data in fetch:
            if data[6] != '':
                if int(data[6]) <= year_now :
                    tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

    def window_update_vols():
        master = tk.Tk()
        master.geometry("380x80")
        master.title("Обновить ВОЛС ")
        master.resizable(0, 0)

        conn = sqlite3.connect('database.db')
        cursor=conn.execute("SELECT * FROM players")
        fetch = cursor.fetchall()
        mycursor = conn.cursor()

        def show_entry_vols():
            info = mycursor.execute('SELECT * FROM players WHERE tabel_nom=?', (e1.get(), ))
            if info.fetchone() is None: 
                master.destroy()
                messagebox.showerror("Ошибка", "Мы не можем найти данного сотрудника ! ")
            else:
                if int(e2.get()) <= current_datetime.year:
                    user = (e2.get(), e1.get())
                    sql_update_query = """Update players set VOLS = ? where tabel_nom = ?"""
                    mycursor.execute(sql_update_query, user)
                    conn.commit()

                    DisplayData()
                    e1.delete(0, 'end')
                    e2.delete(0, 'end')
                    master.destroy()
                    click_button0()
                    messagebox.showinfo("Уведомление", "Данные сотрудника обновлены")
                else:
                    master.destroy()
                    messagebox.showerror("Ошибка", "Вы ввели неверную дату ! ")

        tk.Label(master, text=" Табельный номер : ").grid(row=0)
        tk.Label(master, text=" Последнее обучение ВОЛС : ").grid(row=1)

        e1 = tk.Entry(master, width=30)
        e2 = tk.Entry(master, width=30)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)

        tk.Button(master, text='Обновить', command=show_entry_vols).grid(row=3, column=1, sticky=tk.W, pady=4)
        tk.mainloop()
        cursor.close()
        conn.close()

    def window_update_rigger():
        master = tk.Tk()
        master.geometry("400x80")
        master.title("Обновить Вышкомонтажник ")
        master.resizable(0, 0)

        conn = sqlite3.connect('database.db')
        cursor=conn.execute("SELECT * FROM players")
        fetch = cursor.fetchall()
        mycursor = conn.cursor()

        def show_entry_rigger():
            info = mycursor.execute('SELECT * FROM players WHERE tabel_nom=?', (e1.get(), ))
            if info.fetchone() is None: 
                master.destroy()
                messagebox.showerror("Ошибка", "Мы не можем найти данного сотрудника ! ")
            else:
                if int(e2.get()) <= current_datetime.year:
                    user = (e2.get(), e1.get())
                    sql_update_query = """Update players set rigger = ? where tabel_nom = ?"""
                    mycursor.execute(sql_update_query, user)
                    conn.commit()

                    e1.delete(0, 'end')
                    e2.delete(0, 'end')
                    master.destroy()
                    click_button0()
                    messagebox.showinfo("Уведомление", "Данные сотрудника обновлены")
                else:
                    master.destroy()
                    messagebox.showerror("Ошибка", "Вы ввели неверную дату ! ")

        tk.Label(master, text=" Табельный номер : ").grid(row=0)
        tk.Label(master, text=" Последнее обучение Вышкомонтажник : ").grid(row=1)

        e1 = tk.Entry(master, width=25)
        e2 = tk.Entry(master, width=25)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)

        tk.Button(master, text='Обновить', command=show_entry_rigger).grid(row=3, column=1, sticky=tk.W, pady=4)
        tk.mainloop()
        cursor.close()
        conn.close()


    def window_update_electro():
        master = tk.Tk()
        master.geometry("400x80")
        master.title("Обновить Эл. пож. охр. сигн ")
        master.resizable(0, 0)

        conn = sqlite3.connect('database.db')
        cursor=conn.execute("SELECT * FROM players")
        fetch = cursor.fetchall()
        mycursor = conn.cursor()

        def show_entry_electro():

            info = mycursor.execute('SELECT * FROM players WHERE tabel_nom=?', (e1.get(), ))
            if info.fetchone() is None: 
                master.destroy()
                messagebox.showerror("Ошибка", "Мы не можем найти данного сотрудника ! ")
            else:
                if int(e2.get()) <= current_datetime.year:
                    user = (e2.get(), e1.get())
                    sql_update_query = """Update players set electro = ? where tabel_nom = ?"""
                    mycursor.execute(sql_update_query, user)
                    conn.commit()
                    e1.delete(0, 'end')
                    e2.delete(0, 'end')
                    master.destroy()
                    click_button0()
                    messagebox.showinfo("Уведомление", "Данные сотрудника обновлены")
                else:
                    master.destroy()
                    messagebox.showerror("Ошибка", "Вы ввели неверную дату ! ")

        tk.Label(master, text=" Табельный номер : ").grid(row=0)
        tk.Label(master, text=" Последнее обучение Эл. пож. охр. сигн : ").grid(row=1)

        e1 = tk.Entry(master, width=25)
        e2 = tk.Entry(master, width=25)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)

        tk.Button(master, text='Обновить', command=show_entry_electro).grid(row=3, column=1, sticky=tk.W, pady=4)
        tk.mainloop()
        cursor.close()
        conn.close()

    def window_delete_player():
        conn = sqlite3.connect('database.db')
        cursor=conn.execute("SELECT * FROM players")
        fetch = cursor.fetchall()
        mycursor = conn.cursor()

        master = tk.Tk()
        master.geometry("300x80")
        master.title(" Удалить сотрудника")
        master.resizable(0, 0)


        def show_delete():

            info = mycursor.execute('SELECT * FROM players WHERE tabel_nom=?', (r1.get(), ))
            if info.fetchone() is None: 
                master.destroy()
                messagebox.showerror("Ошибка", "Мы не можем найти данного сотрудника ! ")
            else:
                user = (r1.get())
                sql_update_query = """DELETE from players where tabel_nom = ?"""
                mycursor.execute(sql_update_query, (user, ))
                conn.commit()
                r1.delete(0, 'end')
                master.destroy()
                click_button0()
                messagebox.showinfo("Уведомление", "Вы удалили данные сотрудника")
        tk.Label(master, text=" Табельный номер : ").grid(row=0)

        r1 = tk.Entry(master, width=25)

        r1.grid(row=0, column=1)

        tk.Button(master, text='Удалить', command=show_delete).grid(row=1, column=1, sticky=tk.W, pady=4)
        tk.mainloop()
        cursor.close()
        conn.close()

    def window_add_player():
        conn = sqlite3.connect('database.db')
        cursor=conn.execute("SELECT * FROM players")
        fetch = cursor.fetchall()
        mycursor = conn.cursor()

        master = tk.Tk()
        master.geometry("380x200")
        master.title("Добавить сотрудника")
        master.resizable(0, 0)

        def show_entry_fields():

            info = mycursor.execute('SELECT * FROM players WHERE tabel_nom=?', (e1.get(), ))
            if info.fetchone() is None: 
                user = (e1.get(), e2.get(),e3.get(),e4.get(),e5.get(),e6.get(),e7.get())
                mycursor.execute("INSERT INTO players VALUES(?, ?, ?, ?, ?, ?, ?);", user)
                conn.commit()
                e1.delete(0, 'end')
                e2.delete(0, 'end')
                e3.delete(0, 'end')
                e4.delete(0, 'end')
                e5.delete(0, 'end')
                e6.delete(0, 'end')
                e7.delete(0, 'end')
                master.destroy()
                click_button0()
                messagebox.showinfo("Уведомление", "Сотрудник добавлен")
            else:
                master.destroy()
                messagebox.showerror("Ошибка", "Такой сотрудник уже имеется ! ")

            
        tk.Label(master, text=" Табельный номер : ").grid(row=0)
        tk.Label(master, text=" Ф. И. О. : ").grid(row=1)
        tk.Label(master, text=" Разряд : ").grid(row=2)
        tk.Label(master, text=" Занимаемая должность : ").grid(row=3)
        tk.Label(master, text=" Разряд, ВОЛС : ").grid(row=4)
        tk.Label(master, text=" Вышкомонтажник : ").grid(row=5)
        tk.Label(master, text=" Эл. пож. охр. сигн : ").grid(row=6)

        e1 = tk.Entry(master, width=35)
        e2 = tk.Entry(master, width=35)
        e3 = tk.Entry(master, width=35)
        e4 = tk.Entry(master, width=35)
        e5 = tk.Entry(master, width=35)
        e6 = tk.Entry(master, width=35)
        e7 = tk.Entry(master, width=35)
        

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        e3.grid(row=2, column=1)
        e4.grid(row=3, column=1)
        e5.grid(row=4, column=1)
        e6.grid(row=5, column=1)
        e7.grid(row=6, column=1)

        tk.Button(master, text='Добавить', command=show_entry_fields).grid(row=7, column=1, sticky=tk.W, pady=4)
        tk.mainloop()
        cursor.close()
        conn.close()
        
    DisplayForm()

    btn0 = Button(text="Общий список", background="#0794ce", foreground="#ccc",padx="20", pady="8", font="16",width="25", fg="white", command=click_button0)    
    btn1 = Button(text="Разряд, ВОЛС", background="#0794ce", foreground="#ccc",padx="20", pady="8", font="16", width="25", fg="white", command=click_button1)
    btn2 = Button(text="Вышкомонтажник", background="#0794ce", foreground="#ccc",padx="20", pady="8", font="16", width="25", fg="white", command=click_button2)
    btn3 = Button(text="Эл.пож.охр.сигн.", background="#0794ce", foreground="#ccc",padx="20", pady="8", font="16", width="25", fg="white", command=click_button3)
    btn4 = Button(text="Обновить ВОЛС", background="#0794ce", foreground="#ccc",padx="20", pady="8", font="16", width="25", fg="white", command=window_update_vols)
    btn5 = Button(text="Обновить Вышкомонтажник", background="#0794ce", foreground="#ccc",padx="20", pady="8", font="16", width="25", fg="white", command=window_update_rigger)
    btn6 = Button(text="Обновить Эл. пож. охр. сигн", background="#0794ce", foreground="#ccc",padx="20", pady="8", font="16", width="25", fg="white", command=window_update_electro)
    btn7 = Button(text="Добавить сотрудника", background="#0794ce", foreground="#ccc",padx="20", pady="8", font="16", width="25", fg="white", command=window_add_player)
    btn8 = Button(text="Удалить сотрудника", background="#0794ce", foreground="#ccc",padx="20", pady="8", font="16", width="25", fg="white", command=window_delete_player)

    btn0.pack()
    btn1.pack()
    btn2.pack()
    btn3.pack()
    btn4.pack()
    btn5.pack()
    btn6.pack()
    btn7.pack()
    btn8.pack()

    mainloop()
else:
    messagebox.showerror("Ошибка", " Пожалуйста поменяйте раскладку на казахский   ! ")