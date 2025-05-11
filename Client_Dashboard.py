import tkinter as tk
from tkinter import ttk ,PhotoImage,messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import graphs,db_connection,Freelance_Dashboards


class ClientScreen:
    def __init__(self, root, user_id, username,user_role):
        self.root = root
        self.user_id = user_id
        self.user_role=user_role
        self.icon = PhotoImage(file='Logo.png')
        self.root.title('Client Dashboard - Freelance Project Management System')
        self.root.iconphoto(True, self.icon)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.state('zoomed')
        self.root.configure(bg="white")

        # Fetch user name and stats
        self.username = username
        self.stats = db_connection.get_client_projects(user_id)

        self.setup_ui()

    def setup_ui(self):
        # Topbar setup
        self.top_bar = tk.Frame(self.root, bg='#0a295c', width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight()//9)
        self.top_bar.propagate(False)
        self.top_bar.place(x=0, y=0)
        logo = PhotoImage(file='CLogo.png').subsample(3, 3)
        logo_label = tk.Label(self.top_bar, image=logo, bg='#0a295c')
        logo_label.place(x=50, y=25)
        logo_label.image = logo
        
        # Welcome text
        welcome_label = tk.Label(self.top_bar, text=f"Welcome!\n {self.username}", bg="#0a295c",font=("Times New Roman", 18, "bold"), fg="white")
        welcome_label.place(x=200, y=20)
        client_label = tk.Label(self.top_bar, text="Client Dashboard", bg="#0a295c",
                                font=("Sacrifice Demo", 40, "bold"), fg="white")
        client_label.place(x=700, y=15)
        switch_button=tk.Button(self.top_bar, text="Switch to Freelance ", font=('Arial', 14), fg='#0a295c', bg='lightgray', activebackground='#1553b6', width=20, command=lambda:self.switch_freelance(self.user_id,self.username,self.user_role))
        switch_button.place(x=1600, y=35)

        # Sidebar setup
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
            ("📈 Stats", self.view_stats),
            ("🚪 Logout", self.logout)
        ]
        btn_space = 0
        for text, command in buttons:
            btn = tk.Button(sidebar, text=text, font=("Arial", 14), fg='white', bg='#133a7c', activebackground='#1553b6',border=1 ,relief='groove',anchor='center', width=20, command=command)
            btn.place(x=0, y=40 + btn_space, height=70)
            btn_space += 100

        self.view_projects()

    def init__right_frame(self):
        self.right_frame = tk.Frame(self.root, bg='white', width=1536, height=960)
        self.right_frame.place(x=384, y=120)
        self.right_frame.grid_propagate(False)
    
    def switch_freelance(self,user_id,user_name,user_role):
        if user_role==3:
            confirm=messagebox.askyesno("Info","Do you want to switch to Freelance Dashboard?")
            if confirm:
                self.root.destroy()
                Freelance=tk.Tk()
                Freelance_Dashboards.FreelanceScreen(Freelance,user_id,user_name,user_role)
                Freelance.mainloop()
        else:
            import login_screen
            confirm=messagebox.askyesno("Info","You don't have Freelance Profile.Do You want to setup?")
            if confirm:
                self.root.destroy()
                Profile_root=tk.Tk()
                login_screen.Freelance_profile(Profile_root,user_id,user_name,user_role)
                Profile_root.mainloop()
    
    def view_projects(self):
        self.init__right_frame()  # Clears the frame and prepares for the new content
        #Open Projects Frame
        self.open_projects_frame=tk.Frame(self.right_frame,bg='white',width=1400,height=400,bd=2,relief='groove')
        self.open_projects_frame.place(x=68,y=20)
        #Active Projects Frame
        self.active_projects_frame=tk.Frame(self.right_frame,bg='white',width=1400,height=400,bd=2,relief='groove')
        self.active_projects_frame.place(x=68,y=470)

        tk.Label(self.open_projects_frame, text="Open Projects", font=('Arial', 18, 'bold'), fg='black', bg='white').place(x=10, y=10)
        tk.Label(self.active_projects_frame, text="Active/Completed Projects", font=('Arial', 18, 'bold'), fg='black', bg='white').place(x=10, y=10)
        # Add 'Create New Project' button
        create_project_btn = tk.Button(self.open_projects_frame, text="➕ Create a New Project", font=('Arial', 14), fg='white', bg='#0a295c', activebackground='#1553b6', width=20, command=self.create_project)
        create_project_btn.place(x=1100, y=10)

        # Fetch the client's current projects
        client_projects = db_connection.get_client_projects(self.user_id)
        open_projects=client_projects['open_projects']
        active_projects=client_projects['active_projects']
        completed_projects=client_projects['completed_projects']
        # Display client's projects
        if len(open_projects) == 0:
            tk.Label(self.open_projects_frame, text='No Currently Open Projects\n Start by creating a project', font=('Times New Roman', 20), fg='grey', bg='white').place(x=550, y=150)
        else:
            projects_frame = tk.Frame(self.open_projects_frame, bg='white',bd=1,relief='groove', width=1100, height=310)
            projects_frame.place(x=150, y=70)
            tk.Label(projects_frame,text='Title',font=('Arial',18,'bold'),fg='black',bg='white').place(x=70,y=10)
            tk.Label(projects_frame,text='Budget',font=('Arial',18,'bold'),fg='black',bg='white').place(x=300,y=10)
            tk.Label(projects_frame,text='Deadline',font=('Arial',18,'bold'),fg='black',bg='white').place(x=520,y=10)
            tk.Label(projects_frame,text='Status',font=('Arial',18,'bold'),fg='black',bg='white').place(x=730,y=10)
        
            canvas = tk.Canvas(projects_frame)
            canvas.place(x=10, y=60,width=1000, height=230)  # Adjust the height accordingly
            scrollbar = tk.Scrollbar(projects_frame, width=30,orient="vertical", command=canvas.yview)
            scrollbar.place(x=1020, y=60, height=230)  # Align the scrollbar with the canvas
            canvas.configure(yscrollcommand=scrollbar.set)

            # Create a frame to hold the project rows and place it on the canvas
            project_list_frame = tk.Frame(canvas,height=0, width=1000)
            canvas.create_window((10, 10), window=project_list_frame, anchor='nw')
            
            List_frame_height=70
            row = 0  

            for project in open_projects:
                tk.Label(project_list_frame, text=project[1], font=('Arial', 16), fg='black', bg='white').place(x=0, y=(row * 70))  
                tk.Label(project_list_frame, text=f"{project[2]}$", font=('Arial', 16), fg='black', bg='white').place(x=290, y=(row * 70))
                tk.Label(project_list_frame, text=project[3], font=('Arial', 16), fg='black', bg='white').place(x=510, y=(row * 70))
                if project[4]==1:
                    text='Open'
                elif project[4]==4:
                    text='Closed'
                tk.Label(project_list_frame, text=text, font=('Arial', 16), fg='black', bg='white').place(x=730, y=(row * 70))
                tk.Button(project_list_frame,text='Edit',font=('Arial',14),fg='gray',bg='white',activeforeground='black',activebackground='white',width=10,command=lambda pid=project[0]:self.edit_projects(pid)).place(x=840,y=(row*70))
                row += 1  # Move to the next row
                project_list_frame.configure(height=row*List_frame_height)
        
            # Update the scrolling region for the canvas
            project_list_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
        #active/completed projects
        if len(active_projects)==0 and len(completed_projects) == 0:
            tk.Label(self.active_projects_frame, text='No Currently Active/Completed Projects', font=('Times New Roman', 20), fg='grey', bg='white').place(x=450, y=170)
        else:
            projects_frame = tk.Frame(self.active_projects_frame, bg='white',bd=2,relief='groove', width=1300, height=310)
            projects_frame.place(x=50, y=70)
            tk.Label(projects_frame,text='Title',font=('Arial',18,'bold'),fg='black',bg='white').place(x=120,y=10)
            tk.Label(projects_frame,text='Budget',font=('Arial',18,'bold'),fg='black',bg='white').place(x=350,y=10)
            tk.Label(projects_frame,text='Deadline',font=('Arial',18,'bold'),fg='black',bg='white').place(x=570,y=10)
            tk.Label(projects_frame,text='Freelancer',font=('Arial',18,'bold'),fg='black',bg='white').place(x=780,y=10)
            tk.Label(projects_frame,text='Status',font=('Arial',18,'bold'),fg='black',bg='white').place(x=1050,y=10)
        
            canvas = tk.Canvas(projects_frame)
            canvas.place(x=10, y=60,width=1200, height=230)  # Adjust the height accordingly
            scrollbar = tk.Scrollbar(projects_frame, width=30,orient="vertical", command=canvas.yview)
            scrollbar.place(x=1220, y=60, height=230)  # Align the scrollbar with the canvas
            canvas.configure(yscrollcommand=scrollbar.set)

            # Create a frame to hold the project rows and place it on the canvas
            project_list_frame = tk.Frame(canvas,height=0, width=1300)
            canvas.create_window((10, 10), window=project_list_frame, anchor='nw')
            
            List_frame_height=70
            row = 0  # Start from the first row below the headers
            for project in active_projects:
                tk.Label(project_list_frame, text=project[0], font=('Arial', 16), fg='black', bg='white').place(x=0, y=(row * 70))  # Adjust y position for each row
                tk.Label(project_list_frame, text=f"{project[1]}$", font=('Arial', 16), fg='black', bg='white').place(x=340, y=(row * 70))
                tk.Label(project_list_frame, text=project[2], font=('Arial', 16), fg='black', bg='white').place(x=560, y=(row * 70))
                tk.Label(project_list_frame, text=project[3], font=('Arial', 16), fg='black', bg='white').place(x=770, y=(row * 70))
                tk.Label(project_list_frame, text=project[4], font=('Arial', 16), fg='green', bg='white').place(x=1050, y=(row * 70))
                row += 1  # Move to the next row
                project_list_frame.configure(height=row*List_frame_height)
            for project in completed_projects:
                tk.Label(project_list_frame, text=project[0], font=('Arial', 16), fg='black', bg='white').place(x=0, y=(row * 70))  # Adjust y position for each row
                tk.Label(project_list_frame, text=f"{project[1]}$", font=('Arial', 16), fg='black', bg='white').place(x=340, y=(row * 70))
                tk.Label(project_list_frame, text=project[2], font=('Arial', 16), fg='black', bg='white').place(x=560, y=(row * 70))
                tk.Label(project_list_frame, text=project[3], font=('Arial', 16), fg='black', bg='white').place(x=770, y=(row * 70))
                tk.Label(project_list_frame, text=project[4], font=('Arial', 16), fg='gray', bg='white').place(x=1050, y=(row * 70))
                row += 1  # Move to the next row
                project_list_frame.configure(height=row*List_frame_height)
        
            # Update the scrolling region for the canvas
            project_list_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

    def create_project(self):
        # Create a new window to handle project details
        self.project_window = tk.Toplevel(self.root)
        self.project_window.attributes('-topmost', True)
        self.project_window.focus_force()
        self.project_window.title("Create New Project")
        self.project_window.geometry("500x500")
        self.project_window.resizable(False,False)

        tk.Label(self.project_window, text="Project Title:", font=('Arial', 14)).place(x=20, y=20)
        self.project_title_entry = tk.Entry(self.project_window, font=('Arial', 14), width=25)
        self.project_title_entry.place(x=150, y=20,height=40)
        
        tk.Label(self.project_window, text="Project\nDescription:", font=('Arial', 14)).place(x=20, y=100)
        self.project_desc_entry = tk.Text(self.project_window, font=('Arial', 12), width=30, height=5)
        self.project_desc_entry.place(x=150, y=80)
        tk.Label(self.project_window,text='Project Budget:',font=('Arial',14),fg='black').place(x=20,y=210)
        self.project_budget_entry=tk.Entry(self.project_window, font=('Arial', 12), width=20)
        self.project_budget_entry.place(x=180,y=210,height=40)
        tk.Label(self.project_window,text="Project Deadline:",font=('Arial',14),fg='black').place(x=20,y=270)
        self.project_deadline_entry=tk.Entry(self.project_window, font=('Arial', 12), width=19)
        self.project_deadline_entry.place(x=195,y=270,height=40)
        tk.Label(self.project_window,text="Format(YYYY-MM-DD):",font=('Arial',10),fg='gray').place(x=20,y=295)
        tk.Label(self.project_window,text="Project Status:",font=('Arial',14),fg='black').place(x=20,y=330) 
        self.status_var=tk.StringVar(value='Active')
        self.status_dropdown=ttk.Combobox(self.project_window,textvariable=self.status_var,font=('Arial',14),state='readonly',width=10)
        self.status_dropdown['values']=['Active','Closed']
        self.status_dropdown.place(x=180,y=330)
        tk.Button(self.project_window, text="Submit", font=('Arial', 14), bg="#0a295c", fg="white", command=self.submit_project).place(x=200, y=420)

    def submit_project(self):
        Project_title=self.project_title_entry.get()
        Project_desc=self.project_desc_entry.get("1.0","end").strip()
        words = Project_desc.split()
        Project_budget=self.project_budget_entry.get()
        Project_deadline=self.project_deadline_entry.get()
        Project_status=self.status_var.get()

        if not Project_title or not Project_desc or not Project_budget or not Project_deadline:
            messagebox.showerror('Error','Please fill all fields!')
            return
        elif len(words) > 150:
            messagebox.showwarning("Limit Exceeded", "Please limit the description to 150 words.")
            return
        else:
            if Project_status=='Active':
                status_value=1
            elif Project_status=='Closed':
                status_value=4
            success=db_connection.add_project(self.user_id,Project_title,Project_desc,Project_budget,Project_deadline,status_value)
            if success:
                messagebox.showinfo('Success','Project Added Successfully!')
                self.project_window.destroy()  
                self.view_projects()
            else:
                messagebox.showerror('Error','Something gone Wrong!')

    def edit_projects(self,Project_ID):
        self.Project_ID=Project_ID
        self.project_window = tk.Toplevel(self.root)
        self.project_window.attributes('-topmost', True)
        self.project_window.focus_force()
        self.project_window.title("Edit Project")
        self.project_window.geometry("500x500")
        self.project_window.resizable(False,False)

        tk.Label(self.project_window, text="Project Title:", font=('Arial', 14)).place(x=20, y=20)
        self.project_title_entry = tk.Entry(self.project_window, font=('Arial', 14), width=25)
        self.project_title_entry.place(x=150, y=20,height=40)
        
        tk.Label(self.project_window, text="Project\nDescription:", font=('Arial', 14)).place(x=20, y=100)
        self.project_desc_entry = tk.Text(self.project_window, font=('Arial', 12), width=30, height=5)
        self.project_desc_entry.place(x=150, y=80)
        tk.Label(self.project_window,text='Project Budget:',font=('Arial',14),fg='black').place(x=20,y=210)
        self.project_budget_entry=tk.Entry(self.project_window, font=('Arial', 12), width=20)
        self.project_budget_entry.place(x=180,y=210,height=40)
        tk.Label(self.project_window,text="Project Deadline:",font=('Arial',14),fg='black').place(x=20,y=270)
        self.project_deadline_entry=tk.Entry(self.project_window, font=('Arial', 12), width=19)
        self.project_deadline_entry.place(x=195,y=270,height=40)
        tk.Label(self.project_window,text="Format(YYYY-MM-DD):",font=('Arial',10),fg='gray').place(x=20,y=295)
        tk.Label(self.project_window,text="Project Status:",font=('Arial',14),fg='black').place(x=20,y=330) 
        self.status_var=tk.StringVar(value='Active')
        self.status_dropdown=ttk.Combobox(self.project_window,textvariable=self.status_var,font=('Arial',14),state='readonly',width=10)
        self.status_dropdown['values']=['Active','Closed']
        self.status_dropdown.place(x=180,y=330)
        tk.Button(self.project_window, text="Save", font=('Arial', 14), bg="#0a295c", fg="white", command=lambda pid=self.Project_ID:self.save_project(pid)).place(x=200, y=420)
    
    def save_project(self,Project_ID):
        self.Project_ID=Project_ID
        Project_title=self.project_title_entry.get()
        Project_desc=self.project_desc_entry.get("1.0","end").strip()
        words=Project_desc.split()
        Project_budget=self.project_budget_entry.get()
        Project_deadline=self.project_deadline_entry.get()
        Project_status=self.status_var.get()
        if len(words) > 150:
            messagebox.showwarning("Limit Exceeded", "Please limit the description to 150 words.")
            return

        if Project_status=='Active':
            status_value=1
        elif Project_status=='Closed':                
            status_value=4

        project_created=db_connection.edit_project(self.Project_ID,self.user_id,Project_title,Project_desc,Project_budget,Project_deadline,status_value)
        if project_created == True:
            messagebox.showinfo('Success','Project Updated Successfully!')
            self.project_window.destroy()  # Close the create project window
            self.view_projects()  # Refresh the My Projects screen
        else:
            messagebox.showerror('Error','Something gone Wrong!')

    def view_stats(self):
        self.init__right_frame()
        self.right_frame.config(bg="#0b0f3c")
        bar_chart_frame=tk.Frame(self.right_frame,width=720,height=400,bg="#0b0f3c") 
        bar_chart_frame.place(x=15,y=10)

        fig1=graphs.get_top_freelancers()

        canvas = FigureCanvasTkAgg(fig1, master=bar_chart_frame)
        canvas.draw()   
        toolbar = NavigationToolbar2Tk(canvas, bar_chart_frame)
        toolbar.update()
        
        for child in toolbar.winfo_children():
            child.config( bd=2)
            if isinstance(child, tk.Button):
                child.config(fg='white', activebackground='black', activeforeground='white', relief='groove')
        toolbar.place(x=0,y=360)
        canvas.get_tk_widget().place(x=0,y=0)

        #Line Chart
        line_chart_frame=tk.Frame(self.right_frame,width=770,height=400,bg="#0b0f3c") 
        line_chart_frame.place(x=750,y=10)

        fig3=graphs.plot_payments(self.user_id)
        if fig3=="Not Found!":
            tk.Label(line_chart_frame,text="No Payments Found",font=("Times New Roman",24),fg="lightgray",bg='#0b0f3c').place(x=250,y=170)
        else:
            canvas = FigureCanvasTkAgg(fig3, master=line_chart_frame)
            canvas.draw()   
            toolbar = NavigationToolbar2Tk(canvas, line_chart_frame)
            toolbar.update()
        
            for child in toolbar.winfo_children():
                child.config( bd=2)
                if isinstance(child, tk.Button):
                    child.config(fg='white', activebackground='black', activeforeground='white', relief='groove')
            toolbar.place(x=0,y=360)
            canvas.get_tk_widget().place(x=0,y=0)

        #Pie Chart
        pie_chart_frame=tk.Frame(self.right_frame,width=485,height=450,bg="#0b0f3c")
        pie_chart_frame.place(x=10,y=420)

        fig2=graphs.get_top_skills()
        canvas = FigureCanvasTkAgg(fig2, master=pie_chart_frame)
        canvas.draw() 
        
        for child in toolbar.winfo_children():
            child.config( bd=2)
            if isinstance(child, tk.Button):
                child.config(fg='white', activebackground='black', activeforeground='white', relief='flat')
        toolbar.place(x=0,y=360)
        canvas.get_tk_widget().place(x=0,y=0)

        #contracts_line_chart
        contracts_line_chart_frame=tk.Frame(self.right_frame,width=1005,height=450,bg="#0b0f3c") 
        contracts_line_chart_frame.place(x=510,y=420)

        fig4=graphs.plot_contracts(self.user_id)
        if fig4=="Not Found!":
            tk.Label(contracts_line_chart_frame,text="No Contracts Found",font=("Times New Roman",24),fg="lightgray",bg='#0b0f3c').place(x=250,y=170)
        else:
            canvas = FigureCanvasTkAgg(fig4, master=contracts_line_chart_frame)
            canvas.draw()   
            toolbar = NavigationToolbar2Tk(canvas, contracts_line_chart_frame)
            toolbar.update()
        
            for child in toolbar.winfo_children():
                child.config( bd=2)
                if isinstance(child, tk.Button):
                    child.config(fg='white', activebackground='black', activeforeground='white', relief='groove')
            toolbar.place(x=0,y=404)
            canvas.get_tk_widget().place(x=0,y=0)

    def view_proposals(self):
        self.init__right_frame()
        cards_frame=tk.Frame(self.right_frame,bd=2,relief='groove',highlightbackground='lightgray',highlightthickness=1,bg='white',width=1400,height=100)
        cards_frame.place(x=68,y=50)
        proposals=db_connection.get_client_proposal_stats(self.user_id)
        self.proposal_label=tk.Label(cards_frame,text=f"Pending Proposals - {proposals['Pending']}",font=("Times New Roman",16),bg='white')
        self.proposal_label.place(x=10,y=30)
        self.proposal_var=tk.StringVar(value='Pending Proposals')
        self.proposal_dropdown=ttk.Combobox(cards_frame,textvariable=self.proposal_var,font=('Arial',16),state='readonly',width=20)
        self.proposal_dropdown['values']=['Pending Proposals','Accepted Proposals','Rejected Proposals']
        self.proposal_dropdown.place(x=1050,y=25,height=50)
        self.proposal_dropdown.bind("<<ComboboxSelected>>",self.update_proposal_label)
        #Manage Active Projects
        tk.Label(self.right_frame,text="Manage Proposals",font=('Arial',18,'bold'),fg='black',bg='white').place(x=68,y=200)
        proposals_list=db_connection.get_pending_proposals(self.user_id)
        if len(proposals_list)==0:
            tk.Label(self.right_frame,text='No Current Pending Proposals',font=('Times New Roman',20),fg='grey',bg='white').place(x=550,y=450)
        else:
            proposal_frame = tk.Frame(self.right_frame, bg='white',bd=2,relief='groove', width=1400, height=600)
            proposal_frame.place(x=68, y=250)
            tk.Label(proposal_frame,text='Title',font=('Arial',18,'bold'),fg='black',bg='white').place(x=150,y=10)
            tk.Label(proposal_frame,text='Bid Amount',font=('Arial',18,'bold'),fg='black',bg='white').place(x=400,y=10)
            tk.Label(proposal_frame,text='Freelancer',font=('Arial',18,'bold'),fg='black',bg='white').place(x=650,y=10)
            tk.Label(proposal_frame,text='Status',font=('Arial',18,'bold'),fg='black',bg='white').place(x=950,y=10)
            
            canvas = tk.Canvas(proposal_frame)
            canvas.place(x=50, y=60,width=1300, height=500)  # Adjust the height accordingly
            scrollbar = tk.Scrollbar(proposal_frame, orient="vertical", command=canvas.yview)
            scrollbar.place(x=1320, y=60, height=500)  # Align the scrollbar with the canvas
            canvas.configure(yscrollcommand=scrollbar.set)

            # Create a frame to hold the project rows and place it on the canvas
            proposal_list_frame = tk.Frame(canvas,height=0, width=1240)
            canvas.create_window((10, 10), window=proposal_list_frame, anchor='nw')
            
            List_frame_height=70
            row = 0  # Start from the first row below the headers
            for proposal in proposals_list:
                tk.Label(proposal_list_frame, text=proposal['Project_Title'], font=('Arial', 16), fg='black', bg='white').place(x=0, y=(row * 70))  # Adjust y position for each row
                tk.Label(proposal_list_frame, text=f"{proposal['Bid_Amount']}$", font=('Arial', 16), fg='black', bg='white').place(x=340, y=(row * 70))
                tk.Label(proposal_list_frame, text=proposal['Freelancer_Name'], font=('Arial', 16), fg='black', bg='white').place(x=600, y=(row * 70))
                tk.Label(proposal_list_frame, text=proposal['Status'], font=('Arial', 16), fg='black', bg='white').place(x=900, y=(row * 70))
                tk.Button(proposal_list_frame, text="View Details", font=('Arial', 14), bg="#0a295c", fg="white", command=lambda p=proposal:self.view_proposal_details(p['Proposal_ID'],p['Freelancer_Name'],p['Project_Title'],p['Bid_Amount'],p['Description'],p['Project_ID'],p['Freelancer_ID'],p['Project_Deadline'])).place(x=1100,y=(row* 70))
        
                row += 1  # Move to the next row
                proposal_list_frame.configure(height=row*List_frame_height)

            # Update the scrolling region for the canvas
            proposal_list_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

    def update_proposal_label(self,event):
        selected_proposal_type=self.proposal_var.get()
        proposals=db_connection.get_client_proposal_stats(self.user_id)
        if selected_proposal_type=="Pending Proposals":
            self.proposal_label.config(text=f"Pending Proposals - {proposals['Pending']}")
        if selected_proposal_type=="Accepted Proposals":
            self.proposal_label.config(text=f"Accepted Proposals - {proposals['Accepted']}")
        if selected_proposal_type=="Rejected Proposals":
            self.proposal_label.config(text=f"Rejected Proposals - {proposals['Rejected']}")
    
    def view_proposal_details(self,Proposal_ID,Freelancer,Title,Bid_Amount,Description,Project_ID,Freelancer_ID,Project_Deadline):
        self.view_details_window = tk.Toplevel(self.root)
        self.view_details_window.attributes('-topmost', True)
        self.view_details_window.focus_force()
        self.view_details_window.title("Proposal Details")
        self.view_details_window.geometry("1280x500")
        self.view_details_window.resizable(False,False)
        
        tk.Label(self.view_details_window, text="Project Title:", font=('Arial', 14,'bold')).place(x=20, y=30)
        tk.Label(self.view_details_window, text=Title, font=('Arial', 14),bg='lightgray').place(x=160, y=30)
        tk.Label(self.view_details_window, text="Bid Amount:", font=('Arial', 14,'bold')).place(x=600, y=30)
        tk.Label(self.view_details_window, text=(f"{Bid_Amount}$"), font=('Arial', 14),bg='lightgray').place(x=740, y=30)
        tk.Label(self.view_details_window, text="Freelancer Name:", font=('Arial', 14,'bold')).place(x=20, y=90)
        tk.Label(self.view_details_window, text=Freelancer, font=('Arial', 14),bg='lightgray').place(x=210, y=90)
        tk.Label(self.view_details_window, text="Proposal\nDescription:", font=('Arial', 14,'bold')).place(x=20, y=150)
        tk.Label(self.view_details_window, text=Description, font=('Times New Roman', 14),bg='lightgray',width=86,wraplength=1030,justify='left').place(x=230,y=150,height=250)
        tk.Button(self.view_details_window, text="Accept Proposal", font=('Arial', 16), bg="green", fg="white", command=lambda pid=Project_ID,fid=Freelancer_ID,pdl=Project_Deadline,proposal_id=Proposal_ID:self.Accept_proposal(pid,fid,pdl,proposal_id)).place(x=400, y=430)
        tk.Button(self.view_details_window, text="Reject Proposal", font=('Arial', 16), bg="red", fg="white", command=lambda pid=Proposal_ID:self.Reject_proposal(pid)).place(x=700, y=430)

    def Accept_proposal(self,Project_ID,Freelancer_ID,Project_Deadline,Proposal_ID):
        confirm=messagebox.askyesno("Info","Do you really want to Accept Proposal?",parent=self.view_details_window)
        if confirm:
            contact_created=db_connection.create_contract(Project_ID,Freelancer_ID,self.user_id,Project_Deadline,Proposal_ID)
            if contact_created=="Success":
                messagebox.showinfo("Success","Contract Created Successfully",parent=self.view_details_window)
                self.view_details_window.destroy()
                self.view_proposals()
            else:
                messagebox.showerror("Error","Contract Couldn't Created!",parent=self.view_details_window)

    def Reject_proposal(self,Proposal_ID):
        confirm=messagebox.askyesno("Info","Do you really want to Accept Proposal?",parent=self.view_details_window)
        if confirm:
            rejected=db_connection.reject_proposal(Proposal_ID)
            if rejected:
                messagebox.showinfo("Success","Proposal rejected Successfully",parent=self.view_details_window)
                self.view_details_window.destroy()
                self.view_proposals()
            else:
                messagebox.showerror("Error","Something went wrong!",parent=self.view_details_window)

    def view_payments(self):
        self.init__right_frame()
        cards_frame = tk.Frame(self.right_frame, bd=2, relief='groove', highlightbackground='lightgray', highlightthickness=1, bg='white', width=1400, height=100)
        cards_frame.place(x=68, y=50)
    
        # Fetch contract stats for the client
        contracts = db_connection.get_client_contract_stats(self.user_id)
        self.contract_label = tk.Label(cards_frame, text=f"Active Contracts - {contracts['Active']}", font=("Times New Roman", 16), bg='white')
        self.contract_label.place(x=10, y=30)
    
        self.contract_var = tk.StringVar(value='Active Contracts')
        self.contract_dropdown = ttk.Combobox(cards_frame, textvariable=self.contract_var, font=('Arial', 16), state='readonly', width=20)
        self.contract_dropdown['values'] = ['Active Contracts', 'Completed Contracts', 'Terminated Contracts']
        self.contract_dropdown.place(x=1050, y=25, height=50)
        self.contract_dropdown.bind("<<ComboboxSelected>>", self.update_contract_label)
    
        # Manage Active Contracts Section
        tk.Label(self.right_frame, text="Manage Payments", font=('Arial', 18, 'bold'), fg='black', bg='white').place(x=68, y=200)
    
        # Fetch the list of active contracts for the client
        contract_list = db_connection.get_active_contracts(self.user_id)
    
        if len(contract_list) == 0:
            tk.Label(self.right_frame, text='No Current Active Contracts', font=('Times New Roman', 20), fg='grey', bg='white').place(x=550, y=450)
        else:
            contract_frame = tk.Frame(self.right_frame, bg='white', bd=2, relief='groove', width=1400, height=600)
            contract_frame.place(x=68, y=250)
        
            # Add headers for the contract list
            tk.Label(contract_frame, text='Freelancer', font=('Arial', 18, 'bold'), fg='black', bg='white').place(x=150, y=10)
            tk.Label(contract_frame, text='Bid Amount', font=('Arial', 18, 'bold'), fg='black', bg='white').place(x=400, y=10)
            tk.Label(contract_frame, text='Project Title', font=('Arial', 18, 'bold'), fg='black', bg='white').place(x=650, y=10)
            tk.Label(contract_frame, text='Status', font=('Arial', 18, 'bold'), fg='black', bg='white').place(x=950, y=10)
        
            canvas = tk.Canvas(contract_frame)
            canvas.place(x=50, y=60, width=1300, height=500)
            scrollbar = tk.Scrollbar(contract_frame, orient="vertical", command=canvas.yview)
            scrollbar.place(x=1320, y=60, height=500)
            canvas.configure(yscrollcommand=scrollbar.set)
        
            # Create a frame to hold the contract rows and place it on the canvas
            contract_list_frame = tk.Frame(canvas, height=0, width=1240)
            canvas.create_window((10, 10), window=contract_list_frame, anchor='nw')
        
            List_frame_height = 70
            row = 0  # Start from the first row below the headers
            for contract in contract_list:
                tk.Label(contract_list_frame, text=contract[1], font=('Arial', 16), fg='black', bg='white').place(x=0, y=(row * 70))
                tk.Label(contract_list_frame, text=f"{contract[2]}$", font=('Arial', 16), fg='black', bg='white').place(x=340, y=(row * 70))
                tk.Label(contract_list_frame, text=contract[3], font=('Arial', 16), fg='black', bg='white').place(x=600, y=(row * 70))
                tk.Label(contract_list_frame, text=contract[4], font=('Arial', 16), fg='black', bg='white').place(x=900, y=(row * 70))
            
                # Button to view contract details
                tk.Button(contract_list_frame, text="Pay Amount", font=('Arial', 14), bg="#0a295c", fg="white", 
                      command=lambda c=contract: self.pay(c[0],c[1],c[3],c[2],c[5],c[6])).place(x=1100, y=(row * 70))
            
                row += 1  # Move to the next row
                contract_list_frame.configure(height=row * List_frame_height)
        
            # Update the scrolling region for the canvas
            contract_list_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
        
    def update_contract_label(self, event):
        selected_contract_type = self.contract_var.get()
        contracts = db_connection.get_client_contract_stats(self.user_id)
    
        if selected_contract_type == "Active Contracts":
            self.contract_label.config(text=f"Active Contracts - {contracts['Active']}")
        if selected_contract_type == "Completed Contracts":
            self.contract_label.config(text=f"Completed Contracts - {contracts['Completed']}")
        if selected_contract_type == "Terminated Contracts":
            self.contract_label.config(text=f"Terminated Contracts - {contracts['Terminated']}")

    def pay(self,Contract_ID,Freelancer_Name,Title,Bid_Amount,Project_ID,Freelancer_ID):
        self.pay_window = tk.Toplevel(self.root)
        self.pay_window.attributes('-topmost', True)
        self.pay_window.focus_force()
        self.pay_window.title("Payments")
        self.pay_window.geometry("1280x500")
        self.pay_window.resizable(False,False)
        
        tk.Label(self.pay_window, text="Project Title:", font=('Arial', 14,'bold')).place(x=20, y=30)
        tk.Label(self.pay_window, text=Title, font=('Arial', 14),bg='lightgray').place(x=160, y=30)
        tk.Label(self.pay_window, text="Pay Amount:", font=('Arial', 14,'bold')).place(x=600, y=30)
        tk.Label(self.pay_window, text=(f"{Bid_Amount}$"), font=('Arial', 14),bg='lightgray').place(x=770, y=30)
        tk.Label(self.pay_window, text="Freelancer Name:", font=('Arial', 14,'bold')).place(x=20, y=90)
        tk.Label(self.pay_window, text=(f"{Freelancer_Name}"), font=('Arial', 14),bg='lightgray').place(x=210, y=90)
        tk.Label(self.pay_window, text="Payment Method:", font=('Arial', 14,'bold')).place(x=20, y=150)
        self.payment_methods = ["Bank Transfer", "Credit Card", "PayPal", "JazzCash", "EasyPaisa"]
        self.payment_method_var = tk.StringVar()
        self.payment_dropdown = ttk.Combobox(self.pay_window, textvariable=self.payment_method_var, values=self.payment_methods, state="readonly")
        self.payment_dropdown.set("Select Payment Method")
        self.payment_dropdown.place(x=210, y=150, width=200,height=35)

        tk.Label(self.pay_window, text="Rating:", font=('Arial', 14,'bold')).place(x=600, y=150)
        ratings = [str(i) for i in range(1, 6)]
        self.rating_var = tk.StringVar()
        rating_dropdown = ttk.Combobox(self.pay_window, textvariable=self.rating_var, values=ratings, state="readonly")
        rating_dropdown.set("Select Rating")
        rating_dropdown.place(x=700, y=150, width=200,height=35)

        tk.Label(self.pay_window, text="Comment:", font=('Arial', 14,'bold')).place(x=20, y=200)
        self.comment_entry = tk.Text(self.pay_window, font=('Arial', 12), width=92)
        self.comment_entry.place(x=150, y=200,height=200)
        tk.Button(self.pay_window, text="Pay Amount", font=('Arial', 14), bg="#0a295c", fg="white", command=lambda cid=Contract_ID,bamt=Bid_Amount,fid=Freelancer_ID,pid=Project_ID:self.pay_amount(cid,bamt,fid,pid)).place(x=600, y=430)
        
    def pay_amount(self,Contract_ID,Pay_amount,Freelancer_ID,Project_ID):
        payment_metod=self.payment_method_var.get()
        rating=self.rating_var.get()
        comment=self.comment_entry.get(1.0,'end').strip()
        words=comment.split()
        if not payment_metod or not rating or not comment:
            messagebox.showerror("Error","Please fill all fields!",parent=self.pay_window)
        elif (len(words)>150):
            messagebox.showerror("Error","Comment limit exceeds 150 words!",parent=self.pay_window)
        else:
            payment=db_connection.add_payments(Contract_ID,Pay_amount,payment_metod,self.user_id,Freelancer_ID,Project_ID,rating,comment)
            if payment:
                messagebox.showinfo("Info","Payment Successfull!",parent=self.pay_window)
                self.pay_window.destroy()
                self.view_payments()
            else:
                messagebox.showerror("Error","Something Gone wrong!",parent=self.pay_window)  

    def view_messages(self):
        self.init__right_frame()
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
    

