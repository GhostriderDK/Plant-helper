# Plant Helper Project Setup Guide

Welcome to the Plant Helper project! This guide will walk you through setting up the project from scratch.

## Prerequisites

Before you begin, ensure you have the following installed:
- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/) (version 14 or higher)
- [npm](https://www.npmjs.com/) (comes with Node.js)

## Steps

### 1. Clone the Repository

Open your terminal and run the following command to clone the repository:

```sh
git clone https://github.com/GhostriderDK/Plant-helper.git
```

### 2. Navigate to the Project Directory

Change to the project directory:

```sh
cd Plant-helper/Flask
```



### 3. Set Up Environment Variables

Create a `.env` file in the root directory and add the necessary environment variables. For example:

```env
```sh
# Windows
python -m venv venv
venv\Scripts\activate

# Linux and macOS
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

Install the required dependencies using pip:

```sh
pip install -r requirements.txt
```

after this you can run 
```sh
python3 app.py
```

and open your virtual enviroment in another terminal and run
```sh
python3 log_data.py
```
to log data to the database (if you have set up the database)


### 5. setup the database

### 5. Setup the Database

To set up the database for the `log_data.py` and `get_data.py` scripts, follow these steps:

1. Open your terminal and navigate to the project directory:

    ```sh
    cd Plant-helper/Flask
    ```

2. Create a new SQLite database file:

    ```sh
    sqlite3 plant_helper.db
    ```

3. Once inside the SQLite shell, create the necessary tables:

    ```sql
    CREATE TABLE IF NOT EXISTS plants (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      species TEXT NOT NULL,
      watering_frequency INTEGER NOT NULL,
      last_watered DATE
    );

    CREATE TABLE IF NOT EXISTS watering_logs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      plant_id INTEGER NOT NULL,
      date DATE NOT NULL,
      FOREIGN KEY (plant_id) REFERENCES plants (id)
    );
    ```

4. Exit the SQLite shell:

    ```sh
    .exit
    ```

5. You have now successfully set up the database for the `log_data.py` and `get_data.py` scripts.

Note: Make sure to update the database connection string in both `log_data.py` and `get_data.py` to point to the newly created `plant_helper.db` file.

### 6. Start the Development Server

- *** step will come at a later date ***

### 7. Access the Application

Open your browser and navigate to `http://localhost:5000` to see the application in action.

Happy coding!

