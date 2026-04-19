import oracledb
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = oracledb.connect(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                dsn=os.getenv("DB_DSN")
            )
    print("Connected to Oracle DB")
except Exception as e:
    print("Connection failed:", e)
    exit()

cursor = conn.cursor()

tables = [

    """CREATE TABLE stops (
        stop_id NUMBER PRIMARY KEY,
        stop_name VARCHAR2(100) NOT NULL,
        landmark VARCHAR2(100),
        latitude NUMBER(10,6),
        longitude NUMBER(10,6)
    )""",

    """CREATE TABLE buses (
        bus_id NUMBER PRIMARY KEY,
        bus_number VARCHAR2(30) UNIQUE NOT NULL,
        model VARCHAR2(50),
        bus_type VARCHAR2(20),
        is_active NUMBER(1) DEFAULT 1 CHECK(is_active IN (0,1))
    )""",

    """CREATE TABLE drivers (
        driver_id NUMBER PRIMARY KEY,
        name VARCHAR2(50) NOT NULL,
        phone_no VARCHAR2(20),
        license_number VARCHAR2(50) UNIQUE,
        experience_years NUMBER,
        photo_url VARCHAR2(100),
        is_active NUMBER(1) DEFAULT 1 CHECK(is_active IN (0,1))
    )""",

    """CREATE TABLE users (
        user_id NUMBER PRIMARY KEY,
        name VARCHAR2(50) NOT NULL,
        phone_no VARCHAR2(20),
        email VARCHAR2(50) UNIQUE NOT NULL,
        password VARCHAR2(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",

    """CREATE TABLE routes (
        route_id NUMBER PRIMARY KEY,
        route_number VARCHAR2(20) UNIQUE NOT NULL,
        route_name VARCHAR2(50),
        is_active NUMBER(1) DEFAULT 1 CHECK(is_active IN (0,1)),
        total_distance NUMBER(10,6),
        start_stop_id NUMBER,
        end_stop_id NUMBER,
        frequency_minutes NUMBER,
        CONSTRAINT fk_route_start FOREIGN KEY(start_stop_id) REFERENCES stops(stop_id),
        CONSTRAINT fk_route_end FOREIGN KEY(end_stop_id) REFERENCES stops(stop_id)
    )""",

    """CREATE TABLE route_stops (
        route_stops_id NUMBER PRIMARY KEY,
        route_id NUMBER NOT NULL,
        stop_id NUMBER NOT NULL,
        stop_sequence NUMBER NOT NULL,
        distance_from_start NUMBER(8,2),
        minutes_from_start NUMBER,
        CONSTRAINT fk_rs_route FOREIGN KEY (route_id) REFERENCES routes(route_id),
        CONSTRAINT fk_rs_stop FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
    )""",

    """CREATE TABLE assignments (
        assignment_id NUMBER PRIMARY KEY,
        bus_id NUMBER NOT NULL,
        driver_id NUMBER NOT NULL,
        route_id NUMBER NOT NULL,
        assignment_day VARCHAR2(20),
        departure_time VARCHAR2(5),
        arrival_time VARCHAR2(5),
        shift VARCHAR2(20),
        CONSTRAINT fk_assign_bus FOREIGN KEY(bus_id) REFERENCES buses(bus_id),
        CONSTRAINT fk_assign_driver FOREIGN KEY(driver_id) REFERENCES drivers(driver_id),
        CONSTRAINT fk_assign_route FOREIGN KEY(route_id) REFERENCES routes(route_id)
    )""",

    """CREATE TABLE fares (
        fare_id NUMBER PRIMARY KEY,
        route_id NUMBER NOT NULL,
        from_sequence NUMBER,
        to_sequence NUMBER,
        fare_amt NUMBER(8,2),
        CONSTRAINT fk_fares_route FOREIGN KEY(route_id) REFERENCES routes(route_id)
    )""",

    """CREATE TABLE search_history (
        history_id NUMBER PRIMARY KEY,
        user_id NUMBER NOT NULL,
        from_stop_id NUMBER,
        to_stop_id NUMBER,
        searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        result_snapshot VARCHAR2(2000),
        CONSTRAINT fk_search_user FOREIGN KEY(user_id) REFERENCES users(user_id),
        CONSTRAINT fk_search_from_stop FOREIGN KEY(from_stop_id) REFERENCES stops(stop_id),
        CONSTRAINT fk_search_to_stop FOREIGN KEY(to_stop_id) REFERENCES stops(stop_id)
    )"""
]

for table in tables:
    try:
        cursor.execute(table)
        print("Table created")
    except Exception as e:
        print("Table exists:", e)


# USERS
users_data = [
    (1, 'Mike Smith', '9999999999', 'mike@example.com', 'pass123'),
    (2, 'John Doe', '8888888888', 'john@example.com', 'pass456'),
    (3, 'Alice Brown', '7777777777', 'alice@example.com', 'pass789')
]

for user in users_data:
    try:
        cursor.execute("""
            INSERT INTO users (user_id, name, phone_no, email, password)
            VALUES (:1, :2, :3, :4, :5)
        """, user)
    except:
        pass

# STOPS
try:
    cursor.execute("""
        INSERT ALL
          INTO stops (stop_id, stop_name) VALUES (1, 'A')
          INTO stops (stop_id, stop_name) VALUES (2, 'B')
          INTO stops (stop_id, stop_name) VALUES (3, 'C')
          INTO stops (stop_id, stop_name) VALUES (4, 'D')
          INTO stops (stop_id, stop_name) VALUES (5, 'E')
          INTO stops (stop_id, stop_name) VALUES (6, 'F')
          INTO stops (stop_id, stop_name) VALUES (7, 'G')
        SELECT * FROM dual
    """)
    print("Stops inserted")
except:
    print("Stops already exist")

# BUSES
try:
    cursor.execute("""
        INSERT ALL
          INTO buses (bus_id, bus_number, bus_type, is_active) VALUES (1, 'B-001', 'govt', 1)
          INTO buses (bus_id, bus_number, bus_type, is_active) VALUES (2, 'B-002', 'govt', 1)
          INTO buses (bus_id, bus_number, bus_type, is_active) VALUES (3, 'B-003', 'pvt', 1)
        SELECT * FROM dual
    """)
    print("Buses inserted")
except:
    print("Buses already exist")

# DRIVERS
try:
    cursor.execute("""
        INSERT ALL
          INTO drivers (driver_id, name, is_active) VALUES (1, 'Ram', 1)
          INTO drivers (driver_id, name, is_active) VALUES (2, 'Gopal', 1)
          INTO drivers (driver_id, name, is_active) VALUES (3, 'Sekhar', 1)
        SELECT * FROM dual
    """)
except:
    pass

# ROUTES
try:
    cursor.execute("""
        INSERT ALL
          INTO routes (route_id, route_number, route_name, total_distance, start_stop_id, end_stop_id, frequency_minutes) 
            VALUES (1, 'R1', 'Route 1', 25, 1, 6, 20)
          INTO routes (route_id, route_number, route_name, total_distance, start_stop_id, end_stop_id, frequency_minutes) 
            VALUES (2, 'R2', 'Route 2', 33, 5, 6, 25)
          INTO routes (route_id, route_number, route_name, total_distance, start_stop_id, end_stop_id, frequency_minutes) 
            VALUES (3, 'R3', 'Route 3', 29, 6, 5, 30)
        SELECT * FROM dual
    """)
except:
    pass

conn.commit()
print("All data inserted")

cursor.close()
conn.close()

print("Connection closed")