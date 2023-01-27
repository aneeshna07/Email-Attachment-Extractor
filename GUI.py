# Make a regular expression
# for validating an Email

import webbrowser
import re
import sys
import os
from tkinter import *
import tkinter as tk
import tkinter.filedialog
from pathlib import Path
from tkinter.ttk import *
import attachment_extractor
from tkcalendar import DateEntry, Calendar
from datetime import date
import pandas as pd
import csv
import threading
import logging
import time


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Add tkdesigner to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
try:
    from tkdesigner.designer import Designer
except ModuleNotFoundError:
    raise RuntimeError("Couldn't add tkdesigner to the PATH.")


# Path to asset files for this GUI window.
ASSETS_PATH = Path(__file__).resolve().parent / "assets"

# Required in filter_page to add data files to Windows executable
path = getattr(sys, '_MEIPASS', os.getcwd())
os.chdir(path)

output_path = ""
users = 0
filters = {'UNSEEN':0}
usernames = []
emails = set()

def btn_clicked():
    email = email_entry.get()
    password = password_entry.get()
    # output_path = path_entry.get()
    # output_path = output_path.strip()
    # filter_page.pack(fill='both', expand=1)
    # login_detail_page.pack_forget()
    # return
    
    if not (re.fullmatch(regex, email)):
        tk.messagebox.showerror(
            title="Invalid Credentials!", message="Please enter Valid mail ID.")
        return
    if not password:
        tk.messagebox.showerror(
            title="Empty Fields!", message="Please enter password.")
        return

    msg = attachment_extractor.add_user(email, password, imap_entry.get())
    # print(attachment_extractor.mail_password)
    
    if not msg == 'Successfully Logged in!' or msg == 'Already Logged in':
        tk.messagebox.showerror(message=msg)
        return
    tk.messagebox.showinfo(message=msg)
    # if not output_path:
    #     tk.messagebox.showerror(
    #         title="Invalid Path!", message="Enter a valid output path.")
    #     return
    change_to_login_detail_page()
    filter_page.pack(fill='both', expand=1)
    login_detail_page.pack_forget()
    

def select_path():
    global output_path
    output_path = tk.filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, output_path)


def know_more_clicked(event):
    instructions = (
        "https://github.com/ParthJadhav/Tkinter-Designer/"
        "blob/master/docs/instructions.md")
    webbrowser.open_new_tab(instructions)


def make_label(master, x, y, h, w, *args, **kwargs):
    f = tk.Frame(master, height=h, width=w)
    f.pack_propagate(0)  # don't shrink
    f.place(x=x, y=y)

    label = tk.Label(f, *args, **kwargs)
    label.pack(fill=tk.BOTH, expand=1)

    return label


window = tk.Tk()
logo = tk.PhotoImage(file=ASSETS_PATH / "iconbitmap.gif")
window.call('wm', 'iconphoto', window._w, logo)
window.title("Email Attachment Extractor")

window.geometry("862x519")
window.maxsize(window.winfo_screenwidth(), window.winfo_screenheight())
window.configure(bg="#3A7FF6")
canvas = tk.Canvas(
    window, bg="#333333", height=window.winfo_screenheight(), width=window.winfo_screenwidth(),
    bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(400, 0, window.winfo_screenwidth(
), window.winfo_screenheight(), fill="#008080", outline="")


text_box_bg = tk.PhotoImage(file=ASSETS_PATH / "TextBox_Bg.png")
select_bg = tk.PhotoImage(file=ASSETS_PATH / "select.png")
email_entry_img = canvas.create_image(650.5, 167.5, image=text_box_bg)
password_entry_img = canvas.create_image(650.5, 248.5, image=text_box_bg)
imap_entry_img = canvas.create_image(650.5, 333.5, image=text_box_bg)

user_icon_img = tk.PhotoImage(file=ASSETS_PATH / "user.png")
user = canvas.create_image(785, 167.5, image=user_icon_img)

pwd_img = PhotoImage(file=ASSETS_PATH / "pwd.png")
pwd = canvas.create_image(785, 247.5, image=pwd_img)

email_entry = tk.Entry(bd=0, bg="white", fg="#000716",  highlightthickness=0)
email_entry.place(x=490.0, y=137+25, width=250.0, height=35)
email_entry.focus()

password_entry = tk.Entry(bd=0, show="*", bg="white",
                          fg="#000716",  highlightthickness=0)
password_entry.place(x=490.0, y=218+25, width=250.0, height=35)

imap_entry = tk.Entry(bd=0, bg='white', fg="#000716", highlightthickness=0)
imap_entry.insert(0, "imap.gmail.com")
imap_entry.place(x=490.0, y=308+22, width=313.0, height=35)

canvas.create_text(
    490.0, 156.0, text="Email ID", fill="#515486",
    font=("Arial-BoldMT", int(13.0)), anchor="w")

canvas.create_text(
    490.0, 234.5, text="Password", fill="#515486",
    font=("Arial-BoldMT", int(13.0)), anchor="w")

canvas.create_text(
    490.0, 321.0, text="imap server", fill="#515486",
    font=("Arial-BoldMT", int(13.0)), anchor="w")


canvas.create_text(
    646.5, 428.5, text="Generate",
    fill="#FFFFFF", font=("Arial-BoldMT", int(13.0)))
canvas.create_text(
    585.5, 88.0, text="Enter the details.",
    fill="black", font=("Arial-BoldMT", int(22.0)))

title = tk.Label(
    text="Email Attachment Extractor", bg="#333333",
    fg="white", font=("Arial-BoldMT", int(20.0)))
title.place(x=27.0, y=120.0)

info_text = tk.Label(
    text="Email Attachment extractor.\n\n"
    "using Tkinter Designer.",
    bg="#333333", fg="white", justify="left",
    font=("Georgia", int(16.0)))

info_text.place(x=27.0, y=200.0)

know_more = tk.Label(
    text="Click here for instructions",
    bg="#008080", fg="black", cursor="hand2")
know_more.place(x=27, y=400)
# know_more.bind('<Button-1>', know_more_clicked)

btn_img = tk.PhotoImage(file=ASSETS_PATH / "login1.png")

login_btn = tk.Button(
   image=btn_img, bg="#333333",fg="white", borderwidth=0, highlightthickness=0,
    command=btn_clicked, relief="groove")
login_btn.place(x=577, y=401)


# Create a new frame in the window

filter_page = Frame(window)
path_page = Frame(window)
login_detail_page = Frame(window)
downloads_view_page = Frame(window)
# Define a function for switching the frames

def change_to_downloads_page():
    downloads_view_page.pack(fill='both', expand=1)
    path_page.pack_forget()
    login_detail_page.pack_forget()
    filter_page.pack_forget()

def change_to_login_page():
    filter_page.pack_forget()


def remove_user(key):
    print(key)
    print(attachment_extractor.remove_user(key))
    global users
    for widgets in filter_page.winfo_children():
        if(type(widgets)==tkinter.ttk.Checkbutton and widgets['text'] not in ['PDF',"docx","jpg","other","All"] ):
            widgets.destroy()
    if users == 1:
        users -= 1
        
        login_detail_page.pack_forget()
    else:
        users -= 1
        login_detail_page.pack_forget()
        
        # filter_page.pack(fill="both",expand=1)
        for widgets in login_detail_page.winfo_children():
            widgets.destroy()
        change_to_login_detail_page()
    return

def change_to_login_detail_page():
    canvas3 = tk.Canvas(
    login_detail_page, bg="#333333", height=window.winfo_screenheight(), width=window.winfo_screenwidth(),
    bd=0, highlightthickness=0, relief="ridge")
    canvas3.place(x=0, y=0)
    canvas3.create_rectangle(300, 0, 300 + window.winfo_screenwidth(),
                             window.winfo_screenheight(), fill="#008080", outline="")

    path_back_btn = tk.Button(login_detail_page,
                              text='Back', bg="#333333", 
                              fg="white",font = ("Times New Roman",13),
                              borderwidth=0, highlightthickness=0,
                              command=change_to_filter_page, relief="groove")
    path_back_btn.place(x=500, y=401, width=70, height=30)

    add = tk.Button(login_detail_page,
                       text = "Add mail ID", bg="#333333", fg="white",
                       font = ("Times New Roman",13), command = add_mail )
    add.place(x = 500 + 150, y = 401, width = 100, height = 30)
    keys = attachment_extractor.display_users()
    # print(keys)
    login_detail_page.pack_forget()
    login_detail_page.pack(fill='both', expand=1)
    filter_page.pack_forget()
    path_page.pack_forget()
    j = 200
    k=90
    global users 
    users=0  
    btn_dict = {} 
    # Checkbutton1 = IntVar()
    global usernames
    checknutton1 = IntVar()
    checknutton2 = IntVar()
    checknutton3 = IntVar()
    checknutton4 = IntVar()
    checknutton5 = IntVar()

    usernames = [IntVar(),IntVar(),IntVar(),IntVar(),IntVar()]
    for i,key in enumerate(keys):
        def delete_user(x=key):
            return remove_user(x)
        lab = tk.Label(login_detail_page,
                       text=key, bg="#008080", fg="#000716",
                       font=("Times New Roman", 13)
                       )
        lab.place(x=500, y=j)
        Button1 = tk.Checkbutton(filter_page, text=key,
                      bg= "#008080",
                      variable=usernames[i],
                      onvalue=1,
                      offvalue=0,
                      )
        
        Button1.place(x=670, y=k)
        # filter_lab = tk.Label(filter_page,
        #                text=key, bg="#008080", fg="#000716",
        #                font=("Times New Roman", 13)
        #                )
        # filter_lab.place(x=20, y=j+50)
        btn_dict[key] = tk.Button(login_detail_page,
                        text="logout", bg="#333333",fg="white",borderwidth=0, highlightthickness=0,
                        font = ("Times New Roman",13),command = delete_user)
        btn_dict[key].place(x=500+200, y=j)
        users += 1
        j += 50
        k+=30


def change_to_filter_page():
    filter_page.pack(fill='both', expand=1)
    path_page.pack_forget()
    login_detail_page.pack_forget()


def change_to_path_page():
    path_page.pack(fill='both', expand=1)
    filter_page.pack_forget()
    downloads_view_page.pack_forget()
    login_detail_page.pack_forget()


def add_mail():
    def btn_clicked_2():
        email = email_entry_2.get()
        password = password_entry_2.get()
        # output_path = path_entry.get()
        # output_path = output_path.strip()
        # filter_page.pack(fill='both', expand=1)
        # return
        if not (re.fullmatch(regex, email)):
            tk.messagebox.showerror(
                title="Invalid Credentials!", message="Please enter Valid mail ID.")
            return
        if not password:
            tk.messagebox.showerror(
                title="Empty Fields!", message="Please enter password.")
            return
        msg = attachment_extractor.add_user(email, password, imap_entry_2.get())
        if not msg == 'Successfully Logged in!' or msg == 'Already Logged in':
            tk.messagebox.showerror(message=msg)
            return
        tk.messagebox.showinfo(message=msg)
        # if not output_path:
        #     tk.messagebox.showerror(
        #         title="Invalid Path!", message="Enter a valid output path.")
        #     return
        change_to_login_detail_page()
        filter_page.pack(fill='both', expand=1)
        login_detail_page.pack_forget()
        new_root.destroy()
    new_root = tk.Toplevel(window,bg="black")
    logo_= tk.PhotoImage(file=ASSETS_PATH / "iconbitmap.gif")
    new_root.iconphoto(False, logo_)
    new_root.title("Email Attachment Extractor")
    new_root.geometry("210x250")
    email_entry_2 = tk.Entry(new_root,bd=0, bg="white", fg="#000716",  highlightthickness=0)
    email_entry_2.place(x=30, y=40, width=140, height=25)
    email_entry_2.focus()
    label_1 = tk.Label(new_root,
                  text="Enter Email ID : ", bg="black", fg="white",
                  font=("Times New Roman", 13)
                  )
    label_1.place(x=30, y=10)
    password_entry_2 = tk.Entry(new_root,bd=0, show="*", bg="white",
                              fg="#000716",  highlightthickness=0)
    password_entry_2.place(x=30, y=110, width=140, height=25)
    label2 = tk.Label(new_root,
                  text="Enter Password: ", bg="black", fg="white",
                  font=("Times New Roman", 13)
                  )
    label2.place(x=30, y=80)
    imap_entry_2 = tk.Entry(new_root,bd=0, bg="white",
                              fg="#000716",  highlightthickness=0)
    imap_entry_2.place(x=30, y=180, width=140, height=25)
    password_entry_2.place(x=30, y=110, width=140, height=25)
    label3 = tk.Label(new_root,
                  text="Enter Imap server: ", bg="black", fg="white",
                  font=("Times New Roman", 13)
                  )
    label3.place(x=30, y=150)
    login_btn_root = tk.Button(new_root,
    text='login', bg="#008080", borderwidth=0, highlightthickness=0,
    command=btn_clicked_2, relief="groove")
    login_btn_root.place(x=55, y=220, width=80, height=25)

    


# login detail page
canvas3 = tk.Canvas(
    login_detail_page, bg="#333333", height=window.winfo_screenheight(), width=window.winfo_screenwidth(),
    bd=0, highlightthickness=0, relief="ridge")
canvas3.place(x=0, y=0)
canvas3.create_rectangle(300, 0, 300 + window.winfo_screenwidth(),
                         window.winfo_screenheight(), fill="#008080", outline="")

path_back_btn = tk.Button(login_detail_page,
                          text='Back', bg="#3A7FF6", borderwidth=0, highlightthickness=0,
                          command=change_to_filter_page, relief="groove")
path_back_btn.place(x=500, y=401, width=70, height=30)

add = tk.Button(login_detail_page,
                   text = "Add mail ID", bg="#3A7FF6",borderwidth=0, highlightthickness=0,
                    command = add_mail )
add.place(x = 500 + 150, y = 401, width = 100, height = 30)


# filterpage
canvas1 = tk.Canvas(
    filter_page, bg="#333333", height=window.winfo_screenheight(), width=window.winfo_screenwidth(),
    bd=0, highlightthickness=0, relief="ridge")
canvas1.place(x=0, y=0)
canvas1.create_rectangle(300, 0, 300 + window.winfo_screenwidth(),
                         window.winfo_screenheight(), fill="#008080", outline="")
login_detail_btn = tk.Button(filter_page,
                             text='login/logout', bg="#008080", borderwidth=0, highlightthickness=0,
                             command=change_to_login_detail_page, relief="groove")
login_detail_btn.place(x=27, y=30, width=100, height=30)

title = tk.Label(filter_page,
                 text="Choose Filters", bg="#333333",
                 fg="white", font=("Arial-BoldMT", int(20.0)))
title.place(x=27.0, y=120.0)

info_text = tk.Label(filter_page,
                     text="\n\n"

                     "Select atleast one Reciever email ID \nbefore applying filters\n\n"
                     "Sender Email ID and Subject\nneed not be exact even a substring\nworks ",
                     bg="#333333", fg="white", justify="left",
                     font=("Times New Roman", 13))

info_text.place(x=27.0, y=200.0)

Checkbutton1 = StringVar()
Checkbutton2 = StringVar()
Checkbutton3 = StringVar()
Checkbutton4 = tk.StringVar()
Checkbutton5 = tk.StringVar()



label1 = tk.Label(filter_page,
                  text="Select the type of attachments : ", bg="#008080", fg="#000716",
                  font=("Times New Roman", 13)
                  )
label1.place(x=340, y=50)


label7 = tk.Label(filter_page,
                  text="Select Reciever email ID : ", bg="#008080", fg="#000716",
                  font=("Times New Roman", 13)
                  )
label7.place(x=650, y=50)


label2 = tk.Label(filter_page,
                  text="Select the Time Interval : ", bg="#008080", fg="#000716",
                  font=("Times New Roman", 13)
                  )
label2.place(x=340, y=240)


label3 = tk.Label(filter_page,
                  text="Start Date : ", bg="#008080", fg="#000716",
                  font=("Times New Roman", 10)
                  )
label3.place(x=360, y=260)

cal1_data = StringVar()
cal2_data = StringVar()

cal1 = DateEntry(filter_page, width=16, background="black",
                foreground="white", bd=2, textvariable = cal1_data)
cal1.place(x=360.0, y=280, width=100.0, height=20)

label4 = tk.Label(filter_page,
                  text="End Date : ", bg="#008080", fg="#000716",
                  font=("Times New Roman", 10)
                  )
label4.place(x=480, y=260)
today  = date.today()
cal2 = DateEntry(filter_page, width=16, background="black",maxdate = today,
                foreground="white", bd=2, textvariable = cal2_data)
cal2.place(x=480.0, y=280, width=100.0, height=20)

label5 = tk.Label(filter_page,
                  text="Sender Mail ID : ", bg="#008080", fg="#000716",
                  font=("Times New Roman", 13)
                  )
label5.place(x=360, y=320)
sender_email_entry = tk.Entry(
    filter_page, bd=0, bg="white", fg="#000716",  highlightthickness=0)
sender_email_entry.place(x=360, y=348, width=200, height=20)

label6 = tk.Label(filter_page,
                  text="Subject : ", bg="#008080", fg="#000716",
                  font=("Times New Roman", 13)
                  )
label6.place(x=360, y=378)
subject_entry = tk.Entry(
    filter_page, bd=0, bg="white", fg="#000716",  highlightthickness=0)
subject_entry.place(x=360, y=410, width=200, height=20)

Button1 = tk.Checkbutton(filter_page, text="PDF",
                      
                      variable=Checkbutton1,bg="#008080",
                      onvalue='pdf',
                      offvalue='',

                      )

Button2 = tk.Checkbutton(filter_page, text="docx",
                      variable=Checkbutton2,bg="#008080",
                      onvalue='docx',
                      offvalue=''
                      )

Button3 = tk.Checkbutton(filter_page, text="jpg",
                      variable=Checkbutton3,bg="#008080",
                      onvalue='jpg',
                      offvalue='')

type_entry = tk.Entry(filter_page, bd=0, bg="white",
                      fg="#000716", highlightthickness=0)

def other_():
    if(Checkbutton4.get()=='on'):
        type_entry.place(x=440, y=180, width=200, height=20)
        type_entry.focus()
    else:
        type_entry.place_forget()
    
def delete_other():
    type_entry.place_forget()
var = IntVar()
Button4 = tk.Checkbutton(filter_page, text="other",
                      variable=Checkbutton4,bg="#008080",
                      onvalue="on",command=other_,
                      offvalue="")

Button5 = tk.Checkbutton(filter_page, text="All",
                      variable=Checkbutton5,
                      onvalue='all',bg="#008080",
                      offvalue='')   

Checkbutton5.set('all')             
Button1.place(x=370, y=90)
Button2.place(x=370, y=120)
Button3.place(x=370, y=150)
Button4.place(x=370, y=180)
Button5.place(x=370, y=210)


# back_btn = tk.Button(filter_page,
#     text = 'Back', bg="#3A7FF6",borderwidth=0, highlightthickness=0,
#     command=change_to_login_page, relief="groove")
# back_btn.place(x=500, y=401, width=70, height=30)

# next_btn = tk.Button(filter_page,
#                      text='Next', bg="#333333",
#                      fg="white",
#                      borderwidth=0, highlightthickness=0,
#                      command=change_to_path_page, relief="groove")
# next_btn.place(x=550, y=401, width=70, height=30)


def apply_filter():
    filters['Type'] = []
    check_user = [usernames[0].get(),usernames[1].get(),usernames[2].get(),usernames[3].get(),usernames[4].get()]
    if 1 not in check_user:
        tk.messagebox.showerror(title="Select atleast one user!", message="Select atleast one user")
        return
    if Checkbutton1.get(): filters['Type'].append(Checkbutton1.get())
    if Checkbutton2.get(): filters['Type'].append(Checkbutton2.get())
    if Checkbutton3.get(): filters['Type'].append(Checkbutton3.get())
    if Checkbutton4.get() == 'on': 
        for i in type_entry.get().strip().split(','):
            filters['Type'].append(i)
    if Checkbutton5.get(): filters['Type'].append(Checkbutton5.get())
    filters['From'] = sender_email_entry.get().strip().split(',')
    # filters['Subject'] = subject_entry.get().strip().split(',')
    print(filters['From'])
    # if not filters['Subject'][0]:
    #     filters.pop('Subject')
    if not filters['From'][0]:
        filters.pop('From')
    filters['Start_date'] = cal1_data.get()[:-2] + '20' + cal1_data.get()[-2:]
    filters['End_date'] = cal2_data.get()[:-2] + '20' + cal2_data.get()[-2:]
    filters['usernames'] = [usernames[0].get(),usernames[1].get(),usernames[2].get(),usernames[3].get(),usernames[4].get()]
    filters['Subject'] = subject_entry.get().strip().split(',')
    if not filters['Subject'][0]:
        filters.pop('Subject')
    print(filters)
    #global emails
    #emails = attachment_extractor.get_attachment_count(filters)
    tk.messagebox.showinfo("", "Filters Applied")
    path_page.pack(fill="both",expand = "1")
    filter_page.pack_forget()
    login_detail_page.pack_forget()

def download():
    global emails
    global filters
    global var
    if path_entry.get()=='':
        tk.messagebox.showerror(title="Select a valid path!", message="Select a valid path")
        return
    print("Path_",path_entry.get())
    print('Here')
    # emails = attachment_extractor.get_attachment_count(filters)
    # x = threading.Thread(target=attachment_extractor.get_attachments, args=(emails,[Checkbutton1.get(),Checkbutton2.get(),Checkbutton3.get(),Checkbutton4.get(), Checkbutton5.get()],path_entry.get()), daemon=True)
    # x.start()
    location_filter = ''
    print(var.get())
    if var.get() == 1:
        location_filter = 'From'
    elif var.get() == 2:
        location_filter = 'Subject'
    elif var.get() == 3:
        location_filter = folder_entry.get()
    else:
        location_filter = ''
    print(location_filter)
    tk.messagebox.showinfo("",attachment_extractor.download(filters, path_entry.get(), location_filter))

def close():
    attachment_extractor.cleanup()
    window.destroy()

apply_filter_btn = tk.Button(filter_page,
                             text='Apply Filter', bg="#333333",fg="white", borderwidth=0, highlightthickness=0,
                             command=apply_filter, relief="groove")
apply_filter_btn.place(x=470, y=450, width=70, height=30)

window.protocol('WM_DELETE_WINDOW',close)

# path_page
canvas2 = tk.Canvas(
    path_page, bg="#333333", height=window.winfo_screenheight(), width=window.winfo_screenwidth(),
    bd=0, highlightthickness=0, relief="ridge")
canvas2.place(x=0, y=0)
canvas2.create_rectangle(300, 0, 300 + window.winfo_screenwidth(),
                         window.winfo_screenheight(), fill="#008080", outline="")

downloads_btn = tk.Button(path_page,
                             text='Downloads Summary', bg="#008080", borderwidth=0, highlightthickness=0,
                             command=change_to_downloads_page, relief="groove")
downloads_btn.place(x=27, y=30, width=120, height=30)
title = tk.Label(path_page,
                 text="Path Page", bg="#333333",
                 fg="white", font=("Arial-BoldMT", int(20.0)))
title.place(x=27.0, y=120.0)

# info_text = tk.Label(path_page,
#                      text=".\n\n"

#                      "Even this GUI was created\n"
#                      "using Tkinter Designer.",
#                      bg="#333333", fg="white", justify="left",
#                      font=("Geor
# gia", int(16.0)))

# info_text.place(x=27.0, y=200.0)

folder_entry = tk.Entry(path_page, bd=0, bg="white",
                      fg="#000716", highlightthickness=0)

def other_(): 
    R4.place_forget()
    folder_entry.place(x=490.0, y=160, width=200, height=20)
    R4.place(x=450.0,y=190)
    folder_entry.focus()

    
def delete_other_1():
    folder_entry.place_forget()
    R4.place_forget()
    R4.place(x=450.0,y=160)

label5 = tk.Label(path_page,
                  text="Create folder by name: ", bg="#008080", fg="#000716",
                  font=("Times New Roman", 13)
                  )
label5.place(x=445, y=40)

R1 = Radiobutton(path_page, text="Sender Email Address", variable=var, value=1,command=delete_other_1)
R1.place(x=450.0, y=70)

R2 = Radiobutton(path_page, text="Subject", variable=var, value=2,command=delete_other_1)
R2.place(x=450.0, y=100)

R3 = Radiobutton(path_page, text="Custom", variable=var, value=3,command=other_)
R3.place(x=450.0, y=130)

R4 = Radiobutton(path_page, text="None", variable=var, value=4,command=delete_other_1)
R4.place(x=450.0, y=160)

path_entry = tk.Entry(path_page, bd=0, bg="white",
                      fg="#000716", highlightthickness=0)
path_entry.place(x=450.0, y=299+25, width=321.0, height=35)
path_picker_img = tk.PhotoImage(file=ASSETS_PATH / "path_picker.png")
path_picker_button = tk.Button(
    path_page,
    image=path_picker_img,
    text='',
    compound='center',
    fg='white',
    borderwidth=0,
    highlightthickness=0,
    command=select_path,
    relief='flat')
path_picker_button.place(
    x=743, y=327,
    width=24,
    height=22)

path_back_btn = tk.Button(path_page,
                          text='Back', bg="#333333", 
                          fg="white",
                          borderwidth=0, highlightthickness=0,
                          command=change_to_filter_page, relief="groove")
path_back_btn.place(x=500, y=401, width=70, height=30)

path_Download_btn = tk.Button(path_page,
                              text='Download', bg="#333333", 
                              fg="white",
                              borderwidth=0, highlightthickness=0,
                              relief="groove", command=download)
path_Download_btn.place(x=600, y=401, width=70, height=30)

canvas2.create_text(
    450.0, 308.5, text="Specify the destination folder :",
    fill="black", font=("Arial-BoldMT", int(13.0)), anchor="w")

if(attachment_extractor.already_logged_in()):
    filter_page.pack(fill='both', expand=1)
    login_detail_page.pack_forget()
    keys = attachment_extractor.display_users()
    j = 200
    k=90
    btn_dict = {} 
    # Checkbutton1 = IntVar()
    usernames = [IntVar(),IntVar(),IntVar(),IntVar(),IntVar()]
    for i,key in enumerate(keys):
        Button1 = tk.Checkbutton(filter_page, text=key,
                      
                      variable=usernames[i],bg="#008080",
                      onvalue=1,
                      offvalue=0,

                      )
        Button1.place(x=670, y=k)
        k += 30

#dowmload summary 
canvas2 = tk.Canvas(
    downloads_view_page, bg="#333333", height=window.winfo_screenheight(), width=window.winfo_screenwidth(),
    bd=0, highlightthickness=0, relief="ridge")
canvas2.place(x=0, y=0)
canvas2.create_rectangle(300, 0, 300 + window.winfo_screenwidth(),
                         window.winfo_screenheight(), fill="#008080", outline="")

path_back_btn = tk.Button(downloads_view_page,
                              text='Back', bg="#333333", 
                              fg="white",font = ("Times New Roman",13),
                              borderwidth=0, highlightthickness=0,
                              command=change_to_path_page, relief="groove")
path_back_btn.place(x=500, y=401, width=70, height=30)

summary = tk.Text(
    downloads_view_page, bd=0, bg="black", fg="white",  highlightthickness=0)
summary.place(x=360, y=20, width=420, height=300)
summary.focus()
# summary.insert('insert',"hello")
logfile = 'C:/Users/Dell/Desktop/Email_attachment_extractor/logfile.txt'
def read_next(filename,lastseen=0):
    with open(filename) as fp:
        fp.seek(lastseen)
        for line in fp:
            data = line.rstrip(',')
            if data == "Download_Complete":
                pass
                # lb["text"] = "Downloads Completed!"
            else:
                summary.insert(END,data)
                # lb["text"] = "Downloads Pending..."
            # print(data)
        return fp.tell()

def read_log():
    lastseen = 0
    while(1):
        lastseen = read_next(logfile,lastseen)
        time.sleep(5)

threading.Thread(target=read_log, args = (),daemon=True).start()

window.mainloop()
