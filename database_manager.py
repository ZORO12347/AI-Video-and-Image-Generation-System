import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

class DatabaseManager:
    def __init__(self):
        try:
            # Establish connection to MySQL database
            self.conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT", 3306)),  # Default to 3306 if not provided
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                connection_timeout=10  # Timeout for database connection
            )
            self.cursor = self.conn.cursor(dictionary=True)  # Return rows as dictionaries
            print("Database connection successful")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise

    def create_tables(self):
        """
        Create the content_generation table if it doesn't exist.
        """
        try:
            query = """
            CREATE TABLE IF NOT EXISTS content_generation (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                prompt TEXT NOT NULL,
                video_paths JSON,
                image_paths JSON,
                status VARCHAR(50) DEFAULT 'Processing',
                generated_at DATETIME
            )
            """
            self.cursor.execute(query)
            self.conn.commit()
            print("Tables created successfully")
        except Error as e:
            print(f"Error creating tables: {e}")
            raise

    def insert_generation_record(self, user_id, prompt):
        """
        Insert a new record into the content_generation table.
        """
        try:
            query = """
            INSERT INTO content_generation (user_id, prompt, status, generated_at)
            VALUES (%s, %s, 'Processing', NOW())
            """
            self.cursor.execute(query, (user_id, prompt))
            self.conn.commit()
            print(f"Record inserted successfully for user_id: {user_id}")
            return self.cursor.lastrowid
        except Error as e:
            print(f"Error inserting record: {e}")
            raise

    def update_generation_status(self, record_id, video_paths, image_paths):
        """
        Update the record with completed status and generated paths.
        """
        try:
            query = """
            UPDATE content_generation
            SET video_paths = %s, image_paths = %s, status = 'Completed'
            WHERE id = %s
            """
            self.cursor.execute(query, (json.dumps(video_paths), json.dumps(image_paths), record_id))
            self.conn.commit()
            print(f"Record {record_id} updated successfully with paths")
        except Error as e:
            print(f"Error updating record: {e}")
            raise

    def fetch_user_content(self, user_id):
        """
        Fetch content generation records for a user by user_id.
        """
        try:
            query = "SELECT * FROM content_generation WHERE user_id = %s"
            self.cursor.execute(query, (user_id,))
            results = self.cursor.fetchall()
            print(f"Fetched {len(results)} records for user_id: {user_id}")
            return results
        except Error as e:
            print(f"Error fetching user content: {e}")
            raise

    def close_connection(self):
        """
        Close the database connection gracefully.
        """
        try:
            if self.conn.is_connected():
                self.cursor.close()
                self.conn.close()
                print("Database connection closed")
        except Error as e:
            print(f"Error closing connection: {e}")

