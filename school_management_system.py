import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
from tkinter import Tk, PhotoImage

headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)


# Connecting to the Database ----------------------------------
connector = sqlite3.connect('SchoolManagement.db')
cursor = connector.cursor()
connector.execute(
"CREATE TABLE IF NOT EXISTS SCHOOL_MANAGEMENT (STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NO TEXT, GENDER TEXT, DOB TEXT, STREAM TEXT)"
)
#functions------------------------------------------
def reset_fields():
   global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
   for i in ['name_strvar', 'email_strvar', 'contact_strvar', 'gender_strvar', 'stream_strvar']:
       exec(f"{i}.set('')")
   dob.set_date(datetime.datetime.now().date())
def reset_form():
   global tree
   tree.delete(*tree.get_children())
   reset_fields()
def display_records():
   tree.delete(*tree.get_children())
   curr = connector.execute('SELECT * FROM SCHOOL_MANAGEMENT')
   data = curr.fetchall()
   for records in data:
       tree.insert('', END, values=records)
def add_record():
   global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
   name = name_strvar.get()
   email = email_strvar.get()
   contact = contact_strvar.get()
   gender = gender_strvar.get()
   DOB = dob.get_date()
   stream = stream_strvar.get()
   if not name or not email or not contact or not gender or not DOB or not stream:
       mb.showerror('Error!', "Please fill all the missing fields!!")
   else:
       try:
           connector.execute(
           'INSERT INTO SCHOOL_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES (?,?,?,?,?,?)', (name, email, contact, gender, DOB, stream)
           )
           connector.commit()
           mb.showinfo('Record added', f"Record of {name} was successfully added!")
           reset_fields()
           display_records()
       except:
           mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')
def remove_record():
   if not tree.selection():
       mb.showerror('Error!', 'Please select an item from the database')
   else:
       current_item = tree.focus()
       values = tree.item(current_item)
       selection = values["values"]
       tree.delete(current_item)
       connector.execute('DELETE FROM SCHOOL_MANAGEMENT WHERE STUDENT_ID=%d' % selection[0])
       connector.commit()
       mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')
       display_records()
def view_record():
   global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar
   if not tree.selection():

       mb.showerror('Error!', 'Please select a record to view')
   else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]

        name_strvar.set(selection[1]); email_strvar.set(selection[2])
        contact_strvar.set(selection[3]); gender_strvar.set(selection[4])
        date = datetime.date(int(selection[5][:4]), int(selection[5][5:7]), int(selection[5][8:]))
        dob.set_date(date);stream_strvar.set(selection[6])



main = Tk()
main.title('School Management System')
main.geometry('1000x600')
main.resizable(0, 0)
# main.wm_iconbitmap(default="student.ico")
# icon = PhotoImage(file='student.ico')
# main.iconphoto(True, icon)
# ----------------------------
lf_bg = "SteelBlue"
# -----------------
# variables------------------------------------------------
name_strvar = StringVar()
email_strvar = StringVar()
contact_strvar = StringVar()
gender_strvar = StringVar()
stream_strvar = StringVar()
# main heading------------------------------------------------
Label(main, text="SCHOOL MANAGEMENT SYSTEM", font=headlabelfont, bg='SkyBlue').pack(side=TOP, fill=X)
left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0,y=30,height=1000,width=500)

right_frame = Frame(main, bg="Gray35")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)
# left frame------------------------------------------------------
Label(left_frame,text="Name",bg=lf_bg,font="Arial 11").place(x=30,y=55)
Label(left_frame,text="Contact Number",bg=lf_bg,font="Arial 11").place(x=30,y=105)
Label(left_frame,text="Email Address",bg=lf_bg,font="Arial 11").place(x=30,y=155)
Label(left_frame,text="Gender",bg=lf_bg,font="Arial 11").place(x=30,y=205)
Label(left_frame,text="Date Of Birth",bg=lf_bg,font="Arial 11").place(x=30,y=255)
Label(left_frame,text="Stream",bg=lf_bg,font="Arial 11").place(x=30,y=305)


# entry-----------------------------------------------------------------------
Entry(left_frame,textvariable=name_strvar,width=23,font="Arial 10").place(x=200,y=55)
Entry(left_frame,textvariable=contact_strvar,width=23,font="Arial 10").place(x=200,y=105)
Entry(left_frame,textvariable=email_strvar,width=23,font="Arial 10").place(x=200,y=155)
OptionMenu(left_frame,gender_strvar,"Male","Female").place(x=200,y=205,width=85)
dob=DateEntry(left_frame,width=15,font="Arial 10" )
dob.place(x=200, y=255)
Entry(left_frame,textvariable=stream_strvar,width=23,font="Arial 10").place(x=200,y=305)
# buttons----------------------------------------------------------------
Button(left_frame, text="Add Record", pady=5, padx=5, font="Arial 11", width=15,command=add_record).place(x=130, y=360)
Button(left_frame, text="Reset Fields", pady=5, padx=5, font="Arial 11", width=13,command=reset_fields).place(x=60, y=415)
Button(left_frame, text="Delete Record", pady=5, padx=5, font="Arial 11", width=13,command=remove_record).place(x=208, y=415)
Button(left_frame, text="View Record", pady=5, padx=5, font="Arial 11", width=13,command=view_record).place(x=60, y=468)
Button(left_frame, text="Delete Database", pady=5, padx=5, font="Arial 11", width=13,command=reset_form).place(x=208, y=468)


#  right frame----------------------------------------------------------------------------------------
Label(right_frame, text='Students Records', font=headlabelfont, bg='navy', fg='LightCyan').pack(side=TOP, fill=X)
tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                   columns=('Student ID', "Name", "Email Address", "Contact Number", "Gender", "Date of Birth", "Stream"))
X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)
tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
tree.heading('Student ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Email Address', text='Email ID', anchor=CENTER)
tree.heading('Contact Number', text='Phone No', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Date of Birth', text='DOB', anchor=CENTER)
tree.heading('Stream', text='Stream', anchor=CENTER)
tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=150, stretch=NO)
tree.column('#3', width=170, stretch=NO)
tree.column('#4', width=90, stretch=NO)
tree.column('#5', width=90, stretch=NO)
tree.column('#6', width=90, stretch=NO)
tree.column('#7', width=150, stretch=NO)
tree.place(y=30, relwidth=1, relheight=0.9, relx=0)
display_records()








main.update()
main.mainloop()