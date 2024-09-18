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
#DATA CỦA GUEST DASHBOARD
def get_hotels_data():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT reg.region_name AS region, h.hotel_name, r.room_type, r.price, 
                   COUNT(r.room_id) AS available_rooms
            FROM Hotels h
            JOIN Regions reg ON h.region_id = reg.region_id
            JOIN Rooms r ON h.hotel_id = r.hotel_id
            WHERE r.status = 'available'
            GROUP BY reg.region_name, h.hotel_name, r.room_type, r.price
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
            SELECT h.hotel_name, u.username AS reviewer, hr.rating, hr.comment
            FROM Hotels h
            JOIN HotelReviews hr ON h.hotel_id = hr.hotel_id
            JOIN Users u ON hr.user_id = u.user_id
            """
            cursor.execute(query)
            results = cursor.fetchall()
            connection.close()
            return results
        except Error as e:
            print(f"Error executing query: {e}")
            return []
    return []

#DATA CỦA HISTORY
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

#DATA CỦA ADMIN DASHBOARD
def get_user_data():
    con = create_connection()
    if con:
        cursor = con.cursor(dictionary=True)
        query = "SELECT username, CASE WHEN user_type = 'guest' THEN 'Guest' WHEN user_type = 'admin' THEN 'Admin' END AS role FROM Users;"
        cursor.execute(query)
        results = cursor.fetchall()
        con.close()
        return results
    else:
        print("Loi !")
    return []
        
def get_booking_data():
    con = create_connection()
    if con:
        cursor = con.cursor(dictionary=True)
        query = """SELECT r.room_type AS room, 
                        h.hotel_name AS hotel, 
                        b.status, 
                        r.price, 
                        reg.region_name AS region
                    FROM Bookings b
                        JOIN Rooms r ON b.room_id = r.room_id
                        JOIN Hotels h ON r.hotel_id = h.hotel_id
                        JOIN Regions reg ON h.region_id = reg.region_id;
                """
        cursor.execute(query)
        results = cursor.fetchall()
        con.close()
        return results
    else:
        print("Loi !")
    return []

# Hàm lấy dữ liệu thống kê phòng theo loại
def get_room_stats():
    con = create_connection()
    if con:
        cursor = con.cursor(dictionary=True)
        query = """
        SELECT room_type, COUNT(*) AS total_rooms
        FROM Rooms r
        JOIN Bookings b ON r.room_id = b.room_id
        GROUP BY room_type;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        con.close()
        room_stats = {result['room_type'].title() + " Room": result['total_rooms'] for result in results}
        return room_stats
    return {}

# Hàm lấy dữ liệu doanh thu theo khu vực
def get_region_revenue():
    con = create_connection()
    if con:
        cursor = con.cursor(dictionary=True)
        query = """
        SELECT reg.region_name, SUM(b.total_price) AS region_revenue
        FROM Bookings b
        JOIN Rooms r ON b.room_id = r.room_id
        JOIN Hotels h ON r.hotel_id = h.hotel_id
        JOIN Regions reg ON h.region_id = reg.region_id
        GROUP BY reg.region_name;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        con.close()
        region_revenue = {result['region_name']: result['region_revenue'] for result in results}
        return region_revenue
    return {}

# Hàm lấy dữ liệu doanh thu theo khách sạn
def get_hotel_revenue():
    con = create_connection()
    if con:
        cursor = con.cursor(dictionary=True)
        query = """
        SELECT h.hotel_name, SUM(b.total_price) AS hotel_revenue
        FROM Bookings b
        JOIN Rooms r ON b.room_id = r.room_id
        JOIN Hotels h ON r.hotel_id = h.hotel_id
        GROUP BY h.hotel_name;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        con.close()
        hotel_revenue = {result['hotel_name']: result['hotel_revenue'] for result in results}
        return hotel_revenue
    return {}

# Hàm tổng hợp dữ liệu revenue_data
def get_revenue_data():
    return {
        "Room Stats": get_room_stats(),
        "Region Revenue": get_region_revenue(),
        "Hotel Revenue": get_hotel_revenue()
    }
