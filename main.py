from tkinter import *
from tkinter import messagebox
import pyperclip
import random
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pw():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    password_entry.delete(0,END)
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 6)
    password_list=[random.choice(letters) for char in range(nr_letters)]
    password_list+=[random.choice(symbols) for sym in range(nr_symbols)]
    password_list+=[random.choice(numbers) for num in range(nr_numbers)]
    random.shuffle(password_list)
    while password_list[0] in symbols:
        random.shuffle(password_list)

    password = "".join(password_list)
    # password = ""
    # for char in password_list:
    #   password += char
    password_entry.insert(0,password)
    pyperclip.copy(password)
    #print(f"Your password is: {password}")
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    web = website_entry.get().title()
    gmail_txt = email_entry.get()
    pw = password_entry.get()
    new_data = {
        web:{
            "email": gmail_txt,
            "password": pw
        }
    }
    if len(web) == 0 or len(gmail_txt) == 0 or len(pw) == 0:
        messagebox.showerror("Empry Field", "Please dont leave any fields empty")
    else:
        is_ok = messagebox.askokcancel(title=web,message=f"These are details entered: \n Email: {gmail_txt} \n Password: {pw} \n Is it ok to Save?")
        if is_ok:
            try:
                with open("Password.json", "r") as file:
                    data = json.load(file)
                    data.update(new_data)
                with open("Password.json", "w") as file:
                    json.dump(data, file, indent=4)
                    website_entry.delete(0, END)
                    password_entry.delete(0, END)
            except FileNotFoundError:
                with open("Password.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

def search():
    web = website_entry.get().title()
    try:
        with open("Password.json") as file:
            data = json.load(file)
            if web in data:
                pyperclip.copy(data[web]['password'])
                messagebox.showinfo(web,f"Email: {data[web]['email']}\nPassword: {data[web]['password']} ")
            else:
                messagebox.showinfo(web, f"No details for {web} exists")
    except FileNotFoundError:
        messagebox.showerror("Error","File is not Found,\n First add information")


def remove_last():

    sure = messagebox.askyesno("Delete","Are you sure that you want to delete last row?")
    if sure:
        with open("Password.json","r") as file:
            data = json.load(file)
            web_del = list(data)
            #print(web_del[-1])
            del data[web_del[-1]]
        with open("Password.json", "w") as file:
            json.dump(data, file, indent=4)
            #print(data)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
#window.minsize(450,450)
window.config(padx=50,pady=50)
#canva
canva = Canvas(height=200,width=200)
logo_image = PhotoImage(file="logo.png")
canva.create_image(100,100,image=logo_image)
canva.grid(row=0,column=1)
#website
website = Label(text="Website:")
website.grid(row=1,column=0)
website_entry = Entry(width=21,borderwidth=3)
website_entry.grid(row=1,column=1,columnspan=2,sticky='EW',pady=10)
website_entry.focus()
#email
email = Label(text="Email/Username:")
email.grid(row=2,column=0)
email_entry = Entry(width=35,borderwidth=3)
email_entry.grid(row=2,column=1,columnspan=2,sticky='EW',pady=10)
email_entry.insert(0,"serhi1334@gmail.com")
#password
password = Label(text="Password:")
password.grid(row=3,column=0)
password_entry = Entry(width=21,borderwidth=3)
password_entry.grid(row=3,column=1,sticky='EW',pady=10)
#btn
delete_btn = Button(text="Delete Last Row",width=36,command=remove_last)
delete_btn.grid(row=5,column=1,columnspan=2,sticky='EW')
generate_btn = Button(text="Generate Password",command=generate_pw)
generate_btn.grid(row=3,column=2,sticky='EW')
add_btn = Button(text="Add",width=36,command=save)
add_btn.grid(row=4,column=1,columnspan=2,sticky='EW',pady=10)
search_btn = Button(text="Search",command=search)
search_btn.grid(row=1,column=2,sticky=EW)
#label credit
me = Label(text="Made by Serhan",font=("Courier",10,"bold"))
me.grid(row=0,column=0,sticky=N)


window.mainloop()