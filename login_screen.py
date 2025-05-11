import tkinter as tk
from tkinter import ttk ,PhotoImage,messagebox
import db_connection
import Freelance_Dashboards
import Client_Dashboard


class Freelance_profile:
    def __init__(self, root, user_id,user_name,user_role):
        self.root = root
        self.user_id = user_id
        self.user_name=user_name
        self.user_role=user_role
        self.root.title("Freelancer Profile Setup")
        self.root.geometry("1200x700") 
        self.root.resizable(False, False)  
        self.root.configure(bg='white')

        # Centering the window
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1200x700+{x}+{y}")

        # Title
        tk.Label(self.root,text=f"Welcome  {self.user_name}!",font=('Times New Roman',18,'bold'),fg='black',bg='white').place(x=50,y=20)
        tk.Label(self.root, text="Setup Your Freelance Profile", font=("Arial", 24, "bold"), fg="#0a295c", bg="white").place(x=360,y=80)

        # Description Label + Text Area
        tk.Label(self.root, text="Profile Description", font=("Arial", 14), bg="white").place(x=50, y=140)
        self.description_text = tk.Text(self.root, height=5, width=90,bd=1,relief='solid', font=("Arial", 14))
        self.description_text.place(x=50, y=180)

        # Skills Section
        tk.Label(self.root, text="Select Your Skills", font=("Arial", 14), bg="white").place(x=50, y=330)
        skills = ["Python","Web Development", "Graphic Design","Digital Marketing","SEO", "Content Writing",
                    "Data Analysis", "UI/UX","App Development",
                    "Video Editing", "Cloud Computing", "Database Design", "Cybersecurity"
                ]
        self.skill_vars = {}

        skill_frame = tk.Frame(self.root, width=1100, bg='white')
        skill_frame.place(relx=0.5, y=360, anchor='n')  # Centered horizontally

        for idx, skill in enumerate(skills):
            var = tk.BooleanVar()
            cb = tk.Checkbutton(skill_frame, text=skill, variable=var, bg='white',font=('Arial', 12, 'bold'), anchor='w')
            cb.grid(row=idx // 4, column=idx % 4, padx=40, pady=15, sticky='w')
            self.skill_vars[skill] = var

        # Save Button
        save_btn = tk.Button(self.root, text="Save & Continue", bg="blue", fg="white", font=("Arial", 12),
                             width=30, height=1, command=self.save_profile)
        save_btn.place(x=450, y=620)

    def save_profile(self):
        description = self.description_text.get("1.0", "end").strip()
        selected_skills = [skill for skill, var in self.skill_vars.items() if var.get()]

        if not description or not selected_skills:
            messagebox.showerror("Error", "Please provide a description and select at least one skill.")
            return

        # Save to DB
        db_connection.save_freelancer_profile(self.user_id, description, selected_skills)
        db_connection.update_user_role(self.user_id, 3)  # Mark setup as completed
        messagebox.showinfo("Success", "Profile setup completed successfully!")
        self.root.destroy()
        Freelance_dashboard=tk.Tk()
        Freelance_Dashboards.FreelanceScreen(Freelance_dashboard,self.user_id,self.user_name,self.user_role)
        Freelance_dashboard.mainloop()
        
class RegistrationScreen:
    def __init__(self,reg_root):
        self.reg_root=reg_root
        self.icon=PhotoImage(file='Logo.png')
        self.reg_root.title("Create Account-Freelance Project Management System")
        self.reg_root.geometry("1200x700")
        self.reg_root.iconphoto(True,self.icon)
        self.reg_root.resizable(False, False)
        
        # Centering the window
        x = (self.reg_root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.reg_root.winfo_screenheight() // 2) - (700 // 2)
        self.reg_root.geometry(f"1200x700+{x}+{y}")
        #left section
        self.left_frame=tk.Frame(self.reg_root,bg="#0a295c",width=400,height=700)
        self.left_frame.place(x=-0,y=0)
        self.logo=PhotoImage(file='Logo.png').subsample(2,2)
        title_label=tk.Label(self.left_frame,text="Join\nUs",image=self.logo,font=('Sacrifice Demo',30,'bold'), fg='white',bg='#0a295c',justify='center',compound="top")
        title_label.place(relx=0.5,rely=0.5,anchor='center')
        title_label.image=self.logo
        #right section
        self.right_frame=tk.Frame(self.reg_root,bg='white',width=800,height=700)
        self.right_frame.place(x=400,y=0)
        #header
        header = tk.Label(self.right_frame, text="Create a New Account", font=("Arial", 22, "bold"), fg="#0a295c", bg="white")
        header.place(x=200, y=40)
        #name
        tk.Label(self.right_frame,text="Full Name",font=('Arial',14),bg='white').place(x=20,y=120)
        self.name_entry=ttk.Entry(self.right_frame,width=30,font=('Aria',14))
        self.name_entry.place(x=20,y=160,height=50)
        #Phone
        tk.Label(self.right_frame,text="Phone No.",font=('Arial',14),bg='white').place(x=410,y=120)
        self.phone_entry=ttk.Entry(self.right_frame,width=30,font=('Arial',14))
        self.phone_entry.place(x=410,y=160,height=50)
        #Email
        tk.Label(self.right_frame,text='Email',font=('Arial',14),bg='white').place(x=20,y=240)
        self.email_entry=ttk.Entry(self.right_frame,width=30,font=('Arial',14))
        self.email_entry.place(x=20,y=280,height=50)
        #Password
        tk.Label(self.right_frame,text='Password',font=('Arial',14),bg='white').place(x=410,y=240)
        self.password_entry=ttk.Entry(self.right_frame,font=('Arial',14),width=30,show='x')
        self.password_entry.place(x=410,y=280,height=50)
        # Role Selection
        tk.Label(self.right_frame, text="Register As", font=('Arial', 14), bg='white').place(x=20, y=360)
        self.role_var = tk.StringVar(value='Freelancer')
        self.role_dropdown = ttk.Combobox(self.right_frame, textvariable=self.role_var, font=('Arial', 14), state='readonly', width=30)
        self.role_dropdown['values'] = ['Freelancer', 'Client']
        self.role_dropdown.place(x=20, y=400,height=50)
 
        #Register Button
        tk.Button(self.right_frame, text="Register", bg='Blue', fg='white',activebackground='Blue',activeforeground='white',font=('Arial', 14), width=25, command=self.register_user).place(x=40, y=500)
        #Back to Login
        tk.Button(self.right_frame, text="Login Account", bg='Blue', fg='white',activebackground='Blue',activeforeground='white',font=('Arial', 14), width=25, command=self.back_to_login).place(x=420, y=500)
        
        copyright_label = tk.Label(self.right_frame, text="© 2025 Freelance Management System. All rights reserved.",
                                   font=("Arial", 10), fg="gray", bg="white")
        copyright_label.place(x=200, y=650)
    #Method of Back to Login
    def back_to_login(self):
        self.reg_root.destroy()
        root=tk.Tk()
        LoginScreen(root)
        root.mainloop()
    #Register 
    def register_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()

        if not all([name, email, phone, password, role]):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        # Convert role to numeric values
        if role == 'Freelancer':
            role_value = 1
        elif role == 'Client':
            role_value = 2


        # Call database function to register
        success = db_connection.register_user(name, email, phone, password, role_value)
        if success=='User_Exist':
            messagebox.showerror("Error","Email has already been Registered!")
        elif success:
            messagebox.showinfo("Success", "Account created successfully!")
            self.reg_root.destroy()
            root = tk.Tk()
            LoginScreen(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Something went wrong during registration.")



class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.icon=PhotoImage(file="Logo.png")
        self.root.title("Login-Freelance Project Management System")
        self.root.geometry("1200x700") 
        self.root.iconphoto(True,self.icon) 
        self.root.resizable(False, False)  

        # Centering the window
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1200x700+{x}+{y}")

        # Left Panel - Dark Blue
        self.left_frame = tk.Frame(self.root, width=400, height=700)
        self.left_frame.place(x=0, y=0)

        self.left_bg_image = PhotoImage(file="login_bg.png")  
        self.left_bg_label = tk.Label(self.left_frame, image=self.left_bg_image)
        self.left_bg_label.place(x=0, y=0)

        # Right Panel - White (Login Section)
        self.right_frame = tk.Frame(self.root, bg="white", width=800, height=700)
        self.right_frame.place(x=400, y=0)
    
        welcome_label=tk.Label(self.right_frame,text="Welcome  Back",font=('Ananda Black Personal Use',24,"bold"),fg='black',bg='White')
        welcome_label.place(x=50,y=50)

        login_label = tk.Label(self.right_frame, text="Login to your account", font=("Arial", 22, "bold"), fg="#0a295c", bg="white")
        login_label.place(x=200, y=150)

        # Email Field
        email_label = tk.Label(self.right_frame, text="Email Address", font=("Arial", 14), bg="white")
        email_label.place(x=200, y=230)
        self.email_entry = ttk.Entry(self.right_frame, width=35, font=('Arial', 14))
        self.email_entry.place(x=200, y=270, height=50)

        # Password Field
        password_label = tk.Label(self.right_frame, text="Password", font=("Arial", 14), bg="white")
        password_label.place(x=200, y=330)
        self.password_entry = ttk.Entry(self.right_frame, width=35, show="x", font=('Arial', 14))
        self.password_entry.place(x=200, y=370, height=50)

        # Login Button
        login_button = tk.Button(self.right_frame, text="Login", bg='Blue',fg='White',activebackground='Blue',activeforeground='White',font=('Arial', 14),anchor='center',width=32,command=self.login)
        login_button.place(x=200, y=440)

        # "Don't have an account?" Label
        register_label = tk.Label(self.right_frame, text="Don't have an account? ", font=("Arial", 12), bg="white")
        register_label.place(x=210, y=500)

        # "Create a new account" Clickable Label
        create_account_label = tk.Label(self.right_frame, text="Create a new account", font=("Arial", 12, "bold"),
                                        fg="blue", bg="white", cursor="hand2")
        create_account_label.place(x=410, y=500)
        create_account_label.bind("<Button-1>", self.open_registration)

        # Copyright Text
        copyright_label = tk.Label(self.root, text="© 2025 Freelance Management System. All rights reserved.",
                                   font=("Arial", 10), fg="gray", bg="white")
        copyright_label.place(x=600, y=650)
    
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if not email or not password:
            messagebox.showerror("Login Failed", "Please enter both email and password!")
            return
        user=db_connection.authenticate_user(email,password)
        if user:
            if user[3]==2:
                activate=messagebox.askyesno("Info","Account is deactivated.Do you want to activate?")
                if activate:
                    activate_account=db_connection.activate_account(user[0])
                    messagebox.showinfo("Info","Activated,Sign in Again!")
                    return
                else:
                    messagebox.showerror("Error","Something Gone wrong!")

            messagebox.showinfo("Login Successful", f"Welcome {user[1]}!")
            self.root.destroy()
            if user[2] == 1:
                Profile_root=tk.Tk()
                Freelance_profile(Profile_root,user[0],user[1],user[2])
                Profile_root.mainloop()  
            elif user[2] == 2:
                Client=tk.Tk()
                Client_Dashboard.ClientScreen(Client,user[0],user[1],user[2])
                Client.mainloop()
            elif user[2] == 3:
                Freelance=tk.Tk()
                Freelance_Dashboards.FreelanceScreen(Freelance,user[0],user[1],user[2])
                Freelance.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password!")
    def open_registration(self, event):
        self.root.destroy()
        reg_root=tk.Tk()
        RegistrationScreen(reg_root)
        reg_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    LoginScreen(root)
    root.mainloop()
