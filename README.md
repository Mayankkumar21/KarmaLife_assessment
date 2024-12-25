# MongoDB Management Script

## Overview

This project demonstrates managing MongoDB data using Python and Pandas. It covers data insertion, retrieval, manipulation, analysis, and export/import operations with MongoDB. The database connection is secured using environment variables.

---

## Features

- **Secure Database Connection**: Fetches credentials from environment variables.
- **Data Management**: Performs CRUD operations on student data.
- **Data Analysis**: Computes statistics like average grades and age distribution.
- **Export/Import Support**: Handles JSON data export and import for easy data migration.
- **Error Handling**: Manages missing credentials and connection issues.

---

## Requirements

- Python 3.10 or higher
- MongoDB Atlas cluster

### Dependencies

Install the required packages using:

```bash
pip3 install -r requirements.txt
```

---

## Setup Instructions

### 1. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate      # On Linux/MacOS
venv\Scripts\activate         # On Windows
```

### 2. Create a `.env` File

#### Completed for this case

Add MongoDB credentials in the `.env` file:

```
MONGO_USER=your_username
MONGO_PASSWORD=your_password
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Script

```bash
python main.py
```

---

## Code Structure

- **`main.py`**: Contains the implementation for MongoDB connection, data management, and analysis.
- **`.env`**: Stores sensitive environment variables securely.
- **`requirements.txt`**: Lists all dependencies required for the project.

---

## Key Functions

- `init_mongo()`: Initializes MongoDB connection and validates credentials.
- `retrieve_students()`: Fetches and displays data based on query filters.
- `analyze_data()`: Performs statistical analysis on student data.
- `export_to_json()`: Handles data export and import operations.

---

## Notes

### Completed for this case

- Replace placeholder credentials in the `.env` file before running the code.
- Ensure the MongoDB cluster IP whitelist includes your current IP address.
