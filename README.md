# Freelance Project Management System

A comprehensive desktop application designed to streamline the freelance ecosystem, connecting clients and freelancers through an intuitive platform for project management, payments, and communication.

## Table of Contents

- [📋 Overview](#-overview)
  - [Key Objectives](#key-objectives)
- [✨ Features](#-features)
  - [👥 For Clients](#-for-clients)
  - [🎯 For Freelancers](#-for-freelancers)
  - [📱 Communication Features](#-communication-features)
  - [🔄 Dual Role Support](#-dual-role-support)
- [🖼️ Screenshots](#-screenshots)
- [🏗️ Architecture](#-architecture)
  - [Project Structure](#project-structure)
- [🛠️ Technology Stack](#-technology-stack)
  - [Dependencies](#dependencies)
- [⚡ Installation](#-installation)
  - [Prerequisites](#prerequisites)
  - [Setup Steps](#setup-steps)
- [🚀 Usage](#-usage)
  - [Getting Started](#getting-started)
  - [Client Workflow](#client-workflow)
  - [Freelancer Workflow](#freelancer-workflow)
- [🗄️ Database Schema](#-database-schema)
  - [Core Entities](#core-entities)
  - [Database ERD](#database-erd).
- [📝 License](#-license)
- [About](#about)

## 📋 Overview

The Freelance Project Management System is a desktop application that provides a complete solution for managing freelance projects. It features dual dashboards for clients and freelancers, enabling seamless project creation, proposal submission, contract management, and secure payment processing.

### Key Objectives

- Simplify project management between clients and freelancers
- Provide transparent payment tracking and processing
- Enable real-time communication between parties
- Offer comprehensive analytics and reporting
- Support dual role functionality for hybrid users

## ✨ Features

### 👥 For Clients
- **📁 Project Management**
  - Create and manage projects with detailed descriptions
  - Set budgets and deadlines
  - Track project status (Open, Active, Completed)
  - Close or reopen projects as needed

- **📋 Proposal Management**
  - Review incoming proposals from freelancers
  - Accept or reject proposals
  - View detailed freelancer profiles
  - Track proposal statistics

- **💰 Payment Processing**
  - Secure payment methods (Bank Transfer, Credit Card, PayPal, JazzCash, EasyPaisa)
  - Rate and review freelancers
  - Track payment history
  - Generate payment reports

- **📊 Analytics Dashboard**
  - Top freelancers visualization
  - Payment trends over time
  - Contract statistics
  - Popular skills analysis

- **💬 Communication**
  - Built-in messaging system
  - Chat with freelancers
  - Message history
  - Real-time communication

### 🎯 For Freelancers
- **👤 Profile Management**
  - Comprehensive profile setup
  - Skills showcase
  - Portfolio description
  - Profile editing capabilities

- **🔍 Project Discovery**
  - Browse available projects
  - Filter by skills and budget
  - Submit competitive proposals
  - Track proposal status

- **📝 Contract Management**
  - View active contracts
  - Monitor project deadlines
  - Access client information
  - Track earnings

- **💳 Payment Tracking**
  - View payment history
  - Check pending payments
  - Access client reviews
  - Export payment reports

### 📱 Communication Features
- **💬 Integrated Messaging**
  - Real-time chat between clients and freelancers
  - Message history tracking
  - User-friendly interface
  - Available for both client and freelancer dashboards
  - Non-encrypted messaging (with disclaimer)

### 🔄 Dual Role Support
- Switch between client and freelancer accounts
- Maintain separate profiles for each role
- Unified dashboard experience

## 🖼️ Screenshots

#### 🔐 Login & Authentication

![login](https://github.com/user-attachments/assets/faeaea35-b1e7-44e9-8f1f-d82973743c65)

#### 👔 Client Dashboard

![client_dashboard](https://github.com/user-attachments/assets/9598d3b8-fdc9-49e9-8fbc-3a4b85b5e000)

#### 🎯 Freelancer Dashboard

![freelancer_dashboard](https://github.com/user-attachments/assets/0583dfa2-885f-4436-9cfd-12734cd95623)

#### 💬 Messaging System

![messaging](https://github.com/user-attachments/assets/05276346-b984-4d66-b0c7-5191ded93385)

#### 📊 Analytics Dashboard

![analytics](https://github.com/user-attachments/assets/16292e55-ecf2-4b00-90b0-fc2736d225b1)

## 🏗️ Architecture

### Project Structure

The application follows a modular architecture with the following key components:

```
freelance-project-management/
├── Client_Dashboard.py      # Client interface and functionality
├── Freelance_Dashboards.py  # Freelancer interface and functionality
├── login_screen.py          # Authentication and registration
├── db_connection.py         # Database operations
├── graphs.py               # Analytics and visualization
├── assets/                 # Images and icons
└── README.md              # Project documentation
```

## 🛠️ Technology Stack

- **Frontend**: Python Tkinter
- **Backend**: Python 3.7+
- **Database**: Microsoft SQL Server
- **Database Connector**: pyodbc
- **Data Visualization**: Matplotlib
- **Design**: Custom UI components with Tkinter

### Dependencies

```
pyodbc>=4.0.35
matplotlib>=3.5.0
```

## ⚡ Installation

### Prerequisites

- Python 3.7 or higher
- Microsoft SQL Server
- ODBC Driver 17 for SQL Server

### Setup Steps

1. **📥 Download the Project**
   - Download the FMS (main folder) containing all project files
   - Extract to your preferred location

2. **📦 Install dependencies**
   ```bash
   pip install pyodbc matplotlib
   ```

3. **🗄️ Database Setup**
   - Import the provided database file (included in FMS folder)
   - OR Create a database named `Freelance`
   - Update database connection settings in `db_connection.py`:
     ```python
     "SERVER=YOUR_SERVER_NAME;"
     "DATABASE=Freelance;"
     ```

4. **🖼️ Assets Ready**
   All required images are included in the FMS folder:
   - `Logo.png` - Main application logo
   - `CLogo.png` - Secondary logo
   - `login_bg.png` - Login background image

5. **▶️ Run the application**
   ```bash
   python login_screen.py
   ```

## 🚀 Usage

### Getting Started

#### 🎬 First-Time Setup

1. Launch the application
2. Create a new account (Client or Freelancer)
3. For freelancers: Complete profile setup with skills selection
4. For clients: Start creating projects immediately

### Client Workflow

#### 👔 Managing Projects

1. **📝 Create Project**: Define project details, budget, and deadline
2. **📋 Review Proposals**: Evaluate freelancer submissions
3. **✅ Accept Proposal**: Create contract with selected freelancer
4. **🔍 Monitor Progress**: Track project status
5. **💰 Process Payment**: Complete payment with ratings

### Freelancer Workflow

#### 🎯 Building Your Career

1. **👤 Complete Profile**: Add skills and description
2. **🔍 Browse Projects**: Find suitable opportunities
3. **📨 Submit Proposals**: Send competitive bids
4. **📝 Manage Contracts**: Work on accepted projects
5. **💳 Track Payments**: Monitor earnings and reviews

## 🗄️ Database Schema

### Core Entities

The system uses a relational database with the following core entities:

- **👤 Users**: Stores client and freelancer profiles
- **📁 Projects**: Manages project listings and details
- **📋 Proposals**: Handles freelancer submissions
- **📝 Contracts**: Tracks active work agreements
- **💰 Payments**: Records transaction history
- **💬 Messages**: Enables communication
- **🛠️ Skills**: Manages freelancer capabilities
- **⭐ Reviews**: Stores client feedback

All tables are properly normalized with appropriate foreign keys and relationships. The complete database schema is included in the FMS folder.

### Datbase ERD

![Database ERD](https://github.com/user-attachments/assets/6eeb29bd-82d1-4429-af28-022c436ddc81)

## 📝 License

This project is licensed under the [MIT License](LICENSE.md)

## About

**Disclaimer**: This application is for educational and demonstration purposes. Ensure proper security measures before using in production environments.

For questions or support, please contact us through GitHub issues.

---

© 2025 Freelance Management System. All rights reserved.
