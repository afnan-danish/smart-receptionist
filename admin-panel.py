from tkinter import *
from tkinter.ttk import *
from tkcalendar import Calendar, DateEntry
import datetime
from datetime import date
import sqlite3
conn = sqlite3.connect('smart_receptionist.db')
db = conn.cursor()

root = Tk()
#root.attributes("-fullscreen", True)
root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
root.state('zoomed')

root.title("Smart Receptionist Admin Panel")
root.configure(background="Powder Blue")

today = date.today()
#print("Today's date:", today)

w = Label(root, text="Appointment Details", background="Powder Blue", anchor="center", font=("Helvetica", 23),width = 50)
w.grid(row=0, column=0,pady=5)


def create_window(sdate):
    window = Toplevel(root)
    window.geometry('1200x400')
    window.focus_force()
    newtab = App(window)
    newtab.LoadTable(sdate)
    def close(event):
        window.withdraw()
    window.bind("<Escape>", close)


def print_sel(self):
    #print(cal.get_date())
    #today = cal.get_date()
    create_window(cal.get_date())

Label(root, text="Select Date",background="Powder Blue", font='Helvetica 12 bold').grid(row = 1, column = 0,sticky=W)
cal = DateEntry(root, width=12, background='darkblue',
                    foreground='white', borderwidth=2, locale='en_US', date_pattern='dd/MM/yyyy')
cal.grid(row=1, column=0,sticky=W, padx=100, pady=5)
cal.bind("<<DateEntrySelected>>", print_sel)



cdate = ''

class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.CreateUI()
        #self.LoadTable()
        self.grid(sticky = (N,S,W,E))
        parent.grid_rowconfigure(2, weight = 1)
        parent.grid_columnconfigure(0, weight = 1)
        #self.update()

    def CreateUI(self):
        tv = Treeview(self)
        tv['columns'] = ('starttime', 'endtime', 'status', 'date')
        tv.heading("#0", text='Sr No', anchor='center')
        tv.column("#0", anchor="w", width=10)
        tv.heading('starttime', text='Name')
        tv.column('starttime', anchor='w', width=400)
        tv.heading('endtime', text='Age')
        tv.column('endtime', anchor='w', width=100)
        tv.heading('status', text='Gender')
        tv.column('status', anchor='w', width=100)
        tv.heading('date', text='Date')
        tv.column('date', anchor='w', width=100)
        tv.grid(sticky = (N,S,W,E))
        tv.tag_configure('monospace', font='Helvetica 10')
        self.treeview = tv
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

    def LoadTable(self, cdate):
        today = cdate
        #print("get date"+str(today))
        cursor = conn.execute("SELECT * from apt_dtl WHERE DATE='"+str(today)+"' Order By id ASC ")
        srno = 1
        for row in cursor:
            self.treeview.insert('', 'end', text=""+str(srno), values=(''+row[1],
                             ''+str(row[2]), ''+str(row[3]), ''+str(row[4])), tag='monospace')
            srno += 1
            #print(str(row[4]))

apk = App(root)
apk.LoadTable(date.today())
 


root.mainloop()