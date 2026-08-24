CREATE OR REPLACE FUNCTION get_direct_route_fare (
    p_routeid IN NUMBER,
    p_startseq IN NUMBER,
    p_endseq IN NUMBER,
    p_bus_type IN buses.bus_type%TYPE
) RETURN NUMBER
IS
    v_price NUMBER;
    v_final NUMBER;
BEGIN
    SELECT fare_amt INTO v_price
    FROM fares
    WHERE route_id = p_routeid
    AND from_sequence = p_startseq
    AND to_sequence = p_endseq;

    IF p_bus_type = 'pvt' THEN
        v_final := v_price + v_price * 0.5;
    ELSE
        v_final := v_price;
    END IF;

    RETURN v_final;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN 0;
END;
/

CREATE OR REPLACE PROCEDURE get_direct_routes (
    p_start_stop IN NUMBER,
    p_stop_stop IN NUMBER,
    p_time IN assignments.departure_time%TYPE,
    p_day IN assignments.assignment_day%TYPE,
    p_results OUT SYS_REFCURSOR
)
IS
BEGIN
    OPEN p_results FOR
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
                get_direct_route_fare(
                    rs_start.route_id,
                    rs_start.stop_sequence,
                    rs_stop.stop_sequence,
                    b.bus_type
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

        WHERE 
            rs_start.stop_id = p_start_stop
            AND rs_stop.stop_id = p_stop_stop
            AND rs_start.stop_sequence < rs_stop.stop_sequence

            AND TO_DATE(a.departure_time, 'HH24:MI') 
                + NUMTODSINTERVAL(rs_start.minutes_from_start, 'MINUTE') 
                >= TO_DATE(p_time, 'HH24:MI')

            AND a.assignment_day = p_day

            AND ROWNUM <= 20   -- prevents hanging

        ORDER BY fare DESC;

END;
/