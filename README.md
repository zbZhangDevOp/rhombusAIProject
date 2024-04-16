# rhombusAIProject

## Overview
The rhombusAIProject is designed to process data through a web interface, allowing users to upload CSV files, view information, and modify data types. The system is divided into two main components: a frontend web server and a backend server.

## Getting Started

### Prerequisites
- Node.js and npm (for the frontend)
- Python and Django (for the backend)

### Setting Up the Frontend

1. **Navigate to the Frontend Directory:**
   ```bash
   cd data-processor-frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```
3. **Start Development Server**
   ```bash
   npm run dev
   ```

### Setting Up the Backend

1. **Navigate to the Backend Directory:**
   ```bash
   cd data-processor-backend
   ```

2. **Install Dependencies**
   ```bash
    pip install django-cors-headers
    pip install pandas
   ```
3. **Start Development Server**
   ```bash
   python3 manage.py runserver
   ```


## Usage

### Access the Frontend:
- Navigate to the frontend URL, typically http://localhost:5173/, once both servers are running.

## Upload a CSV File:
- Click on the "Choose Files" section.
- Select the CSV file you wish to upload.
- Click the "Upload" button to upload the file.

## Manage Data:
- After uploading, users can access the uploaded data.
- Users have the option to change the data types directly through the web interface.