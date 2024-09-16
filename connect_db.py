import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='hotel_manager'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def get_hotels_data():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT h.region, h.name AS hotel_name, r.room_type, r.price, r.available_rooms
            FROM Hotels h
            JOIN Rooms r ON h.id = r.hotel_id
            """
            cursor.execute(query)
            results = cursor.fetchall()
            connection.close()
            return results
        except Error as e:
            print(f"Error executing query: {e}")
            return []
    return []

def get_reviews_data():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT h.name AS hotel_name, r.room_type, rv.name AS reviewer, rv.rating, rv.comment
            FROM Hotels h
            JOIN Rooms r ON h.id = r.hotel_id
            JOIN Reviews rv ON r.id = rv.room_id
            """
            cursor.execute(query)
            results = cursor.fetchall()
            connection.close()
            return results
        except Error as e:
            print(f"Error executing query: {e}")
            return []
    return []
def get_booking_history_data(username):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT b.date, h.name AS hotel_name, r.room_type, b.total_price, b.status
            FROM Bookings b
            JOIN Hotels h ON b.hotel_id = h.id
            JOIN Rooms r ON b.room_id = r.id
            WHERE b.username = %s
            """
            cursor.execute(query, (username,))
            results = cursor.fetchall()
            connection.close()
            return results
        except Error as e:
            print(f"Error executing query: {e}")
            return []
    return []

