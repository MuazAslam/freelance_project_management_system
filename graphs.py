import matplotlib.pyplot as plt
import db_connection
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_top_freelancers():
    stats = db_connection.top_freelancers()
    names = stats["names"]
    ratings = stats["ratings"]

    plt.figure(figsize=(6,3))
    fig = plt.gcf()
    fig.patch.set_facecolor('#010132')
    ax = plt.gca()
    ax.set_facecolor('#010132')

    # Bar Chart (Column)
    bars = ax.bar(names, ratings, color="#db4e06", label='Rating')

    # Text Labels
    for i, rating in enumerate(ratings):
        label = f"{rating:.1f}" if rating < 5 else "Perfect 5"
        ax.text(i, rating + 0.1, label, ha='center', color='white', fontsize=10, fontname="Arial")

    # Styling
    ax.set_title("Top Freelancers by Rating", fontsize=14, color='white', fontname="Arial", weight='bold')
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, color='white', fontsize=10, fontname="Arial")
    ax.set_yticks([i for i in range(6)])
    ax.tick_params(axis='y', colors='white')
    ax.set_ylim(0, 5.5)
    ax.grid(True, linestyle='--', axis='y', color='white', alpha=0.3)
    ax.legend(facecolor='#010132', edgecolor='white', labelcolor='white')

    # Remove chart spines
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    return fig


def get_top_skills():
    
    stats = db_connection.top_skills()

    fig, ax = plt.subplots(figsize=(4, 4)) 
    fig = plt.gcf()
    fig.patch.set_facecolor('#010132')  
    ax = plt.gca()
    ax.set_facecolor('#010132')  

    # Pie Chart
    wedges, texts, autotexts = ax.pie(
        stats["counts"], 
        labels=stats["skills"], 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=["#db4e06", "#00BFFF", "#9400D3", "#4B0082", "#8B008B","#0047AB", "#2a3439", "#004B49","#353839","#660000"],  # Adjust colors
        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5}
    )

    # Styling
    plt.title("Top Skills", fontsize=12, color='white', fontname="Arial", weight='bold',pad=0, y=1)

    # Font styling for pie chart text
    for text in texts:
        text.set_fontsize(8)
        text.set_fontname("Arial")
        text.set_color('white')

    for autotext in autotexts:
        autotext.set_fontsize(8)
        autotext.set_fontname("Arial")
        autotext.set_color('white')

    # Remove grid lines and spines for the pie chart
    ax.grid(False)
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)

    # Make the plot tight to avoid clipping
    plt.tight_layout()

    return fig

def plot_payments(user_id):
    payment_stats = db_connection.fetch_payments_data(user_id)
    if not payment_stats:
        return "Not Found!"

    dates = []
    amounts = []

    for row in payment_stats:
        date_str, amount = row
        try:
            date = datetime.strptime(str(date_str), "%Y-%m-%d")
        except:
            date = date_str
        dates.append(date)
        amounts.append(float(amount))

    plt.figure(figsize=(6.5, 3))
    fig = plt.gcf()
    fig.patch.set_facecolor('#010132')
    ax = plt.gca()
    ax.set_facecolor('#010132')

    ax.plot(dates, amounts, marker='o', linestyle='-', color='#db4e06', linewidth=2, label="Total Payment Spent")

    for i, (x, y) in enumerate(zip(dates, amounts)):
        ax.text(x, y + 0.5, f"{y:.0f}", color='white', fontsize=10, ha='center')

    ax.set_title("Payments Over Time", fontsize=14, color='white', fontname="Arial", weight='bold')
    ax.set_xlabel("Date", color='white', fontsize=10, fontname="Arial")
    ax.set_ylabel(" Payments($)", color='white', fontsize=10, fontname="Arial")
    ax.tick_params(axis='x', colors='white', labelrotation=45)
    ax.tick_params(axis='y', colors='white')
    ax.grid(True, linestyle='--', color='white', alpha=0.3)
    ax.legend(facecolor='#010132', edgecolor='white', labelcolor='white')

    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    return fig

def plot_contracts(user_id):
    payment_stats = db_connection.fetch_contract_data(user_id)
    if not payment_stats:
        return "Not Found!"

    dates = []
    values = []

    for row in payment_stats:
        date_str, value = row
        try:
            date = datetime.strptime(str(date_str), "%Y-%m-%d")
        except:
            date = date_str
        dates.append(date)
        values.append(value)

    plt.figure(figsize=(8.3, 3.4))
    fig = plt.gcf()
    fig.patch.set_facecolor('#010132')
    ax = plt.gca()
    ax.set_facecolor('#010132')

    ax.plot(dates, values, marker='o', linestyle='-', color='#db4e06', linewidth=2, label="Contract Established")

    for i, (x, y) in enumerate(zip(dates, values)):
        ax.text(x, y + 0.5, f"{y:.0f}", color='white', fontsize=10, ha='center')

    ax.set_title("Contracts Over Time", fontsize=14, color='white', fontname="Arial", weight='bold')
    ax.set_xlabel("Date", color='white', fontsize=10, fontname="Arial")
    ax.set_ylabel(" Contracts", color='white', fontsize=10, fontname="Arial")
    ax.tick_params(axis='x', colors='white', labelrotation=45)
    ax.tick_params(axis='y', colors='white')
    ax.set_ylim(0, max(max(values), 5))
    ax.grid(True, linestyle='--', color='white', alpha=0.3)
    ax.legend(facecolor='#010132', edgecolor='white', labelcolor='white')

    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    return fig
