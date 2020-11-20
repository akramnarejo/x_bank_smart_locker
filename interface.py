from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import filedialog
import os
import glob
from iris_recognition import Iris_Recognition
from database import Database
import shutil
import pickle

iris_obj = Iris_Recognition()
db = Database()


root = Tk(className="Iris recognizer")
root.title("X Bank")
root.geometry("900x900")
root.resizable(0,0)
root.update()


def raise_frame(frame):
    frame.tkraise()

def close():
    root.destroy()

profile_picture = ''
def upload_pic():
    global profile_picture
    profile_picture = filedialog.askopenfilename(initialdir="./", title="Select a File", filetypes=(("JPG files","*.JPG*"),("all files", "*.*")))
    if not profile_picture:
        profile_label.configure(text='file not Selected')
    else:
        profile_label.configure(text='Selected')
manager_iris_image1 = ''
def manager_upload_iris1():
    global manager_iris_image1
    manager_iris_image1 = filedialog.askopenfilename(initialdir="./", title="Select a File", filetypes=(("JPG files","*.JPG*"),("all files", "*.*")))
    if not manager_iris_image1:
        manager_iris1_label.configure(text='file not Selected')
    else:
        manager_iris1_label.configure(text='Selected')

manager_iris_image2 = ''
def manager_upload_iris2():
    global manager_iris_image2
    manager_iris_image2 = filedialog.askopenfilename(initialdir="./", title="Select a File", filetypes=(("JPG files","*.JPG*"),("all files", "*.*")))
    if not manager_iris_image2:
        manager_iris2_label.configure(text='file not Selected')
    else:
        manager_iris2_label.configure(text='Selected')

customer_iris_image1 = ''
def customer_upload_iris1():
    global customer_iris_image1
    customer_iris_image1 = filedialog.askopenfilename(initialdir="./", title="Select a File", filetypes=(("JPG files","*.JPG*"),("all files", "*.*")))
    if not customer_iris_image1:
        customer_iris1_label.configure(text='file not selected')
    else:
        customer_iris1_label.configure(text='Selected')


customer_iris_image2 = ''
def customer_upload_iris2():
    global customer_iris_image2
    customer_iris_image2 = filedialog.askopenfilename(initialdir="./", title="Select a File", filetypes=(("JPG files","*.JPG*"),("all files", "*.*")))
    if not customer_iris_image2:
        customer_iris2_label.configure(text='file not selected')
    else:
        customer_iris2_label.configure(text='Selected')

def recognize_iris(img):
    crop,r = iris_obj.localize_iris(img)
    normalized = iris_obj.normalize_iris(crop,60,300,r,100)
    encoded = iris_obj.encode_features(normalized)
    return encoded

def save_manager():
    global manager_iris_image1
    global manager_iris_image2
    existing_irises = []
    if os.path.isfile('./db.pkl'):
        data = db.read()
        for mkey in data.keys():
            for iris in data[mkey]['iris']:
                existing_irises.append(iris)
    
    if manager_name_entry.get() == '' or manager_cnic_entry.get() == '' or manager_iris_image1 == '':
        messagebox.showerror('Error','Please provide the required data to register.')
    else:
        yes = False
        for i in [manager_iris_image1, manager_iris_image2]:
            check, img = iris_obj.match_iris(recognize_iris(i), existing_irises)
            if check:
                yes = True
                break
        if yes:
            messagebox.showerror('Error', 'This user already exists.')
        else:
            if messagebox.showinfo('Info', 'Your account has been created! \n Please Log In.'):
                db.write(manager_name_entry.get(),manager_cnic_entry.get(),recognize_iris(manager_iris_image1),recognize_iris(manager_iris_image2))
                raise_frame(home)
            # manager_name.configure(text='Bank Manager ('+manager_name_entry.get()+') is signedIn')
            # manager_name2.configure(text='Bank Manager ('+manager_name_entry.get()+') is signedIn')
            # manager_name3.configure(text='Bank Manager ('+manager_name_entry.get()+') is signedIn')
        manager_name_entry.delete(0, END)
        manager_cnic_entry.delete(0, END)
        manager_iris_image1 = ''
        manager_iris_image2 = ''
        manager_iris1_label.configure(text='')
        manager_iris2_label.configure(text='')
        

login_manager_iris = ''
imglbl = ''
def login_manager_iris_upload():
    global login_manager_iris
    login_manager_iris = filedialog.askopenfilename(initialdir="./", title="Select a File", filetypes=(("JPG files","*.JPG*"),("all files", "*.*")))
    print(login_manager_iris)

    crop, r = iris_obj.localize_iris(login_manager_iris)
    img = Image.fromarray(crop, 'RGB')
    render = ImageTk.PhotoImage(img)
    global imglbl
    imglbl = Label(manager_login, image=render)
    imglbl.image = render
    imglbl.place(x=180,y=220)

manager = ''
def login_manager():
    if login_manager_iris != '':
        global imglbl
        if os.path.isfile('./db.pkl'):
            data = db.read()
            irises = list()
            for key in data.keys():
                for iris in data[key]['iris']:
                    irises.append(iris)
            check, img = iris_obj.match_iris(recognize_iris(login_manager_iris), irises)
            if check:
                global manager
                # user = ''
                for key in data.keys():
                    for val in data[key]['iris']:
                        if (img == val).all():
                            manager = key
                            break
                manager_name.configure(text='Bank Manager ('+data[manager]['name']+') is SignedIn')
                raise_frame(manager_page)
                imglbl.image = None
            else:
                imglbl.image = None
                messagebox.showerror("Error", "Invalid iris \nPlease try agian.")
                
        else:
            imglbl.image = None
            messagebox.showerror("Error", "You are not registered")
    else:
        messagebox.showerror('Error', 'Please provide the required data.')
        

def logout_manager():
    raise_frame(home)

locker = 0
def save_customer():
    global customer_iris_image1
    global customer_iris_image2
    if customer_name_entry.get() == '' or customer_cnic_entry.get() == '' or customer_iris_image1 == '':
        messagebox.showerror('Error', 'Please provide the required data to register.')
    else:
        global locker
        locker += 1
        data = db.read()
        irises = []
        existing_irises = []
        # getting existing irises
        for mkey in data.keys():
            if data[mkey]['customers'].keys():
                for ckey in data[mkey]['customers'].keys():
                    for iris in data[mkey]['customers'][ckey]['iris']:
                        existing_irises.append(iris)
            else:
                break
        # checking if new iris already exists
        iris_exists = False
        for i in [customer_iris_image1,customer_iris_image2]:
            if i != '':
                check,img = iris_obj.match_iris(recognize_iris(i), existing_irises)
                if check:
                    iris_exists = True
                else:
                    irises.append(recognize_iris(i).ravel()) 
        if iris_exists:
            messagebox.showerror("Error", "This user already exists.")
        else:
            username = customer_name_entry.get()
            username = username.replace(" ","")
            for mkey in data.keys():       
                if username not in data[mkey]['customers'].keys():
                    data[mkey]['customers'][username] = {
                        'name':customer_name_entry.get(),
                        'cnic':customer_cnic_entry.get(),
                        'locker':locker,
                        'iris':irises
                    }
            if messagebox.showinfo('Info', 'Your account has been created! \n Please Log In.'):
                with open('./db.pkl','wb') as book:
                    pickle.dump(data, book)
                raise_frame(manager_page)
        
        customer_name_entry.delete(0, END)
        customer_cnic_entry.delete(0, END)
        customer_iris_image1 = ''
        customer_iris_image2 = ''
        customer_iris1_label.configure(text='')
        customer_iris2_label.configure(text='')
    


login_customer_iris = ''
customerloginImglbl = ''
def login_customer_iris_upload():
    global customerloginImglbl
    global login_customer_iris
    login_customer_iris = filedialog.askopenfilename(initialdir="./", title="Select a File", filetypes=(("JPG files","*.JPG*"),("all files", "*.*")))
    print(login_customer_iris)

    crop, r = iris_obj.localize_iris(login_customer_iris)
    img = Image.fromarray(crop, 'RGB')
    render = ImageTk.PhotoImage(img)
    global customerloginImglbl
    customerloginImglbl = Label(customer_login, image=render)
    customerloginImglbl.image = render
    customerloginImglbl.place(x=190,y=260)


customer = ''
manager_customer = ''
def login_customer():
    global login_customer_iris
    if login_customer_iris != '':
        global customerloginImglbl
        data = db.read()
        irises = list()
        for mkey in data.keys():
            for ckey in data[mkey]['customers'].keys():
                for iris in data[mkey]['customers'][ckey]['iris']:
                    irises.append(iris)
        check, img = iris_obj.match_iris(recognize_iris(login_customer_iris), irises)
        if check:
            global customer
            # user = ''
            for mkey in data.keys():
                for ckey in data[mkey]['customers'].keys():
                    for val in data[mkey]['customers'][ckey]['iris']:
                        if (img == val).all():
                            customer = ckey
                            manager_customer = mkey

            customer_name.configure(text=''+data[manager_customer]['customers'][customer]['name']+' is SignedIn')
            customer_locker_num.configure(text='Locker number: '+str(data[manager_customer]['customers'][customer]['locker'])+' ')
            raise_frame(customer_page)
            customerloginImglbl.image = None
        else:
            customerloginImglbl.image = None
            messagebox.showerror("Error", "Invalid iris \nPlease try agian.") 
    else:
        messagebox.showerror('Error','Please provide the required data.')

def logout_customer():
    raise_frame(manager_page)

home = Frame(root, width=700)
manager_login = Frame(root)
manager_register = Frame(root)
manager_page = Frame(root)
customer_login = Frame(root)
customer_register = Frame(root)
customer_page = Frame(root)

for frame in (home,manager_login,manager_register,manager_page,customer_login,customer_register, customer_page):
    frame.grid(row=0, column=0, padx=100, pady=70, sticky='news')

# home page
Label(home, text='Welcome to smart bank locker',font=("Courier",30)).pack(pady=70)
Button(home, text="login Bank Manager", width=20,height=2, font=("Courier", 20), command=lambda:raise_frame(manager_login)).pack(pady=10)
Button(home, text="Register Bank Manager", width=20, height=2, font=("Courier", 20), command=lambda:raise_frame(manager_register)).pack(pady=10)
Button(home, text="Close", width=10, height=1, font=("Courier",20),command=close).pack(pady=150)

#manager login page
Label(manager_login, text='Bank Manager Login',font=("Courier",30)).pack(pady=50)
Button(manager_login, text='Please use iris image', font=("Courier", 20),command=login_manager_iris_upload).pack(pady=10)
Button(manager_login, text='Back', font=("Courier",20), command=lambda: raise_frame(home)).place(x=220,y=600)
Button(manager_login, text='LogIn', font=("Courier",20),command=login_manager).place(x=330,y=600)


#manager registeration page
Label(manager_register, text='Bank Manager Register', font=("Courier",30)).pack(pady=50)

Label(manager_register, text='Name:', font=("Courier",20)).place(x=100, y=100)
manager_name_entry = Entry(manager_register,width=20,fg='black', font=("Courier",20))
manager_name_entry.place(x=100,y=125)

Label(manager_register, text="Enter CNIC:", font=('Courier',20)).place(x=100,y=165)
manager_cnic_entry = Entry(manager_register, width=20, font=('Courier',20))
manager_cnic_entry.place(x=100,y=190)

Label(manager_register, text='Profile picture', font=('Courier',20)).place(x=100,y=230)
Button(manager_register, height=1, text='Select', font=('Courier',20), command=upload_pic).place(x=100,y=260)
profile_label = Label(manager_register, text='', font=("Courier",12))
profile_label.place(x=225, y=270)

Label(manager_register, text='Upload Iris Image 1', font=('Courier',20)).place(x=100, y=310)
iris_img1 = Button(manager_register, height=1, text='Select', font=('Courier',20),command=manager_upload_iris1).place(x=100,y=340)
manager_iris1_label = Label(manager_register, text='', font=("Courier",12), )
manager_iris1_label.place(x=225, y=350)

Label(manager_register, text='Upload Iris Image 2', font=('Courier',20)).place(x=100, y=390)
manageriris_img2 = Button(manager_register, height=1, text='Select', font=('Courier',20), command=manager_upload_iris2).place(x=100, y=420)
manager_iris2_label = Label(manager_register, text='', font=("Courier",12), )
manager_iris2_label.place(x=225, y=430)

Button(manager_register, text='Back', font=("Courier",20), command=lambda: raise_frame(home)).place(x=100,y=600)
Button(manager_register, text='Register', font=("Courier",20),command=save_manager).place(x=200,y=600)


#manager home page
manager_name = Label(manager_page, text='', font=("Courier",20))
manager_name.place(x=50, y=100)
Label(manager_page, text='Bank Locker User\n Window', font=("Courier", 30)).place(x=120, y=150)
Button(manager_page, text='Login Locker User', width=20, height=2, font=("Courier",20), command=lambda:raise_frame(customer_login)).place(x=150,y=300)
Button(manager_page, text='Register Locker User', width=20, height=2,font=("Courier",20), command=lambda:raise_frame(customer_register)).place(x=150, y=400)
Button(manager_page, text='Logout', font=('Courier',20), command=logout_manager).place(x=250,y=550)


#customer register page
manager_name2 = Label(customer_register, text='', font=("Courier",20))
manager_name2.place(x=50, y=100)
Label(customer_register, text='Bank Locker User\n Registration', font=("Courier", 30)).place(x=120, y=150)

Label(customer_register, text='Name:', font=("Courier",20)).place(x=100, y=230)
customer_name_entry = Entry(customer_register,width=20,fg='black', font=("Courier",20))
customer_name_entry.place(x=100,y=250)

Label(customer_register, text="Enter CNIC:", font=('Courier',20)).place(x=100,y=290)
customer_cnic_entry = Entry(customer_register, width=20, font=('Courier',20))
customer_cnic_entry.place(x=100,y=310)

Label(customer_register, text='Upload Iris Image 1', font=('Courier',20)).place(x=100, y=345)
customer_iris_img1 = Button(customer_register, height=1, text='Select', font=('Courier',20),command=customer_upload_iris1).place(x=100,y=370)
customer_iris1_label = Label(customer_register, text='', font=("Courier",12), )
customer_iris1_label.place(x=225, y=380)

Label(customer_register, text='Upload Iris Image 2', font=('Courier',20)).place(x=100, y=415)
customer_iris_img2 = Button(customer_register, height=1, text='Select', font=('Courier',20), command=customer_upload_iris2).place(x=100, y=445)
customer_iris2_label = Label(customer_register, text='', font=("Courier",12), )
customer_iris2_label.place(x=225, y=450)

Button(customer_register, text='Back', font=("Courier",20), command=lambda: raise_frame(manager_page)).place(x=100,y=600)
Button(customer_register, text='Register', font=("Courier",20),command=save_customer).place(x=200,y=600)


# customer login page
manager_name3 = Label(customer_login, text='', font=("Courier",20))
manager_name3.place(x=50, y=100)
Label(customer_login, text='Bank Locker User Login', font=("Courier", 30)).place(x=100, y=150)
Button(customer_login, text='Please use iris image', font=("Courier", 20),command=login_customer_iris_upload).place(x=175, y=200)
Button(customer_login, text='Back', font=("Courier",20), command=lambda: raise_frame(manager_page)).place(x=220,y=600)
Button(customer_login, text='LogIn', font=("Courier",20),command=login_customer).place(x=330,y=600)

# customer home page
Label(customer_page, text='Welcome to Smart Bank Locker', font=("Courier", 30)).place(x=50, y=100)
customer_name = Label(customer_page, text='', font=("Courier",20))
customer_name.place(x=100, y=200)
customer_locker_num = Label(customer_page, text='', font=('Courier',20))
customer_locker_num.place(x=100, y=250)

Button(customer_page, text='Logout', font=('Courier',20), command=logout_customer).place(x=250,y=550)





raise_frame(home)

root.mainloop()