import pyodbc
import datetime

# Database connection setup
def get_db_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=DESKTOP-ISD8BJH;"
            "DATABASE=Freelance;"
            "Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        print("Database Connection Error:", e)
        return None

# Function to validate user login
def authenticate_user(email, password):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = "SELECT User_ID, User_Name, Role_ID,Status_ID FROM Users WHERE User_Email = ? AND User_Password = ?"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        conn.close()
        return user
    return None


def activate_account(user_id):
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("UPDATE Users SET Status_ID=1 WHERE User_ID=?",(user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        print(e)

# Function to register a new user
def register_user(name, email, phone, password, role):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT User_Email FROM Users WHERE User_Email=?",email)
        existing_user=cursor.fetchone()
        if existing_user:
            return 'User_Exist'
        else:
            status_ID=1
            cursor.execute("""INSERT INTO Users (User_Name, User_Email,User_Phone,User_Password,Role_id,Status_ID) VALUES (?, ?, ?, ?, ?,?)""", (name, email, phone, password, role,status_ID))
            return True
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.commit()
        conn.close()

def save_freelancer_profile(user_id, description, skills):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("Update Users SET User_Profile_Description=? WHERE User_ID=?", (description,user_id))
    for skill in skills:
        query=("SELECT * FROM Skills WHERE Skill_Name=?")
        cursor.execute(query,skill)
        skill_table=cursor.fetchone()
        skill_id=skill_table[0]
        cursor.execute("INSERT INTO User_Skills (User_ID, Skill_ID) VALUES (?, ?)", (user_id, skill_id))
    conn.commit()
    conn.close()

def update_user_role(user_id, new_role_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET Role_ID = ? WHERE User_ID = ?", (new_role_id, user_id))
    conn.commit()
    conn.close()

def get_freelancer_stats(user_id):
    # Initialize values with 0
    total_projects = 0
    active_projects = 0
    completed = 0
    earnings = 0.0

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Total Projects
        cursor.execute("SELECT COUNT(*) FROM Contracts WHERE Freelancer_ID = ?", (user_id,))
        total_projects = cursor.fetchone()[0]

        # Active Projects
        cursor.execute("""
            SELECT COUNT(*) FROM Contracts 
            WHERE Freelancer_ID = ? AND Contract_Status_ID = 
                (SELECT Contract_Status_ID FROM Contract_Status WHERE Contract_Status_Name = 'Active')
        """, (user_id,))
        active_projects = cursor.fetchone()[0]

        # Completed Projects
        cursor.execute("""
            SELECT COUNT(*) FROM Contracts 
            WHERE Freelancer_ID = ? AND Contract_Status_ID = 
                (SELECT Contract_Status_ID FROM Contract_Status WHERE Contract_Status_Name = 'Completed')
        """, (user_id,))
        completed = cursor.fetchone()[0]

        # Total Earnings
        cursor.execute("""
            SELECT ISNULL(SUM(P.Amount), 0) FROM Payments P
            JOIN Contracts C ON P.Contract_ID = C.Contract_ID
            WHERE C.Freelancer_ID = ? AND P.Payment_Status_ID = 
                (SELECT Payment_Status_ID FROM Payment_Status WHERE Payment_Status_Name = 'Paid')
        """, (user_id,))
        earnings = float(cursor.fetchone()[0])

    except Exception as e:
        print("Error fetching freelancer stats:", e)

    finally:
        conn.close()

    return {
        "total_projects": total_projects,
        "active_projects": active_projects,
        "completed": completed,
        "earnings": earnings
    }

    
def get_active_projects(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT P.Project_Title,P.Project_Budget,P.Project_Deadline, U.User_Name, CS.Contract_Status_Name
            FROM Contracts C
            JOIN Projects P ON C.Project_ID = P.Project_ID
            JOIN Users U ON P.Client_ID = U.User_ID
            JOIN Contract_Status CS ON C.Contract_Status_ID = CS.Contract_Status_ID
            WHERE C.Freelancer_ID = ? AND CS.Contract_Status_Name = 'Active'
        """, (user_id,))
        
        projects = cursor.fetchall()
        return projects

    except Exception as e:
        return None
    finally:
        conn.close()
    
def get_client_projects(client_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Active Projects (Show which freelancer is handling)
        active_query = """
            SELECT P.Project_Title, P.Project_Budget, P.Project_Deadline,
                   U.User_Name AS Freelancer_Name, CS.Contract_Status_Name
            FROM Contracts C
            JOIN Projects P ON C.Project_ID = P.Project_ID
            JOIN Users U ON C.Freelancer_ID = U.User_ID
            JOIN Contract_Status CS ON C.Contract_Status_ID = CS.Contract_Status_ID
            WHERE P.Client_ID = ? AND CS.Contract_Status_Name = 'Active';
        """
        cursor.execute(active_query, (client_id,))
        active_projects = cursor.fetchall()

        # Open Projects And Closed (Projects without signed contracts, no freelancer assigned)
        open_query = """
            SELECT P.Project_ID, P.Project_Title, P.Project_Budget, P.Project_Deadline,P.Project_Status_ID
            FROM Projects P
            WHERE P.Client_ID = ? AND (P.Project_Status_ID=1 OR P.Project_Status_ID=4);
        """
        cursor.execute(open_query, (client_id))
        open_projects = cursor.fetchall()

        # Completed Projects (Projects with completed contracts)
        completed_query = """
            SELECT P.Project_Title, P.Project_Budget, P.Project_Deadline,
                   U.User_Name AS Freelancer_Name, CS.Contract_Status_Name
            FROM Contracts C
            JOIN Projects P ON C.Project_ID = P.Project_ID
            JOIN Users U ON C.Freelancer_ID = U.User_ID
            JOIN Contract_Status CS ON C.Contract_Status_ID = CS.Contract_Status_ID
            WHERE P.Client_ID = ? AND CS.Contract_Status_Name = 'Completed';
        """
        cursor.execute(completed_query, (client_id,))
        completed_projects = cursor.fetchall()

        return {
            "active_projects": active_projects,
            "open_projects": open_projects,
            "completed_projects": completed_projects
        }
    except Exception as e:
        print("Error fetching client projects:", e)
        return None
    finally:
        conn.close()
    

def add_project(Client_ID,Title,Desc,Budget,Deadline,Status):
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        query="""INSERT INTO Projects(Client_ID,Project_Title,Project_Description,Project_Budget,Project_Deadline,Project_Status_ID)
            VALUES(?,?,?,?,?,?)"""
        cursor.execute(query,(Client_ID,Title,Desc,Budget,Deadline,Status))
        return True
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.commit()
        conn.close()

def get_freelancer_proposal_stats(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT 
                PS.Proposal_Status_Name, 
                COUNT(*) AS Total
            FROM 
                Proposals P
            JOIN 
                Proposal_Status PS ON P.Proposal_Status_ID = PS.Proposal_Status_ID
            WHERE 
                P.Freelancer_ID = ?
            GROUP BY 
                PS.Proposal_Status_Name
        """
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

        # Initialize a dictionary with possible statuses and set them to 0 initially
        possible_statuses = ['Pending', 'Accepted', 'Rejected']
        stats = {status: 0 for status in possible_statuses}

        # Update the dictionary with actual data
        for row in results:
            status_name = row[0]
            total = row[1]
            stats[status_name] = total

        return stats
    except Exception as e:
        print("Error fetching proposal stats:", e)
        return None
    finally:
        conn.close()

def get_proposals_list(freelancer_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT 
                PJ.Project_Title AS Project,
                PR.Proposal_Bid_Amount AS Bid_Amount,
                C.User_Name AS Client_Name,
                PS.Proposal_Status_Name AS Status
            FROM 
                Proposals PR
            JOIN 
                Projects PJ ON PR.Project_ID = PJ.Project_ID
            JOIN 
                Users C ON PJ.Client_ID = C.User_ID
            JOIN 
                Proposal_Status PS ON PR.Proposal_Status_ID = PS.Proposal_Status_ID
            WHERE 
                PR.Freelancer_ID = ?
                AND PS.Proposal_Status_Name IN ('Pending', 'Accepted', 'Rejected')
            ORDER BY PS.Proposal_Status_Name ASC
        """
        cursor.execute(query, (freelancer_id,))
        return cursor.fetchall()
    except Exception as e:
        print("Error fetching freelancer proposals:", e)
        return []
    finally:
        conn.close()

def edit_project(Project_ID,Client_ID,Title,Desc,Budget,Deadline,Status):
    conn = get_db_connection()
    cursor = conn.cursor()

    updates = []
    values = []

    if Title !="":
        updates.append("Project_Title = ?")
        values.append(Title)

    if Desc != "":
        updates.append("Project_Description = ?")
        values.append(Desc)

    if Budget !="":
        updates.append("Project_Budget = ?")
        values.append(Budget)

    if Deadline != "":
        updates.append("Project_Deadline = ?")
        values.append(Deadline)

    if Status != "":
        updates.append("Project_Status_ID = ?")
        values.append(Status)
    query = f"UPDATE Projects SET {', '.join(updates)} WHERE Project_ID = ?"
    values.append(Project_ID)
    try:
        cursor.execute(query, values)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.close()

def get_project_list():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                P.Project_ID,
                P.Project_Title,
                P.Project_Description,
                P.Project_Budget,
                P.Project_Deadline,
                U.User_Name AS Client_Name
            FROM 
                Projects P
            JOIN 
                Users U ON P.Client_ID = U.User_ID
            WHERE 
                P.Project_Status_ID = 1  -- 1 = Open or Available
        """
        cursor.execute(query)
        projects = cursor.fetchall()
        return projects
    except Exception as e:
        print("Error browsing available projects:", e)
        return []
    finally:
        conn.close()

def submit_proposal(freelancer_id, project_id, bid_amount, desc, status_id=1):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO Proposals 
            (Freelancer_ID, Project_ID, Proposal_Bid_Amount, Proposal_description, Proposal_Status_ID)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (freelancer_id, project_id, bid_amount, desc, status_id))
        conn.commit()
        return True
    except Exception as e:
        print("Error submitting proposal:", e)
        conn.rollback()
        return False
    finally:
        conn.close()

def top_freelancers():
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("""
        SELECT TOP 5 
            U.User_Name,
            AVG(R.Rating) AS Avg_Rating
        FROM Reviews R
        JOIN Users U ON R.Reviewed_User_ID = U.User_ID
        GROUP BY U.User_Name
        ORDER BY Avg_Rating DESC;
        """)
        rows = cursor.fetchall()
        names = [row[0] for row in rows]
        ratings = [row[1] for row in rows]
        return {"names":names,"ratings":ratings}
    except:
        print("Something Happened wrong!")

def top_skills():
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        query = """
            SELECT S.Skill_Name, COUNT(US.User_ID) AS Freelancer_Count
            FROM User_Skills US
            JOIN Skills S ON US.Skill_ID = S.Skill_ID
            GROUP BY S.Skill_Name
            ORDER BY Freelancer_Count DESC;
            """
        cursor = conn.cursor()
        cursor.execute(query)
        skills = []
        counts = []

        for row in cursor:
            skills.append(row.Skill_Name)
            counts.append(row.Freelancer_Count)
        return {"skills":skills,"counts":counts}
    except:
        print("Unknown error has occured!")

def fetch_contract_data(user_id):
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        contract_query = """
            SELECT 
            C.Start_Date AS Date,
            COUNT(C.Contract_ID) AS Contracts_Established
            FROM 
            Contracts C
            WHERE 
            C.Client_ID = ?  -- Use the client ID
            GROUP BY 
            C.Start_Date
            ORDER BY 
            C.Start_Date DESC
            """
    
        # Execute the query
        cursor.execute(contract_query, user_id)
        contract_stats = cursor.fetchall()
        return contract_stats
    except:
        print("Error,something gone wrong!")
    finally:
        conn.close()

def fetch_payments_data(user_id):
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        payment_query = """
            SELECT 
            P.Payment_Date AS Date,
            SUM(P.Amount) AS Total_Payment_Spent
            FROM 
            Payments P
            JOIN 
            Contracts C ON P.Contract_ID = C.Contract_ID
            WHERE 
            C.Client_ID = ?  
            GROUP BY 
            P.Payment_Date
            ORDER BY 
            P.Payment_Date DESC;
            """
    
        cursor.execute(payment_query,user_id)
        payment_stats = cursor.fetchall()
        return payment_stats
    except:
        print("Error,something gone wrong!")
    finally:
        conn.close()

def get_client_proposal_stats(client_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                PS.Proposal_Status_Name,
                COUNT(*) AS Total
            FROM 
                Proposals P
            JOIN 
                Proposal_Status PS ON P.Proposal_Status_ID = PS.Proposal_Status_ID
            JOIN 
                Projects PR ON P.Project_ID = PR.Project_ID
            WHERE 
                PR.Client_ID = ?
            GROUP BY 
                PS.Proposal_Status_Name
        """
        
        cursor.execute(query, (client_id,))
        results = cursor.fetchall()

        # Ensure all statuses are represented even if count is zero
        full_stats = {'Pending': 0, 'Accepted': 0, 'Rejected': 0}
        for status, count in results:
            full_stats[status] = count

        return full_stats

    except Exception as e:
        print("Error fetching client proposal stats:", e)
        return None
    finally:
        conn.close()

def get_pending_proposals(client_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                P.Proposal_ID,
                U.User_Name AS Freelancer_Name,
                PR.Project_Title,
                P.Proposal_Bid_Amount,
                P.Proposal_Description,
                PS.Proposal_Status_Name,
                P.Project_ID,
                P.Freelancer_ID,
                PR.Project_Deadline
            FROM 
                Proposals P
            JOIN 
                Projects PR ON P.Project_ID = PR.Project_ID
            JOIN 
                Users U ON P.Freelancer_ID = U.User_ID
            JOIN 
                Proposal_Status PS ON P.Proposal_Status_ID = PS.Proposal_Status_ID
            WHERE 
                PR.Client_ID = ?
                AND PS.Proposal_Status_Name = 'Pending'
            ORDER BY 
                P.Proposal_ID DESC
        """

        cursor.execute(query, (client_id,))
        proposals = cursor.fetchall()

        proposal_list = []
        for row in proposals:
            proposal_list.append({
                'Proposal_ID': row[0],
                'Freelancer_Name': row[1],
                'Project_Title': row[2],
                'Bid_Amount': row[3],
                'Description': row[4],
                'Status': row[5],
                'Project_ID': row[6],
                'Freelancer_ID': row[7],
                'Project_Deadline': row[8]
            })

        return proposal_list

    except Exception as e:
        print("Error fetching pending proposals:", e)
        return []
    finally:
        conn.close()

def create_contract(Project_ID,Freelancer_ID,Client_ID,End_Date,Proposal_ID):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        start_date = datetime.datetime.now().date()

        # Step 1: Insert into Contracts
        insert_contract = """
            INSERT INTO Contracts (Project_ID, Freelancer_ID, Client_ID, Start_Date, End_Date, Contract_Status_ID)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_contract, (
            Project_ID,
            Freelancer_ID,
            Client_ID,
            start_date,
            End_Date,
            1
        ))

        # Step 2: Update Proposal Status to Accepted
        update_proposal = """
            UPDATE Proposals SET Proposal_Status_ID = 2 WHERE Proposal_ID = ?
        """
        cursor.execute(update_proposal, (Proposal_ID,))

        # Step 3: Update Project Status to In Progress
        update_project = """
            UPDATE Projects SET Project_Status_ID = 2 WHERE Project_ID = ?
        """
        cursor.execute(update_project, (Project_ID,))

        conn.commit()
        return "Success"

    except Exception as e:
        conn.rollback()
        print( f"Error: {e}")

    finally:
        conn.close()

def reject_proposal(Proposal_ID):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Set Proposal_Status_ID = 3 for Rejected
        update_query = """
            UPDATE Proposals
            SET Proposal_Status_ID = 3
            WHERE Proposal_ID = ?
        """
        cursor.execute(update_query, (Proposal_ID,))
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    finally:
        conn.close()


def get_client_contract_stats(client_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                CS.Contract_Status_Name,
                COUNT(*) AS Total
            FROM 
                Contracts C
            JOIN 
                Contract_Status CS ON C.Contract_Status_ID = CS.Contract_Status_ID
            JOIN 
                Projects PR ON C.Project_ID = PR.Project_ID
            WHERE 
                PR.Client_ID = ?
            GROUP BY 
                CS.Contract_Status_Name
        """
        
        cursor.execute(query, (client_id,))
        results = cursor.fetchall()

        # Ensure all statuses are represented even if count is zero
        full_stats = {'Active': 0, 'Completed': 0, 'Terminated': 0}
        for status, count in results:
            full_stats[status] = count

        return full_stats

    except Exception as e:
        print("Error fetching client contract stats:", e)
        return None
    finally:
        conn.close()

def get_active_contracts(client_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                C.Contract_ID,
                U.User_Name AS Freelancer_Name,
                P.Proposal_Bid_Amount AS Bid_Amount,
                PR.Project_Title,
                CS.Contract_Status_Name AS Status,
                P.Project_ID,
                C.Freelancer_ID
            FROM 
                Contracts C
            JOIN 
                Contract_Status CS ON C.Contract_Status_ID = CS.Contract_Status_ID
            JOIN 
                Projects PR ON C.Project_ID = PR.Project_ID
            JOIN 
                Users U ON C.Freelancer_ID = U.User_ID
            JOIN 
                Proposals P ON P.Project_ID = PR.Project_ID AND P.Freelancer_ID = U.User_ID
            WHERE 
                PR.Client_ID = ? AND CS.Contract_Status_Name = 'Active'
        """
    
        cursor.execute(query, (client_id,))
        contracts = cursor.fetchall()
        
        return contracts
    except Exception as e:
        print("Error fetching active contracts:", e)
        return []
    finally:
        conn.close()

def add_payments(Contract_ID,Amount,Payment_Method,Reviewer_ID,Reviewed_ID,Project_ID,Rating,Comment):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        payment_date=datetime.datetime.now().date()

        payments_query = """
            INSERT INTO Payments (Contract_ID, Amount, Payment_Method,Payment_Date,Payment_Status_ID)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(payments_query, (Contract_ID, Amount, Payment_Method, payment_date,2))
        
        #Update Contract_Status
        update_contract_query = """
            UPDATE Contracts
            SET Contract_Status_ID = 2
            WHERE Contract_ID = ?
        """
        cursor.execute(update_contract_query, (Contract_ID,))

        #Update Project_Status
        update_project_query = """
            UPDATE Projects
            SET Project_Status_ID = 3
            WHERE Project_ID = ?
        """
        cursor.execute(update_project_query, (Project_ID,))

        #Insert into Reviews
        insert_review_query = """
            INSERT INTO Reviews (Reviewer_ID, Reviewed_User_ID, Project_ID, Rating, Comment)
            VALUES (?, ?, ?, ?, ?)
            """
        cursor.execute(insert_review_query, (Reviewer_ID, Reviewed_ID, Project_ID, Rating, Comment))

        conn.commit()
        return True
    except Exception as e:
        print("Error adding payment:", e)
        conn.rollback()
        return False
    finally:
        conn.close()

def get_freelancer_payment_stats(freelancer_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """SELECT C.Freelancer_ID,
            COALESCE(SUM(CASE WHEN Pay.Payment_Status_ID = 2 THEN 1 ELSE 0 END), 0) AS Paid_Count,
            COALESCE(SUM(CASE WHEN Pay.Payment_Status_ID != 2 THEN 1 ELSE 0 END), 0) AS Pending_Count
            FROM 
            Payments Pay
            JOIN 
            Contracts C ON Pay.Contract_ID = C.Contract_ID
            WHERE C.Freelancer_ID = ? 
            GROUP BY 
            C.Freelancer_ID;"""

        # Execute the query with the provided freelancer_id
        cursor.execute(query, (freelancer_id,))
        results = cursor.fetchone()

        full_stats = {'Paid': 0, 'Pending': 0}

        if results is None:
            return full_stats
        
        _, paid_count, pending_count = results
        # Assign values to the dictionary
        if paid_count != 0:
            full_stats['Paid'] = paid_count
        if pending_count != 0:
            full_stats['Pending'] = pending_count

        return full_stats

    except Exception as e:
        print(f"[Error] get_freelancer_payment_stats: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_paid_payments(freelancer_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                PM.Payment_ID,
                PR.Project_Title,
                CL.User_Name AS Client_Name,
                PM.Amount,
                PM.Payment_Method,
                RV.Rating,
                RV.Comment,
                PM.Payment_Date
            FROM 
                Payments PM
            INNER JOIN 
                Contracts C ON PM.Contract_ID = C.Contract_ID
            INNER JOIN 
                Projects PR ON C.Project_ID = PR.Project_ID
            INNER JOIN 
                Users CL ON C.Client_ID = CL.User_ID
            LEFT JOIN 
                Reviews RV ON PR.Project_ID = RV.Project_ID AND RV.Reviewed_User_ID = C.Freelancer_ID
            WHERE 
                C.Freelancer_ID = ?
                AND PM.Payment_Status_ID = 2
            ORDER BY 
                PM.Payment_Date DESC;
        """

        cursor.execute(query, (freelancer_id,))
        rows = cursor.fetchall()

        paid_payments = []
        for row in rows:
            payment = {
                'Payment_ID': row[0],
                'Project_Title': row[1],
                'Client_Name': row[2],
                'Amount': row[3],
                'Method': row[4],
                'Rating': row[5],
                'Comment': row[6],
                'Payment_Date': row[7]
            }
            paid_payments.append(payment)

        return paid_payments

    except Exception as e:
        print(f"[Error] get_paid_payments: {e}")
        return []
    finally:
        conn.close()

def get_freelancer_data(user_ID):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT * FROM Users WHERE User_ID=?
        """

        cursor.execute(query, (user_ID,))
        user_data=cursor.fetchall()

        return user_data[0]

    except Exception as e:
        print(f"[Error] get_paid_payments: {e}")
        return []
    finally:
        conn.close()

def update_details(name,email,phone,desc,new_pass,user_id):
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        check_mail_exist='SELECT COUNT(*) FROM Users WHERE User_Email = ? AND User_ID != ?'
        cursor.execute(check_mail_exist,(email,user_id))
        result=cursor.fetchone()
        if result[0]>0:
            return 'email exist'
        else:
            update_query="""UPDATE Users
                SET User_Name= ?,
                User_Email= ?,
                User_Phone= ?,
                User_Password= ?,
                User_Profile_Description= ?
                WHERE User_Id= ?"""
        
            cursor.execute(update_query,(name,email,phone,new_pass,desc,user_id))
            return True
    except Exception as e:
        conn.rollback()
        print(e)
        return None
    finally:
        conn.commit()
        conn.close()

def check_active_projects(user_id):
    try:
        conn=get_db_connection()
        cursor=conn.cursor()
        query="""SELECT COUNT(*) FROM Contracts WHERE Freelancer_ID=? and Contract_Status_ID=? """
        cursor.execute(query,(user_id,1))
        results=cursor.fetchone()
        if results and results[0]>0:
            return "Active"
        else:
            deactivate_query="""UPDATE Users SET Status_ID=2 WHERE User_ID= ? """
            cursor.execute(deactivate_query,(user_id,))
            #Update open Projects
            close_query="""UPDATE Projects SET Project_Status_ID=4 WHERE Client_ID= ?"""
            cursor.execute(close_query,(user_id,))
            return True
    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        conn.commit()
        conn.close()

def fetch_all_users(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT u.User_ID,u.User_Name,u.User_Email ,r.Role_Name
            FROM Users u 
            Join User_Roles r
            ON u.Role_ID=r.Role_ID
            WHERE User_ID !=?
        """

        cursor.execute(query,(user_id,))
        users=cursor.fetchall()

        return users

    except Exception as e:
        print(f"[Error] Get All Users: {e}")
        return []
    finally:
        conn.close()
    
from datetime import datetime

def fetch_user_messages(sender_id, receiver_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT * 
            FROM Messages
            WHERE 
                (Sender_ID = ? AND Receiver_ID = ?)
                OR
                (Sender_ID = ? AND Receiver_ID = ?)
            ORDER BY Timestamp ASC
        """
        cursor.execute(query, (sender_id, receiver_id, receiver_id, sender_id))
        rows = cursor.fetchall()

        # Format date and time
        messages = []
        for row in rows:
            msg = {
                "Message_ID": row[0],
                "Sender_ID": row[1],
                "Receiver_ID": row[2],
                "Text": row[3],
                "DateTime": row[4]
            }
            messages.append(msg)

        return messages

    except Exception as e:
        print(f"[Error] Fetching messages between users {sender_id} and {receiver_id}: {e}")
        return []
    finally:
        conn.close()


def send_message(sender_id,receiver_id,content):
    try:
        print(content)
        conn = get_db_connection()  
        cursor = conn.cursor()

        query = """
        INSERT INTO Messages (Sender_ID, Receiver_ID, Message_Content)
        VALUES (?, ?, ?)
        """
        cursor.execute(query, (sender_id, receiver_id,content))
        conn.commit()
        
        return True
    except Exception as e:
        conn.rollback() 
        print(f"[Error] Write Message: {e}")
        return False
    finally:
        conn.close()
