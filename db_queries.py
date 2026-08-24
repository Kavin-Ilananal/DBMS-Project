import oracledb
import os

# -----------------------------
# DIRECT ROUTES (NO TRANSFER)
# -----------------------------
def get_available_buses(start_id, end_id, time, day):
    conn = oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dsn=os.getenv("DB_DSN")
    )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            rs_start.route_id,
            b.bus_id,
            d.name,
            d.phone_no,
            d.photo_url,
            d.license_number,
            d.experience_years,
            b.bus_type,

            TO_CHAR(
                TO_DATE(a.departure_time, 'HH24:MI') 
                + NUMTODSINTERVAL(rs_start.minutes_from_start, 'MINUTE'),
                'HH24:MI'
            ) AS get_on_time,

            TO_CHAR(
                TO_DATE(a.departure_time, 'HH24:MI') 
                + NUMTODSINTERVAL(rs_stop.minutes_from_start, 'MINUTE'),
                'HH24:MI'
            ) AS get_off_time,

            ROUND(
                MAX(
                    CASE 
                        WHEN f.fare_amt IS NULL THEN 0
                        WHEN b.bus_type = 'pvt' THEN f.fare_amt * 1.5
                        ELSE f.fare_amt
                    END
                )
            ) AS fare

        FROM route_stops rs_start
        JOIN route_stops rs_stop 
            ON rs_start.route_id = rs_stop.route_id
        JOIN assignments a 
            ON a.route_id = rs_start.route_id
        JOIN buses b 
            ON b.bus_id = a.bus_id
        JOIN drivers d 
            ON d.driver_id = a.driver_id
        LEFT JOIN fares f
            ON f.route_id = rs_start.route_id
            AND f.from_sequence = rs_start.stop_sequence
            AND f.to_sequence = rs_stop.stop_sequence

        WHERE 
            rs_start.stop_id = :start_id
            AND rs_stop.stop_id = :end_id
            AND rs_start.stop_sequence < rs_stop.stop_sequence
            AND TO_DATE(a.departure_time, 'HH24:MI') 
                + NUMTODSINTERVAL(rs_start.minutes_from_start, 'MINUTE') 
                >= TO_DATE(:time, 'HH24:MI')
            AND a.assignment_day = :day

        GROUP BY 
            rs_start.route_id,
            b.bus_id,
            d.name,
            d.phone_no,
            d.photo_url,
            d.license_number,
            d.experience_years,
            b.bus_type,
            rs_start.minutes_from_start,
            rs_stop.minutes_from_start,
            a.departure_time

        ORDER BY get_on_time ASC, fare ASC
    """, {
        "start_id": start_id,
        "end_id": end_id,
        "time": time,
        "day": day
    })

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results


# -----------------------------
# ROUTES WITH TRANSFERS
# -----------------------------
def get_routes_with_transfers(start_id, end_id, time, day):
    conn = oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dsn=os.getenv("DB_DSN")
    )

    cursor = conn.cursor()

    cursor.execute("""

        WITH firstbus AS (
            SELECT 
                rs_start.route_id AS leg1_route,
                rs_start.stop_sequence AS leg1_start_seq,
                rs_dropoff.stop_sequence AS leg1_dropoff_seq,
                rs_dropoff.stop_id AS transfer_stop_id,
                b1.bus_type AS leg1_bus_type,

                b1.bus_id AS first_busid,
                d1.name AS driver1_name,
                d1.phone_no AS driver1_phone,
                d1.photo_url AS driver1_photo,
                d1.license_number AS driver1_license,
                d1.experience_years AS driver1_exp,

                TO_DATE(a1.departure_time, 'HH24:MI') 
                + NUMTODSINTERVAL(rs_start.minutes_from_start, 'MINUTE') AS leg1_board_time,

                TO_DATE(a1.departure_time, 'HH24:MI') 
                + NUMTODSINTERVAL(rs_dropoff.minutes_from_start, 'MINUTE') AS leg1_dropoff_time

            FROM route_stops rs_start
            JOIN route_stops rs_dropoff 
                ON rs_start.route_id = rs_dropoff.route_id
                AND rs_start.stop_sequence < rs_dropoff.stop_sequence
            JOIN assignments a1 
                ON rs_start.route_id = a1.route_id
            JOIN buses b1 
                ON a1.bus_id = b1.bus_id
            JOIN drivers d1 
                ON a1.driver_id = d1.driver_id

            WHERE 
                rs_start.stop_id = :start_id
                AND a1.assignment_day = :day
                AND TO_DATE(a1.departure_time, 'HH24:MI') 
                    + NUMTODSINTERVAL(rs_start.minutes_from_start, 'MINUTE') 
                    >= TO_DATE(:time, 'HH24:MI')
        ),

        secondbus AS (
            SELECT
                rs_pickup.route_id AS leg2_route,
                rs_pickup.stop_id AS transfer_stop_id,
                rs_pickup.stop_sequence AS leg2_pickup_seq,
                rs_end.stop_sequence AS leg2_end_seq,
                b2.bus_type AS leg2_bus_type,

                b2.bus_id AS second_busid,
                d2.name AS driver2_name,
                d2.phone_no AS driver2_phone,
                d2.photo_url AS driver2_photo,
                d2.license_number AS driver2_license,
                d2.experience_years AS driver2_exp,

                TO_DATE(a2.departure_time, 'HH24:MI') 
                + NUMTODSINTERVAL(rs_pickup.minutes_from_start, 'MINUTE') AS leg2_board_time,

                TO_DATE(a2.departure_time, 'HH24:MI') 
                + NUMTODSINTERVAL(rs_end.minutes_from_start, 'MINUTE') AS leg2_dropoff_time

            FROM route_stops rs_pickup
            JOIN route_stops rs_end 
                ON rs_pickup.route_id = rs_end.route_id
                AND rs_pickup.stop_sequence < rs_end.stop_sequence
            JOIN assignments a2 
                ON rs_pickup.route_id = a2.route_id
            JOIN buses b2 
                ON b2.bus_id = a2.bus_id
            JOIN drivers d2 
                ON d2.driver_id = a2.driver_id 

            WHERE 
                rs_end.stop_id = :end_id
                AND a2.assignment_day = :day
        )

        SELECT
            s1.leg1_route AS first_route,
            s1.first_busid,
            s1.driver1_name,
            s1.driver1_phone,
            s1.driver1_photo,
            s1.driver1_license,
            s1.driver1_exp,

            TO_CHAR(s1.leg1_board_time,'HH24:MI') AS board_first_bus_at,

            ts.stop_name AS transfer_at_stop,

            TO_CHAR(s1.leg1_dropoff_time,'HH24:MI') AS arrive_at_transfer_at,

            s2.leg2_route AS second_route,
            s2.second_busid,
            s2.driver2_name,
            s2.driver2_phone,
            s2.driver2_photo,
            s2.driver2_license,
            s2.driver2_exp,

            TO_CHAR(s2.leg2_board_time,'HH24:MI') AS board_second_bus_at,
            TO_CHAR(s2.leg2_dropoff_time,'HH24:MI') AS arrive_at_destination_at,

            ROUND(
                MAX(
                    CASE 
                        WHEN f1.fare_amt IS NULL THEN 0
                        WHEN s1.leg1_bus_type = 'pvt' THEN f1.fare_amt * 1.5
                        ELSE f1.fare_amt
                    END
                )
                +
                MAX(
                    CASE 
                        WHEN f2.fare_amt IS NULL THEN 0
                        WHEN s2.leg2_bus_type = 'pvt' THEN f2.fare_amt * 1.5
                        ELSE f2.fare_amt
                    END
                )
            ) AS total_fare

        FROM firstbus s1
        JOIN secondbus s2 
            ON s1.transfer_stop_id = s2.transfer_stop_id
        JOIN stops ts 
            ON s1.transfer_stop_id = ts.stop_id

        LEFT JOIN fares f1 
            ON f1.route_id = s1.leg1_route
            AND f1.from_sequence = s1.leg1_start_seq
            AND f1.to_sequence = s1.leg1_dropoff_seq

        LEFT JOIN fares f2 
            ON f2.route_id = s2.leg2_route
            AND f2.from_sequence = s2.leg2_pickup_seq
            AND f2.to_sequence = s2.leg2_end_seq

        WHERE 
            s1.leg1_route != s2.leg2_route
            AND s1.first_busid != s2.second_busid
            AND s2.leg2_board_time >= s1.leg1_dropoff_time

        GROUP BY
            s1.leg1_route,
            s1.first_busid,
            s1.driver1_name,
            s1.driver1_phone,
            s1.driver1_photo,
            s1.driver1_license,
            s1.driver1_exp,
            s1.leg1_board_time,
            ts.stop_name,
            s1.leg1_dropoff_time,
            s2.leg2_route,
            s2.second_busid,
            s2.driver2_name,
            s2.driver2_phone,
            s2.driver2_photo,
            s2.driver2_license,
            s2.driver2_exp,
            s2.leg2_board_time,
            s2.leg2_dropoff_time

        ORDER BY 
            s1.leg1_board_time ASC,
            total_fare ASC

        """, {
            "start_id": start_id,
            "end_id": end_id,
            "time": time,
            "day": day
        })

    results = cursor.fetchall()
    cursor.close()
    conn.close()
    print(results)

    return results