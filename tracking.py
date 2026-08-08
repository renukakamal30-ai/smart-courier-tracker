import sqlite3
import uuid
from datetime import datetime


DATABASE_NAME = "courier.db"


class CourierTrackingSystem:
    """Handles courier records, tracking IDs, statuses, and tracking history."""

    STATUS_STAGES = [
        "Booked",
        "Picked Up",
        "In Transit",
        "Arrived at Hub",
        "Out for Delivery",
        "Delivered",
    ]

    def __init__(self, database=DATABASE_NAME):
        self.database = database
        self.create_tables()

    def get_connection(self):
        """Create and return a SQLite database connection."""
        connection = sqlite3.connect(self.database)
        connection.row_factory = sqlite3.Row
        return connection

    def create_tables(self):
        """Create the required database tables."""
        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS couriers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_id TEXT UNIQUE NOT NULL,
                sender_name TEXT NOT NULL,
                sender_phone TEXT,
                receiver_name TEXT NOT NULL,
                receiver_phone TEXT,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                package_description TEXT,
                weight REAL,
                current_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracking_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_id TEXT NOT NULL,
                status TEXT NOT NULL,
                location TEXT,
                remarks TEXT,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (tracking_id)
                    REFERENCES couriers(tracking_id)
                    ON DELETE CASCADE
            )
        """)

        connection.commit()
        connection.close()

    def generate_tracking_id(self):
        """Generate a unique tracking ID."""
        while True:
            tracking_id = "CR" + uuid.uuid4().hex[:10].upper()

            connection = self.get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "SELECT tracking_id FROM couriers WHERE tracking_id = ?",
                (tracking_id,)
            )

            exists = cursor.fetchone()
            connection.close()

            if not exists:
                return tracking_id

    def add_courier(
        self,
        sender_name,
        sender_phone,
        receiver_name,
        receiver_phone,
        origin,
        destination,
        package_description,
        weight
    ):
        """Add a new courier and return its tracking ID."""

        tracking_id = self.generate_tracking_id()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO couriers (
                tracking_id,
                sender_name,
                sender_phone,
                receiver_name,
                receiver_phone,
                origin,
                destination,
                package_description,
                weight,
                current_status,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tracking_id,
            sender_name,
            sender_phone,
            receiver_name,
            receiver_phone,
            origin,
            destination,
            package_description,
            weight,
            "Booked",
            current_time,
            current_time
        ))

        cursor.execute("""
            INSERT INTO tracking_history (
                tracking_id,
                status,
                location,
                remarks,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            tracking_id,
            "Booked",
            origin,
            "Courier booking created",
            current_time
        ))

        connection.commit()
        connection.close()

        return tracking_id

    def update_status(self, tracking_id, new_status, location="", remarks=""):
        """Update courier delivery status."""

        if new_status not in self.STATUS_STAGES:
            return False, (
                f"Invalid status. Choose from: "
                f"{', '.join(self.STATUS_STAGES)}"
            )

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT current_status FROM couriers WHERE tracking_id = ?",
            (tracking_id,)
        )

        courier = cursor.fetchone()

        if not courier:
            connection.close()
            return False, "Tracking ID not found."

        current_status = courier["current_status"]

        # Prevent moving backwards in the delivery process.
        current_index = self.STATUS_STAGES.index(current_status)
        new_index = self.STATUS_STAGES.index(new_status)

        if new_index < current_index:
            connection.close()
            return False, (
                f"Cannot move status backwards from "
                f"'{current_status}' to '{new_status}'."
            )

        if new_index == current_index:
            connection.close()
            return False, f"Courier is already marked as '{new_status}'."

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            UPDATE couriers
            SET current_status = ?, updated_at = ?
            WHERE tracking_id = ?
        """, (
            new_status,
            current_time,
            tracking_id
        ))

        cursor.execute("""
            INSERT INTO tracking_history (
                tracking_id,
                status,
                location,
                remarks,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            tracking_id,
            new_status,
            location,
            remarks,
            current_time
        ))

        connection.commit()
        connection.close()

        return True, f"Status updated to '{new_status}'."

    def get_courier(self, tracking_id):
        """Return courier details using a tracking ID."""

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM couriers
            WHERE tracking_id = ?
        """, (tracking_id,))

        courier = cursor.fetchone()
        connection.close()

        return courier

    def get_tracking_history(self, tracking_id):
        """Return the complete tracking history."""

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT status, location, remarks, updated_at
            FROM tracking_history
            WHERE tracking_id = ?
            ORDER BY id ASC
        """, (tracking_id,))

        history = cursor.fetchall()
        connection.close()

        return history

    def track_courier(self, tracking_id):
        """Return courier details and its complete tracking history."""

        courier = self.get_courier(tracking_id)

        if not courier:
            return None, []

        history = self.get_tracking_history(tracking_id)

        return courier, history

    def get_all_couriers(self):
        """Return all courier records."""

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                tracking_id,
                sender_name,
                receiver_name,
                origin,
                destination,
                current_status,
                created_at,
                updated_at
            FROM couriers
            ORDER BY id DESC
        """)

        couriers = cursor.fetchall()
        connection.close()

        return couriers