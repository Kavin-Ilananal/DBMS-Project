import oracledb
from datetime import datetime, timedelta
import random

conn = oracledb.connect(
    user="system",
    password="oracle123",
    dsn="localhost:1521/XEPDB1"
)

cursor = conn.cursor()

cursor.execute("DELETE FROM fares")
cursor.execute("DELETE FROM assignments")
cursor.execute("DELETE FROM route_stops")
cursor.execute("DELETE FROM drivers")
cursor.execute("DELETE FROM buses")
cursor.execute("DELETE FROM routes")
cursor.execute("DELETE FROM stops")

# ─────────────────────────────────────────────
# 1. STOPS (batch 1: IDs 1–7)
# ─────────────────────────────────────────────
stops_batch1 = [
    (1,  'Gandhipuram',     'Bus Stand',        11.0168, 76.9558),
    (2,  'RS Puram',        'Shopping Area',    11.0080, 76.9446),
    (3,  'Ukkadam',         'Bus Hub',          10.9916, 76.9586),
    (4,  'Singanallur',     'Lake Area',        10.9985, 77.0322),
    (5,  'Peelamedu',       'Airport Area',     11.0310, 77.0390),
    (6,  'Saravanampatti',  'IT Hub',           11.0820, 76.9990),
    (7,  'Vadavalli',       'Residential Area', 11.0250, 76.9000),
]
cursor.executemany(
    "INSERT INTO stops VALUES (:1,:2,:3,:4,:5)",
    stops_batch1
)
print(f"Inserted {len(stops_batch1)} stops (batch 1)")
 
# ─────────────────────────────────────────────
# 2. STOPS (batch 2: IDs 8–11)
# ─────────────────────────────────────────────
stops_batch2 = [
    (8,  'Saibaba Colony', 'Residential Hub',    11.0265, 76.9510),
    (9,  'Race Course',    'City Center',        11.0053, 76.9670),
    (10, 'Podanur',        'Railway Junction',   10.9580, 76.9850),
    (11, 'Ganapathy',      'Industrial Area',    11.0400, 76.9675),
]
cursor.executemany(
    "INSERT INTO stops VALUES (:1,:2,:3,:4,:5)",
    stops_batch2
)
print(f"Inserted {len(stops_batch2)} stops (batch 2)")
 
# ─────────────────────────────────────────────
# 3. BUSES (IDs 1–15)
# ─────────────────────────────────────────────
buses_batch1 = [
    (
        i,
        'B-' + str(i).zfill(3),
        'pvt' if i % 3 == 0 else 'govt',
        1
    )
    for i in range(1, 16)
]
cursor.executemany(
    "INSERT INTO buses (bus_id, bus_number, bus_type, is_active) VALUES (:1,:2,:3,:4)",
    buses_batch1
)
print(f"Inserted {len(buses_batch1)} buses (batch 1, IDs 1-15)")
 
# ─────────────────────────────────────────────
# 4. BUSES (IDs 16–20)
# ─────────────────────────────────────────────
buses_batch2 = [
    (
        i,
        'B-' + str(i).zfill(3),
        'pvt' if i % 2 == 0 else 'govt',
        1
    )
    for i in range(16, 21)
]
cursor.executemany(
    "INSERT INTO buses (bus_id, bus_number, bus_type, is_active) VALUES (:1,:2,:3,:4)",
    buses_batch2
)
print(f"Inserted {len(buses_batch2)} buses (batch 2, IDs 16-20)")
 
# ─────────────────────────────────────────────
# 5. DRIVERS (IDs 1–15)
# ─────────────────────────────────────────────
drivers_batch1 = [
    (
        i,
        'Driver_' + str(i),
        '9' + str(900000000 + i),
        'LIC' + str(i),
        (i % 10) + 1,
        'photo_' + str(i),
        1
    )
    for i in range(1, 16)
]
cursor.executemany(
    """INSERT INTO drivers
       (driver_id, name, phone_no, license_number, experience_years, photo_url, is_active)
       VALUES (:1,:2,:3,:4,:5,:6,:7)""",
    drivers_batch1
)
print(f"Inserted {len(drivers_batch1)} drivers (batch 1, IDs 1-15)")
 
# ─────────────────────────────────────────────
# 6. DRIVERS (IDs 16–20)
# ─────────────────────────────────────────────
drivers_batch2 = [
    (
        i,
        'Driver_' + str(i),
        '9' + str(900000000 + i),
        'LIC' + str(i),
        (i % 12) + 2,
        'photo_' + str(i),
        1
    )
    for i in range(16, 21)
]
cursor.executemany(
    """INSERT INTO drivers
       (driver_id, name, phone_no, license_number, experience_years, photo_url, is_active)
       VALUES (:1,:2,:3,:4,:5,:6,:7)""",
    drivers_batch2
)
print(f"Inserted {len(drivers_batch2)} drivers (batch 2, IDs 16-20)")
 
# ─────────────────────────────────────────────
# 7. ROUTES
# ─────────────────────────────────────────────
# Clear existing routes first (mirrors the SQL's DELETE FROM routes)
print("Cleared existing routes")
 
routes_data = [
    (1, 'R1A', 'Gandhipuram - Ukkadam Loop',             1, 22, 1,  3,  45),
    (2, 'R2B', 'RS Puram - Singanallur Line',             1, 28, 2,  4,  50),
    (3, 'R3C', 'Ukkadam - Podanur Route',                 1, 30, 3,  10, 60),
    (4, 'R4D', 'Peelamedu - Race Course Express',         1, 18, 5,  9,  45),
    (5, 'R5E', 'Saravanampatti - Gandhipuram Tech Route', 1, 25, 6,  1,  50),
    (6, 'R6F', 'Vadavalli - Saibaba Colony Connector',    1, 20, 7,  8,  60),
    (7, 'R7G', 'Ganapathy - Singanallur Circular',        1, 32, 11, 4,  45),
]
cursor.executemany(
    """INSERT INTO routes
       (route_id, route_number, route_name, is_active, total_distance,
        start_stop_id, end_stop_id, frequency_minutes)
       VALUES (:1,:2,:3,:4,:5,:6,:7,:8)""",
    routes_data
)
print(f"Inserted {len(routes_data)} routes")
 
# ─────────────────────────────────────────────
# 8. ROUTE_STOPS
# ─────────────────────────────────────────────
route_stops_data = [
    # (rs_id, route_id, stop_id, stop_sequence, distance_from_start, travel_time)
    (401, 4, 5,  1, 0,  0),
    (402, 4, 9,  2, 6,  10),
    (501, 5, 6,  1, 0,  0),
    (502, 5, 1,  2, 7,  12),
    (503, 5, 9, 3, 15, 25),
    (601, 6, 7,  1, 0,  0),
    (602, 6, 8,  2, 5,  15),
    (603, 6, 1, 3, 12, 25),
    (701, 7, 11, 1, 0,  0),
    (702, 7, 4,  2, 10, 20),
]
cursor.executemany(
    "INSERT INTO route_stops VALUES (:1,:2,:3,:4,:5,:6)",
    route_stops_data
)
print(f"Inserted {len(route_stops_data)} route_stops")
 
# ─────────────────────────────────────────────
# 9. FARES (batch 1 — fare_id starts at ROWNUM = 1)
# ─────────────────────────────────────────────
cursor.execute("""
    INSERT INTO fares (fare_id, route_id, from_sequence, to_sequence, fare_amt)
    SELECT
        ROWNUM,
        rs1.route_id,
        rs1.stop_sequence,
        rs2.stop_sequence,
        (rs2.distance_from_start - rs1.distance_from_start) * 1.2
    FROM route_stops rs1
    JOIN route_stops rs2
      ON rs1.route_id = rs2.route_id
     AND rs1.stop_sequence < rs2.stop_sequence
""")
print(f"Inserted fares batch 1 ({cursor.rowcount} rows, multiplier 1.2)")
 
# ─────────────────────────────────────────────
# 10. FARES (batch 2 — fare_id offset +100, multiplier 1.5)
# ─────────────────────────────────────────────
cursor.execute("""
    INSERT INTO fares (fare_id, route_id, from_sequence, to_sequence, fare_amt)
    SELECT
        ROWNUM + 100,
        rs1.route_id,
        rs1.stop_sequence,
        rs2.stop_sequence,
        (rs2.distance_from_start - rs1.distance_from_start) * 1.5
    FROM route_stops rs1
    JOIN route_stops rs2
      ON rs1.route_id = rs2.route_id
     AND rs1.stop_sequence < rs2.stop_sequence
""")
print(f"Inserted fares batch 2 ({cursor.rowcount} rows, multiplier 1.5)")
 
# ─────────────────────────────────────────────
# 11. ASSIGNMENTS
# ─────────────────────────────────────────────
routes_schedule = {
    1: (45, 38),
    2: (50, 48),
    3: (60, 47),
    4: (45, 25),
    5: (50, 32),
    6: (60, 28),
    7: (45, 35)
}
all_buses   = list(range(1, 20))
all_drivers = list(range(1, 20))
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
 
assignments = []
assignment_id = 1
 
for day in days:
    for route_id, (freq, duration) in routes_schedule.items():
        time_cursor = datetime.strptime("08:00", "%H:%M")
        end_time    = datetime.strptime("20:00", "%H:%M")
        used_buses   = {}
        used_drivers = {}
 
        while time_cursor <= end_time:
            bus    = random.choice(all_buses)
            driver = random.choice(all_drivers)
 
            if bus    in used_buses   and used_buses[bus]       > time_cursor:
                continue
            if driver in used_drivers and used_drivers[driver]  > time_cursor:
                continue
 
            dep = time_cursor
            arr = dep + timedelta(minutes=duration + 5)
 
            assignments.append((
                assignment_id,
                bus,
                driver,
                route_id,
                day,
                dep.strftime("%H:%M"),
                arr.strftime("%H:%M"),
                "Morning" if dep.hour < 12 else "Evening"
            ))
 
            used_buses[bus]     = arr
            used_drivers[driver] = arr
            assignment_id += 1
            time_cursor += timedelta(minutes=freq)
 
cursor.executemany(
    "INSERT INTO assignments VALUES (:1,:2,:3,:4,:5,:6,:7,:8)",
    assignments
)
print(f"Inserted {len(assignments)} assignments")
 
# ─────────────────────────────────────────────
# COMMIT & CLOSE
# ─────────────────────────────────────────────
conn.commit()
cursor.close()
conn.close()
print("\nAll data inserted and committed successfully.")