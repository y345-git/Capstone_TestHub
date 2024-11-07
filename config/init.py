from db_connection import db

def create_supervisors_table():
    # SQL command to create the supervisors table if it doesn't already exist
    create_table_query = """
   CREATE TABLE IF NOT EXISTS supervisors (
    id          INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each supervisor entry
    rfid        VARCHAR(50) UNIQUE,              -- Unique RFID for supervisor identification
    name        VARCHAR(50) NOT NULL,            -- Supervisor's name
    dept_code   VARCHAR(5) NOT NULL,             -- Department code, e.g., 'ME', 'CO'
    desg        VARCHAR(50) NOT NULL,            -- Designation, e.g., 'Lecturer', 'HOD'
    emp_type    VARCHAR(10),                     -- Employment type, e.g., 'Temp', 'Perm'
    post        VARCHAR(50),                     -- Additional post details, if any
    start_date  DATE,                            -- Start date for the role, if applicable
    end_date    DATE                             -- End date for the role, if applicable
    );
    """

    # Execute the SQL command
    try:
        db.exec(create_table_query)
        print("Table 'supervisors' created successfully (if it did not already exist).")
    except Exception as e:
        print(f"An error occurred while creating the table: {e}")

if __name__ == "__main__":
    create_supervisors_table()
