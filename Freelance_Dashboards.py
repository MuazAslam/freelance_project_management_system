import tkinter as tk
from tkinter import ttk ,PhotoImage,messagebox
import db_connection
class FreelanceScreen:
    def __init__(self,root,user_id,username,user_role):
        self.root=root
        self.user_id=user_id
        self.user_role=user_role
        self.icon=PhotoImage(file='Logo.png')
        self.root.title('Freelance Dashboard-Freelance Project Management System')
        self.root.iconphoto(True,self.icon)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.state('zoomed')
        self.root.configure(bg="white")

        # Fetch user name and stats
        self.username = username
        self.stats = db_connection.get_freelancer_stats(user_id)

        self.setup_ui()

    def setup_ui(self):
        #topbar
        self.top_bar=tk.Frame(self.root,bg='#0a295c',width=self.root.winfo_screenwidth(),height=self.root.winfo_screenheight()//9)
        self.top_bar.propagate(False)
        self.top_bar.place(x=0,y=0)
        logo=PhotoImage(file='CLogo.png').subsample(3,3)
        logo_label=tk.Label(self.top_bar,image=logo,bg='#0a295c')
        logo_label.place(x=50,y=25)
        logo_label.image=logo
        # Welcome text
        welcome_label = tk.Label(self.top_bar, text=f"Welcome!\n {self.username}", bg="#0a295c",
                                 font=("Times New Roman", 18, "bold"), fg="white")
        welcome_label.place(x=200, y=20)

        freelancer_label = tk.Label(self.top_bar, text="Freelancer Dashboard", bg="#0a295c",
                                 font=("Sacrifice Demo", 40, "bold"), fg="white")
        freelancer_label.place(x=700, y=15)

        switch_button=tk.Button(self.top_bar, text="Switch to Client ", font=('Arial', 14), fg='#0a295c', bg='lightgray', activebackground='#1553b6', width=20, command=lambda:self.switch_client(self.user_id,self.username))
        switch_button.place(x=1600, y=35)

        #sidebar
        sidebar_width = 384
        sidebar_height = 960
        sidebar = tk.Frame(self.root, bg="#0a295c", width=sidebar_width, height=sidebar_height)
        sidebar.place(x=0, y=120)
        sidebar.grid_propagate(False)
        buttons = [
                ("📁 My Projects", self.view_projects),
                ("🧾 My Proposals", self.view_proposals),
                ("💰 Payments", self.view_payments),
                ("💬 Messages", self.view_messages),
                ("✍️Edit Profile", self.edit_profile),
                ("🚪 Logout",self.logout)
            ]
        btn_space=0
        for text,command in buttons:
            btn=tk.Button(sidebar,text=text,font=("Arial",14),fg='white',bg='#133a7c',activebackground='#1553b6',bd=1,relief='groove',anchor='center',width=20,command=command)
            btn.place(x=0,y=40+btn_space,height=70)
            btn_space+=100
        self.view_projects()

    def init_right_frame(self):
        self.right_frame = tk.Frame(self.root, bg='white', width=1536,height=960)
        self.right_frame.place(x=384, y=120)
        self.right_frame.grid_propagate(False)

    def switch_client(self,user_id,user_name):
        confirm=messagebox.askyesno("Info","Do you want to switch to Client Dashboard?")
        if confirm:
            import Client_Dashboard
            self.root.destroy()
            Client=tk.Tk()
            Client_Dashboard.ClientScreen(Client,user_id,user_name,self.user_role)
            Client.mainloop()
    
    def view_projects(self):
        self.init_right_frame()
        cards_frame=tk.Frame(self.right_frame,bd=2,relief='groove',highlightbackground='lightgray',highlightthickness=1,bg='white',width=1400,height=100)
        cards_frame.place(x=68,y=50)
        projects=db_connection.get_freelancer_stats(self.user_id)
        self.project_label=tk.Label(cards_frame,text=f"Completed Projects - {projects['completed']} ({projects['earnings']}$)",font=("Times New Roman",16),bg='white')
        self.project_label.place(x=10,y=30)
        self.project_var=tk.StringVar(value='Completed Projects')
        self.projects_dropdown=ttk.Combobox(cards_frame,textvariable=self.project_var,font=('Arial',16),state='readonly',width=20)
        self.projects_dropdown['values']=['Completed Projects','Active Projects','Total Projects']
        self.projects_dropdown.place(x=1050,y=25,height=50)
        self.projects_dropdown.bind("<<ComboboxSelected>>",self.update_projects_label)
        #Manage Active Projects
        tk.Label(self.right_frame,text="Active Projects",font=('Arial',18,'bold'),fg='black',bg='white').place(x=68,y=200)
        active_projects=db_connection.get_active_projects(self.user_id)
        if len(active_projects)==0:
            tk.Label(self.right_frame,text='No Current Projects\n Start Bidding to land your first Project',font=('Times New Roman',20),fg='grey',bg='white').place(x=550,y=450)
        else:
            projects_frame = tk.Frame(self.right_frame, bg='white',bd=2,relief='groove', width=1400, height=600)
            projects_frame.place(x=68, y=250)
            tk.Label(projects_frame,text='Title',font=('Arial',18,'bold'),fg='black',bg='white').place(x=150,y=10)
            tk.Label(projects_frame,text='Budget',font=('Arial',18,'bold'),fg='black',bg='white').place(x=400,y=10)
            tk.Label(projects_frame,text='Deadline',font=('Arial',18,'bold'),fg='black',bg='white').place(x=600,y=10)
            tk.Label(projects_frame,text='Client Name',font=('Arial',18,'bold'),fg='black',bg='white').place(x=850,y=10)
            tk.Label(projects_frame,text='Status',font=('Arial',18,'bold'),fg='black',bg='white').place(x=1150,y=10)
        
            canvas = tk.Canvas(projects_frame)
            canvas.place(x=50, y=60,width=1300, height=500)  # Adjust the height accordingly
            scrollbar = tk.Scrollbar(projects_frame, orient="vertical", command=canvas.yview)
            scrollbar.place(x=1320, y=60, height=500)  # Align the scrollbar with the canvas
            canvas.configure(yscrollcommand=scrollbar.set)

            # Create a frame to hold the project rows and place it on the canvas
            project_list_frame = tk.Frame(canvas,height=0, width=1240)
            canvas.create_window((10, 10), window=project_list_frame, anchor='nw')
            
            List_frame_height=65
            row = 0  # Start from the first row below the headers
            for project in active_projects:
                tk.Label(project_list_frame, text=project[0], font=('Arial', 16), fg='black', bg='white').place(x=0, y=(row * 70))  # Adjust y position for each row
                tk.Label(project_list_frame, text=f"{project[1]}$", font=('Arial', 16), fg='black', bg='white').place(x=340, y=(row * 70))
                tk.Label(project_list_frame, text=project[2], font=('Arial', 16), fg='black', bg='white').place(x=550, y=(row * 70))
                tk.Label(project_list_frame, text=project[3], font=('Arial', 16), fg='black', bg='white').place(x=800, y=(row * 70))
                tk.Label(project_list_frame, text=project[4], font=('Arial', 16), fg='green', bg='white').place(x=1100, y=(row * 70))
                row += 1  # Move to the next row
                project_list_frame.configure(height=row*List_frame_height)

            # Update the scrolling region for the canvas
            project_list_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

    def update_projects_label(self,event):
        selected_project_type=self.project_var.get()
        projects=db_connection.get_freelancer_stats(self.user_id)
        if selected_project_type=="Completed Projects":
            self.project_label.config(text=f"Completed Projects - {projects['completed']} ({projects['earnings']}$)")
        if selected_project_type=="Active Projects":
            self.project_label.config(text=f"Active Projects - {projects['active_projects']}")
        if selected_project_type=="Total Projects":
            self.project_label.config(text=f"Total Projects - {projects['total_projects']}")

    def view_proposals(self):
        self.init_right_frame()
        #Proposal Status Frame
        self.status_frame=tk.Frame(self.right_frame,bg='white',width=1400,height=400,bd=2,relief='groove')
        self.status_frame.place(x=68,y=20)
        cards_frame=tk.Frame(self.status_frame,bd=1,relief='sunken',highlightbackground='lightgray',highlightthickness=1,bg='white',width=1300,height=70)
        cards_frame.place(x=40,y=20)
        #Get Details
        self.proposals=db_connection.get_freelancer_proposal_stats(self.user_id)
        #Putting Details
        self.proposal_label=tk.Label(cards_frame,text=f" Pending Proposals- {self.proposals['Pending']}",font=("Times New Roman",16),bg='white')
        self.proposal_label.place(x=5,y=20)
        self.proposal_var=tk.StringVar(value='Pending')
        self.proposal_dropdown=ttk.Combobox(cards_frame,textvariable=self.proposal_var,font=('Arial',16),state='readonly',width=20)
        self.proposal_dropdown['values']=['Pending','Accepted','Rejected']
        self.proposal_dropdown.place(x=960,y=8,height=50)
        self.proposal_dropdown.bind("<<ComboboxSelected>>",self.update_proposal_label)
        self.proposal_list=db_connection.get_proposals_list(self.user_id)

        self.proposal_frame = tk.Frame(self.status_frame, bg='white',bd=2,relief='groove', width=1300, height=250)
        self.proposal_frame.place(x=40, y=120)
        
        if self.proposal_list==[]:
            tk.Label(self.proposal_frame,text='No Current Proposals\n Start Bidding to land your first Proposal',font=('Times New Roman',20),fg='grey',bg='white').place(x=400,y=70)
        else:
            tk.Label(self.proposal_frame,text='Project Title',font=('Arial',18,'bold'),fg='black',bg='white').place(x=100,y=10)
            tk.Label(self.proposal_frame,text='Bidding Amount',font=('Arial',18,'bold'),fg='black',bg='white').place(x=400,y=10)
            tk.Label(self.proposal_frame,text='Client Name',font=('Arial',18,'bold'),fg='black',bg='white').place(x=700,y=10)
            tk.Label(self.proposal_frame,text='Proposal Status',font=('Arial',18,'bold'),fg='black',bg='white').place(x=1000,y=10)

            canvas = tk.Canvas(self.proposal_frame)
            canvas.place(x=10, y=50,width=1250, height=190)  # Adjust the height accordingly
            scrollbar = tk.Scrollbar(self.proposal_frame, width=30,orient="vertical", command=canvas.yview)
            scrollbar.place(x=1250, y=50, height=190)  # Align the scrollbar with the canvas
            canvas.configure(yscrollcommand=scrollbar.set)

            self.proposal_list_frame = tk.Frame(canvas,height=0, width=1250)
            canvas.create_window((10, 10), window=self.proposal_list_frame, anchor='nw')
            
            List_frame_height=70
            row = 0  # Start from the first row below the headers        
            for proposals in self.proposal_list:
                tk.Label(self.proposal_list_frame, text=proposals[0], font=('Arial', 16), fg='black', bg='white').place(x=0, y=(row * 70))  # Adjust y position for each row
                tk.Label(self.proposal_list_frame, text=f"{proposals[1]}$", font=('Arial', 16), fg='black', bg='white').place(x=400, y=(row * 70))
                tk.Label(self.proposal_list_frame, text=proposals[2], font=('Arial', 16), fg='black', bg='white').place(x=700, y=(row * 70))
                tk.Label(self.proposal_list_frame, text=proposals[3], font=('Arial', 16), fg='black', bg='white').place(x=1000, y=(row * 70))
                row += 1  # Move to the next row
                self.proposal_list_frame.configure(height=row*List_frame_height)

            self.proposal_list_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        #Lower Screen//////////////////////////////////////////////////////
        self.lower_frame=tk.Frame(self.right_frame,bg='white',width=1400,height=430,bd=2,relief='groove')
        self.lower_frame.place(x=68,y=440)
        tk.Label(self.lower_frame,text="Browse Projects",font=("Arial",16,"bold"),fg="black",bg="white").place(x=10,y=10)

        self.browse_frame=tk.Frame(self.right_frame,bg='white',width=1380,height=370,bd= 1,relief='sunken')
        self.browse_frame.place(x=78,y=490)
        self.browse_project_list=db_connection.get_project_list()

        if len(self.browse_project_list)==0:
            tk.Label(self.browse_frame,text='No Current Projects Available',font=('Times New Roman',20),fg='grey',bg='white').place(x=400,y=70)
        else:    
            tk.Label(self.browse_frame,text='Title',font=('Arial',18,'bold'),fg='black',bg='white').place(x=100,y=10)
            tk.Label(self.browse_frame,text='Budget',font=('Arial',18,'bold'),fg='black',bg='white').place(x=350,y=10)
            tk.Label(self.browse_frame,text='Client',font=('Arial',18,'bold'),fg='black',bg='white').place(x=650,y=10)
            tk.Label(self.browse_frame,text='Deadline',font=('Arial',18,'bold'),fg='black',bg='white').place(x=900,y=10)

            canvas = tk.Canvas(self.browse_frame)
            canvas.place(x=10, y=50,width=1320, height=310)  
            scrollbar = tk.Scrollbar(self.browse_frame, width=30,orient="vertical", command=canvas.yview)
            scrollbar.place(x=1330, y=50, height=310)  
            canvas.configure(yscrollcommand=scrollbar.set)

            self.browse_projects_frame = tk.Frame(canvas,height=0, width=1320)
            canvas.create_window((10, 10), window=self.browse_projects_frame, anchor='nw')
            
            List_frame_height=70
            row = 0 
            for projects in self.browse_project_list:
                tk.Label(self.browse_projects_frame, text=projects[1], font=('Arial', 16), fg='black', bg='white').place(x=0, y=(row * 70))  # Adjust y position for each row
                tk.Label(self.browse_projects_frame, text=f"{projects[3]}$", font=('Arial', 16), fg='black', bg='white').place(x=340, y=(row * 70))
                tk.Label(self.browse_projects_frame, text=projects[5], font=('Arial', 16), fg='black', bg='white').place(x=640, y=(row * 70))
                tk.Label(self.browse_projects_frame, text=projects[4], font=('Arial', 16), fg='black', bg='white').place(x=890, y=(row * 70))
                tk.Button(self.browse_projects_frame,text='Create Proposal',font=('Arial',14),fg='gray',bg='white',activeforeground='black',activebackground='white',width=15,command=lambda p=projects: self.create_proposal(p[0], p[1], p[2], p[3], p[4], p[5])).place(x=1100,y=(row*70))
                row += 1  # Move to the next row
                self.browse_projects_frame.configure(height=row*List_frame_height)

            self.browse_projects_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))


    def update_proposal_label(self,event):
        # ========= 2. Canvas for Open Projects =========
        selected_proposal_type=self.proposal_var.get()
        if selected_proposal_type=='Pending':
            self.proposal_label.config(text=f"Pending - {self.proposals['Pending']}")
        if selected_proposal_type=='Accepted':
            self.proposal_label.config(text=f"Accepted - {self.proposals['Accepted']}")
        if selected_proposal_type=='Rejected':
            self.proposal_label.config(text=f"Rejected - {self.proposals['Rejected']}")

    def create_proposal(self,project_id,project_title,project_description,project_budget,project_deadline,client_name):
        self.proposal_window = tk.Toplevel(self.root)
        self.proposal_window.attributes('-topmost', True)
        self.proposal_window.focus_force()
        self.proposal_window.title("Create Proposal")
        self.proposal_window.geometry("1280x720")
        self.proposal_window.resizable(False,False)
        
        tk.Label(self.proposal_window, text="Project Title:", font=('Arial', 14,'bold')).place(x=20, y=30)
        tk.Label(self.proposal_window, text=project_title, font=('Arial', 14),bg='lightgray').place(x=160, y=30)
        tk.Label(self.proposal_window, text="Project Budget:", font=('Arial', 14,'bold')).place(x=600, y=30)
        tk.Label(self.proposal_window, text=(f"{project_budget}$"), font=('Arial', 14),bg='lightgray').place(x=770, y=30)
        tk.Label(self.proposal_window, text="Project Deadline:", font=('Arial', 14,'bold')).place(x=20, y=90)
        tk.Label(self.proposal_window, text=project_deadline, font=('Arial', 14),bg='lightgray').place(x=200, y=90)
        tk.Label(self.proposal_window, text="Clent Name:", font=('Arial', 14,'bold')).place(x=600, y=90)
        tk.Label(self.proposal_window, text=(f"{client_name}"), font=('Arial', 14),bg='lightgray').place(x=770, y=90)
        tk.Label(self.proposal_window, text="Project Description:", font=('Arial', 14,'bold')).place(x=20, y=150)
        tk.Label(self.proposal_window, text=project_description, font=('Times New Roman', 14),bg='lightgray',width=86,wraplength=1030,justify='left').place(x=230,y=150,height=250)
        tk.Label(self.proposal_window, text="Proposal Bid Amount:", font=('Arial', 14,'bold')).place(x=20, y=430)
        self.proposal_bid_entry = tk.Entry(self.proposal_window, font=('Arial', 12), width=20)
        self.proposal_bid_entry.place(x=250, y=430,height=40)
        tk.Label(self.proposal_window, text="Proposal Description:", font=('Arial', 14,'bold')).place(x=20, y=500)
        self.proposal_desc_entry = tk.Text(self.proposal_window, font=('Arial', 12), width=92)
        self.proposal_desc_entry.place(x=250, y=500,height=150)
        tk.Button(self.proposal_window, text="Send Proposal", font=('Arial', 14), bg="#0a295c", fg="white", command=lambda pid=project_id:self.send_proposal(pid)).place(x=600, y=660)

    def send_proposal(self,project_id):
        bid_amount=self.proposal_bid_entry.get()
        proposal_desc=self.proposal_desc_entry.get("1.0","end").strip()
        words=proposal_desc.split()
        if not bid_amount or not proposal_desc:
            return messagebox.showwarning("Error","Please fill all fields.", parent=self.proposal_window)
        elif (len(words)>150):
            return messagebox.showwarning("Error","Proposal Description limit is 150 words.")
        else:
            created_proposal=db_connection.submit_proposal(self.user_id,project_id,bid_amount,proposal_desc)
            if created_proposal==True:
                messagebox.showinfo('Success','Proposal sent Successfully!', parent=self.proposal_window)
                self.proposal_window.destroy() 
                self.view_proposals()  
            else:
                messagebox.showerror('Error','Something gone Wrong!', parent=self.proposal_window)


    def view_payments(self):
        self.init_right_frame()
        payment_status_frame = tk.Frame(self.right_frame, bd=2, relief='groove', highlightbackground='lightgray', highlightthickness=1, bg='white', width=1400, height=100)
        payment_status_frame.place(x=68, y=50)
    
        # Fetch payment stats for the freelancer
        payment_stats = db_connection.get_freelancer_payment_stats(self.user_id)
    
        self.payment_status_label = tk.Label(payment_status_frame, text=f"Pending Payments - {payment_stats['Pending']}", font=("Times New Roman", 16), bg='white')
        self.payment_status_label.place(x=10, y=30)
    
        self.payment_status_var = tk.StringVar(value='Pending Payments')
        self.payment_status_dropdown = ttk.Combobox(payment_status_frame, textvariable=self.payment_status_var, font=('Arial', 16), state='readonly', width=20)
        self.payment_status_dropdown['values'] = ['Pending Payments', 'Paid Payments']
        self.payment_status_dropdown.place(x=1050, y=25, height=50)
        self.payment_status_dropdown.bind("<<ComboboxSelected>>", self.update_payment_status_label)
    
        # Fetch the list of paid payments for the freelancer
        paid_payments = db_connection.get_paid_payments(self.user_id)
        
        tk.Label(self.right_frame, text="Manage Payments", font=('Arial', 18, 'bold'), fg='black', bg='white').place(x=68, y=200)
    
        if len(paid_payments) == 0:
            tk.Label(self.right_frame, text='No Paid Payments Found', font=('Times New Roman', 20), fg='grey', bg='white').place(x=550, y=450)
        else:
            payment_frame = tk.Frame(self.right_frame, bg='white', bd=2, relief='groove', width=1400, height=600)
            payment_frame.place(x=68, y=250)
    
            # Add headers for the paid payment list
            tk.Label(payment_frame, text='Project Title', font=('Arial', 18, 'bold'), fg='black', bg='white').place(x=50, y=10)
            tk.Label(payment_frame, text='Client Name', font=('Arial', 18, 'bold'), fg='black', bg='white').place(x=380, y=10)
            tk.Label(payment_frame, text='Paid Amount', font=('Arial', 18, 'bold'), fg='black', bg='white').place(x=630, y=10)
            tk.Label(payment_frame, text='Rating', font=('Arial', 18, 'bold'), fg='black', bg='white').place(x=950, y=10)
    
            canvas = tk.Canvas(payment_frame)
            canvas.place(x=50, y=60, width=1300, height=500)
            scrollbar = tk.Scrollbar(payment_frame, orient="vertical", command=canvas.yview)
            scrollbar.place(x=1320, y=60, height=500)
            canvas.configure(yscrollcommand=scrollbar.set)
    
            # Create a frame to hold the payment rows and place it on the canvas
            payment_list_frame = tk.Frame(canvas, height=0, width=1240)
            canvas.create_window((10, 10), window=payment_list_frame, anchor='nw')
    
            List_frame_height = 70
            row = 0  
            for payment in paid_payments:
                tk.Label(payment_list_frame, text=payment['Project_Title'], font=('Arial', 16), fg='black', bg='white').place(x=0, y=(row * 70))  # Project Title
                tk.Label(payment_list_frame, text=payment['Client_Name'], font=('Arial', 16), fg='black', bg='white').place(x=340, y=(row * 70))  # Client Name
                tk.Label(payment_list_frame, text=f"${payment['Amount']}", font=('Arial', 16), fg='black', bg='white').place(x=600, y=(row * 70)) 
                payment['Rating']= '★' * payment['Rating'] + '☆' * (5 - payment['Rating'])
                tk.Label(payment_list_frame, text=payment['Rating'], font=('Arial', 16), fg='black', bg='white').place(x=870, y=(row * 70))  # Rating
                tk.Button(payment_list_frame, text="View Details", font=('Arial', 14), bg="#0a295c", fg="white", 
                    command=lambda ptitle=payment['Project_Title'],cname=payment['Client_Name'],amount=payment['Amount'],method=payment['Method'],
                    rating=payment['Rating'],cmnt=payment['Comment'],pdate=payment['Payment_Date']: self.view_payment_details(ptitle,cname,amount,method,rating,cmnt,pdate)).place(x=1100, y=(row * 70))  
        
                row += 1  # Move to the next row
                payment_list_frame.configure(height=row * List_frame_height)
    
            # Update the scrolling region for the canvas
            payment_list_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

    def update_payment_status_label(self, event):
        selected_payment_status = self.payment_status_var.get()
        payment_stats = db_connection.get_freelancer_payment_stats(self.user_id)
    
        if selected_payment_status == "Pending Payments":
            self.payment_status_label.config(text=f"Pending Payments - {payment_stats['Pending']}")
        if selected_payment_status == "Paid Payments":
            self.payment_status_label.config(text=f"Paid Payments - {payment_stats['Paid']}")

    def view_payment_details(self,Title,Client,Amount,Method,Rating,comment,date):
        self.payments_window = tk.Toplevel(self.root)
        self.payments_window.attributes('-topmost', True)
        self.payments_window.focus_force()
        self.payments_window.title("Payments Details")
        self.payments_window.geometry("1280x550")
        self.payments_window.resizable(False,False)
        
        tk.Label(self.payments_window, text="Project Title:", font=('Arial', 14,'bold')).place(x=20, y=30)
        tk.Label(self.payments_window, text=Title, font=('Arial', 14),bg='lightgray').place(x=160, y=30)
        tk.Label(self.payments_window, text="Clent Name:", font=('Arial', 14,'bold')).place(x=600, y=30)
        tk.Label(self.payments_window, text=(f"{Client}"), font=('Arial', 14),bg='lightgray').place(x=740, y=30)
        tk.Label(self.payments_window, text="Paid Amount:", font=('Arial', 14,'bold')).place(x=20, y=90)
        tk.Label(self.payments_window, text=(f"{Amount}$"), font=('Arial', 14),bg='lightgray').place(x=170, y=90)
        tk.Label(self.payments_window, text="Payment Method:", font=('Arial', 14,'bold')).place(x=600, y=90)
        tk.Label(self.payments_window, text=Method, font=('Arial', 14),bg='lightgray').place(x=790, y=90)
        tk.Label(self.payments_window, text="Payment Date:", font=('Arial', 14,'bold')).place(x=20, y=150)
        tk.Label(self.payments_window, text=date, font=('Arial', 14),bg='lightgray').place(x=180, y=150)
        tk.Label(self.payments_window, text="Project Rating:", font=('Arial', 14,'bold')).place(x=600, y=150)
        tk.Label(self.payments_window, text=Rating, font=('Arial', 14),bg='lightgray').place(x=770, y=150)
        tk.Label(self.payments_window, text="Comment:", font=('Arial', 14,'bold')).place(x=20, y=210)
        tk.Label(self.payments_window, text=comment, font=('Times New Roman', 14),bg='lightgray',width=86,wraplength=1030,justify='left').place(x=150,y=210,height=250)
        tk.Button(self.payments_window, text="Close", font=('Arial', 16), bg="#0a295c", fg="white", command=self.payments_window.destroy).place(x=600, y=470)


    def view_messages(self):
        print("Messages screen opened")

    def edit_profile(self):
        self.init_right_frame()
        self.user_data=db_connection.get_freelancer_data(self.user_id)
        tk.Label(self.right_frame, text="Profile Details", font=('Arial', 14,'bold'),bg='white',fg='black').place(x=20, y=10)
        tk.Label(self.right_frame, text=" ", bg='lightgray',font=('Arial',18,'bold'),width=83).place(x=20, y=50,height=2)
        tk.Label(self.right_frame, text="Full Name", font=('Arial', 14,'bold'),bg='white',fg='gray').place(x=20, y=80)
        self.name_entry=tk.Entry(self.right_frame, font=('Arial', 14),bg='white',fg='gray',width=30,border=2,relief='groove',justify='left')
        self.name_entry.insert(0,self.user_data[1])
        self.name_entry.place(x=200, y=80)
        tk.Label(self.right_frame, text="User Email", font=('Arial', 14,'bold'),bg='white',fg='gray').place(x=800, y=80)
        self.email_entry=tk.Entry(self.right_frame, font=('Arial', 14),bg='white',fg='gray',width=30,border=2,relief='groove',justify='left')
        self.email_entry.insert(0,self.user_data[2])
        self.email_entry.place(x=1000, y=80)
        tk.Label(self.right_frame, text="Phone No.", font=('Arial', 14,'bold'),bg='white',fg='gray').place(x=20, y=140)
        self.phone_entry=tk.Entry(self.right_frame, font=('Arial', 14),bg='white',fg='gray',width=30,border=2,relief='groove',justify='left')
        self.phone_entry.insert(0,self.user_data[3])
        self.phone_entry.place(x=200, y=140)
        tk.Label(self.right_frame, text="Current Password", font=('Arial', 14,'bold'),bg='white',fg='gray').place(x=800, y=140)
        self.current_entry=tk.Entry(self.right_frame, font=('Arial', 14),show="x",bg='white',fg='gray',width=30,border=2,relief='groove',justify='left')
        self.current_entry.place(x=1000, y=140)
        tk.Label(self.right_frame, text="New Password", font=('Arial', 14,'bold'),bg='white',fg='gray').place(x=20, y=200)
        self.new_entry=tk.Entry(self.right_frame, font=('Arial', 14),show="x",bg='white',fg='gray',width=30,border=2,relief='groove',justify='left')
        self.new_entry.place(x=200, y=200)
        tk.Label(self.right_frame, text="Current Password", font=('Arial', 14,'bold'),bg='white',fg='gray').place(x=800, y=200)
        self.confirm_entry=tk.Entry(self.right_frame, font=('Arial', 14),show="x",bg='white',fg='gray',width=30,border=2,relief='groove',justify='left')
        self.confirm_entry.place(x=1000, y=200)
        tk.Label(self.right_frame, text="Description", font=('Arial', 14,'bold'),bg='white',fg='gray').place(x=20, y=260)
        self.desc_entry=tk.Text(self.right_frame, font=('Arial', 14),bg='white',fg='gray',width=97,border=2,relief='groove',wrap='word')
        self.desc_entry.insert(1.0,self.user_data[6])
        self.desc_entry.place(x=200, y=260,height=200)
        tk.Button(self.right_frame, text="Save Changes", font=('Arial Rounded MT', 12), bg="#1dbf73", fg="white", command= lambda:self.save_changes(self.user_id)).place(x=1230, y=480)
        tk.Label(self.right_frame, text=" ", bg='lightgray',font=('Arial',18,'bold'),width=83).place(x=20, y=550,height=2)
        tk.Label(self.right_frame, text="Account Deactivation", font=('Arial', 14,'bold'),bg='white',fg='gray').place(x=20, y=590)
        tk.Label(self.right_frame, text=" What happens when you deactivate your account?", font=('Arial', 12,'bold'),bg='white',fg='gray').place(x=600, y=590)
        tk.Label(self.right_frame, text="\n•  Your profile won't be shown on Freelance anymore.\n•  Can't deactive account when you have Active orders.\n•  Your all open projects will be closed.",justify='left', font=('Arial', 12),bg='white',fg='gray').place(x=600, y=620)
        tk.Label(self.right_frame, text="I'm leaving because...", font=('Arial', 10,'bold'),bg='white',fg='gray').place(x=20, y=750)

        self.dropdown_var = tk.StringVar()
        options = ['I have another Freelance account', 'No getting enough orders', 'It is complicated to use', 'Other']
        # Creating a combobox dropdown widget
        self.dropdown = ttk.Combobox(self.right_frame, values=options,textvariable=self.dropdown_var, width=40,font=('Arial',14),foreground='gray',state='readonly')
        self.dropdown.set('Choose a reason') 
        self.dropdown.place(x=600,y=750)

        tk.Button(self.right_frame, text="Deactivate", font=('Arial Rounded MT', 12),width=13, bg="#1dbf73", fg="white", command=lambda:self.deactivate_account(self.user_id)).place(x=1230, y=810)
       

    def save_changes(self,user_id):
        name=self.name_entry.get()    
        email=self.email_entry.get()
        phone=self.phone_entry.get()
        desc=self.desc_entry.get(1.0,"end").strip()
        words=desc.strip()
        current_pass=self.current_entry.get()
        new_pass=self.new_entry.get()
        confirm_pass=self.confirm_entry.get()
        if not name or not email or not phone:
            return messagebox.showerror("Error","Missing Required Fields!")
        if len(words)>150:
            return messagebox.showerror("Error","Description limits exceeds 150 words!")
        if (current_pass and not new_pass) or (new_pass and not current_pass):
            return messagebox.showerror("Error", "Both Current and New Password must be entered!")
        
        if (new_pass and current_pass) and current_pass!=self.user_data[5]:
            return messagebox.showerror("Error", "Current Password is incorrect!")
        if confirm_pass and not current_pass and not new_pass:
            return messagebox.showerror("Error","Current and New Passwords are missing!")
        if new_pass and confirm_pass and current_pass:
            if new_pass == self.user_data[5]:
                return messagebox.showerror("Error", "New Password must be different from Current Password!")
            if new_pass != confirm_pass:
                return messagebox.showerror("Error", "New Password and Confirm Password must match!")
            if current_pass != self.user_data[5]:
                return messagebox.showerror("Error", "Current Password is incorrect!")
        if new_pass and current_pass:
            return messagebox.showerror("Error","Confirm Password is not entered")
        else:
            if new_pass and confirm_pass and current_pass:
                update_details=db_connection.update_details(name,email,phone,desc,new_pass,self.user_id)
            else:
                new_pass=self.user_data[5]
                update_details=db_connection.update_details(name,email,phone,desc,new_pass,self.user_id)
            if update_details=='email exist':
                return messagebox.showerror("Error","Email already registered!")
            else:
                messagebox.showinfo("Info","Updated Successfully!")
                self.edit_profile()


    def deactivate_account(self,user_id):
        confirm=messagebox.askyesno("Info","Do you really want to deactivate account?")
        if confirm:
            active_projects=db_connection.check_active_projects(self.user_id)
            if active_projects=='Active':
                return messagebox.showinfo("Info","Account Cannot Deactivated due to Active Projects!")
            if active_projects:
                messagebox.showinfo("Info","Account Deactivated Successfully!")
                self.root.destroy()
            else:
                messagebox.showerror("Error","Something gone wrong!")
    
    def view_messages(self):
        self.init_right_frame()
        self.messages_left_frame=tk.Frame(self.right_frame,bg='#2c2c2c',width=350,height=960,bd=2,relief='groove')
        self.messages_left_frame.place(x=0,y=0)
        all_users=db_connection.fetch_all_users(self.user_id)
        if all_users==[]:
            tk.Label(self.messages_left_frame,text="No Current Users",font=('Arial',18,'bold'),fg='white',bg='#2c2c2c').place(x=450,y=150)
        else:
            tk.Label(self.messages_left_frame,text="Chats",font=('Arial',18,'bold'),fg='white',bg='#2c2c2c').place(x=10,y=10)
            canvas = tk.Canvas(self.messages_left_frame)
            canvas.place(x=10, y=50,width=320, height=910)  
            scrollbar = tk.Scrollbar(self.messages_left_frame, orient="vertical", command=canvas.yview)
            scrollbar.place(x=320, y=50, height=910)  
            canvas.configure(yscrollcommand=scrollbar.set)

            users_list_frame = tk.Frame(canvas,height=0, width=320,bg='#2c2c2c')
            canvas.create_window((0, 0), window=users_list_frame, anchor='nw')
            
            List_frame_height=77
            row = 0  
            for user in all_users:
                btn=tk.Button(users_list_frame,text=f"{user[1]}\n{user[2]}",font=("Arial",12),fg='white',bg='#2c2c2c',activebackground='#2c2c2c',activeforeground='white',bd=3,relief='ridge',justify='left',anchor='w',width=26,command=lambda uid=user[0],uname=user[1]:self.show_messages(uid,uname))
                btn.place(x=2,y=(row*73))
                row+=1
                users_list_frame.configure(height=row*List_frame_height)
            
            users_list_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        self.messages_details_frame=tk.Frame(self.right_frame,bg='#2c2c2c',width=1186,height=960,bd=2,relief='groove')
        self.messages_details_frame.place(x=350,y=0)
        tk.Label(self.messages_details_frame,text="Chats for Freelance Management System",font=('Arial',14),fg='white',bg='#2c2c2c').place(x=400,y=360)
        tk.Label(self.messages_details_frame,text="You can Send Messages to Users\nYou can receive messages from Users",font=('Arial',10),fg='#9e9e9e',bg='#2c2c2c').place(x=450,y=400)
        tk.Label(self.messages_details_frame,text="🔓 Your messages are not End-to-end encrypted",font=('Arial',10),fg='#9e9e9e',bg='#2c2c2c').place(x=450,y=800)
    
    def init_messages_frame(self):
        self.messages_details_frame=tk.Frame(self.right_frame,bg='#2c2c2c',width=1186,height=960,bd=2,relief='groove')
        self.messages_details_frame.place(x=350,y=0)

    def show_messages(self,user_id,user_name):
        self.init_messages_frame()
        tk.Label(self.messages_details_frame,text=f"    {user_name}",font=('Arial',14),fg='white',bg='#2c2c2c',width=1000,anchor='w').place(x=0,y=0,height=50)
        self.message_showing_frame=tk.Frame(self.messages_details_frame,bg='#454343',width=1186,height=750)
        self.message_showing_frame.place(x=0,y=50)

        canvas = tk.Canvas(self.message_showing_frame,bg='#454343')
        canvas.place(x=0, y=0,width=1166, height=750)  
        scrollbar = tk.Scrollbar(self.message_showing_frame, orient="vertical", command=canvas.yview)
        scrollbar.place(x=1166, y=0, height=750,width=20)  
        canvas.configure(yscrollcommand=scrollbar.set)
        message_list_frame = tk.Frame(canvas,height=0, width=1160,bg='#454343')
        canvas.create_window((0, 0), window=message_list_frame, anchor='nw')
        
        messages=db_connection.fetch_user_messages(self.user_id,user_id)
        
        row = 1
        for message in messages:
            is_sender = message['Sender_ID'] == self.user_id
            text = message['Text']
            dt = message['DateTime']
            formatted_dt = dt.strftime("%d-%m-%Y %I:%M %p")
            combined_text = f"{text}\n\t\t\t{formatted_dt}"
            
            label = tk.Label(message_list_frame,
                            text=combined_text,
                            font=("Times New Roman", 12),
                            bg='#005c4b',
                            fg='white',
                            justify='left',
                            anchor='w',
                            wraplength=400,
                            padx=10,
                            pady=5)

            label.update_idletasks()
            label_width = label.winfo_reqwidth()
            label_height = label.winfo_reqheight()

            if not is_sender:
                x = 20 
            else:
                right_margin = 1150
                x = right_margin - label_width  

            label.place(x=x, y=row)
            row += label_height + 10
            message_list_frame.config(height=row+70)


        message_list_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


        self.message_write_frame=tk.Frame(self.messages_details_frame,bg='#2c2c2c',width=1186,height=80,bd=1,relief='solid')
        self.message_write_frame.place(x=0,y=800)
        
        self.message_entry=tk.Entry(self.message_write_frame,font=('Arial', 14),insertbackground='white',bg='#2c2c2c',fg='white',width=80,border=1,relief='sunken',justify='left')
        self.message_entry.place(x=20, y=20,height=45)
        self.send_button=tk.Button(self.message_write_frame,text=f"Send",width=10,font=("Arial",14),fg='white',bg='lightgray',bd=2,relief='groove',anchor='center',command=lambda sid=self.user_id,rid=user_id:self.send_message(sid,rid),state='disabled')
        self.send_button.place(x=1000,y=20)
        self.message_entry.bind("<KeyRelease>", self.check_message)

    def check_message(self, event=None):
        # Get the message text from the entry widget
        message_text = self.message_entry.get().strip()

        # Enable or disable the send button based on whether there is text
        if message_text:
            self.send_button.config(state="normal",bg='#005c4b',activebackground='#005c4b',activeforeground='white')
        else:
            self.send_button.config(state="disabled")

    def send_message(self,sender_id,receiver_id):
        message_content=self.message_entry.get().strip()
        if message_content:
            send_message=db_connection.send_message(sender_id,receiver_id,message_content)
            if send_message:
                self.message_entry.delete(0, tk.END)
                self.send_button.config(state="disabled")
            else:
                messagebox.showerror("Error","something Gone Wrong!")

    def logout(self):
        confirm=messagebox.askyesno("Warning","Do you really want to Logout?")
        if confirm:
            self.root.destroy()
            messagebox.showinfo("Info","Logout Successful!")
            import login_screen
            root = tk.Tk()
            login_screen.LoginScreen(root)
            root.mainloop()
