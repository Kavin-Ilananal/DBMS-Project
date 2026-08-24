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
cursor.execute("Drop table search_history")
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

    """create table search_history
        (
            history_id number primary key,
            user_id number not null,
            from_stop_id number,
            to_stop_id number,
            time varchar2(5),
            day varchar2(20),
            searched_at timestamp default current_timestamp,
            result_snapshot varchar2(2000),      --we can have a json or something
            constraint fk_search_user foreign key(user_id) references users(user_id),
            constraint fk_search_from_stop foreign key(from_stop_id) references stops(stop_id),
            constraint fk_search_to_stop foreign key(to_stop_id) references stops(stop_id)
        )"""
]

for table in tables:
    try:
        cursor.execute(table)
        print("Table created")
    except Exception as e:
        print("Table exists:", e)

try:
    cursor.execute("CREATE SEQUENCE search_history_seq START WITH 1 INCREMENT BY 1")
    print("Sequence created")
except Exception as e:
    print("Sequence exists:", e)
conn.commit()
try:
    cursor.execute("""
    CREATE OR REPLACE TRIGGER trg_history_auto_id
    BEFORE INSERT ON search_history
    FOR EACH ROW
    BEGIN
        IF :NEW.history_id IS NULL THEN
            SELECT search_history_seq.NEXTVAL INTO :NEW.history_id FROM dual;
        END IF;
    END;
    """)
    print("Trigger1 created")
except Exception as e:
    print("Trigger1 exists:", e)

try:
    cursor.execute("""
    CREATE OR REPLACE TRIGGER trg_prevent_invalid_search
    BEFORE INSERT ON search_history
    FOR EACH ROW
    BEGIN
        IF :NEW.from_stop_id = :NEW.to_stop_id THEN
            RAISE_APPLICATION_ERROR(-20001,
            'Invalid Search: The starting stop and destination stop cannot be the same.');
        END IF;
    END;
    """)
    print("Trigger2 created")
except Exception as e:
    print("Trigger2 exists:", e)
# USERS
users_data = [
    (4, 'Mike Smith', '9999999999', 'mike@example.com', 'pass123'),
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

conn.commit()
print("All data inserted")

cursor.close()
conn.close()

print("Connection closed")