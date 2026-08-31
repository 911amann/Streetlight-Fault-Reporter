# Streetlight Fault Reporter

## Project Title
Streetlight Fault Reporter

## Domain
Smart City

## Problem Statement

Develop a decision-support application for streetlight fault reporting
that analyzes data and generates useful recommendations instead of
only storing records.

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- Text File Handling

## Core Features

1. Pole Tracking
2. Priority Assignment
3. Repair Tracking
4. Area-wise Reports
5. Maintenance Queue

## Python Concepts Used

- Variables
- Data Types
- Operators
- If-else statements
- For loops
- Functions
- Lists
- Dictionaries
- Sets
- List Comprehension
- Exception Handling
- Regular Expressions
- File Handling
- Flask

## How the Project Works

The user can report a streetlight fault by entering the pole number,
area, problem, severity and reporter details.

Python processes the information and automatically assigns a priority.

The data is stored in a text file.

The application can display all pole records, pending repairs,
area-wise reports and a maintenance queue.

High-priority faults are placed at the top of the maintenance queue.

## How to Run

Install Flask:

pip install flask

Run the application:

python app.py

Open The Link : http://127.0.0.1:5000

Then open the address shown by Flask in a web browser.

## Storage

The project uses a simple text file instead of a database or JSON file.

Data is stored in:

data/streetlights.txt
