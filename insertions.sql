INSERT ALL
  INTO stops (stop_id, stop_name) VALUES (1, 'A')
  INTO stops (stop_id, stop_name) VALUES (2, 'B')
  INTO stops (stop_id, stop_name) VALUES (3, 'C')
  INTO stops (stop_id, stop_name) VALUES (4, 'D')
  INTO stops (stop_id, stop_name) VALUES (5, 'E')
  INTO stops (stop_id, stop_name) VALUES (6, 'F')
  INTO stops (stop_id, stop_name) VALUES (7, 'G')
SELECT * FROM dual;

INSERT ALL
  INTO buses (bus_id, bus_number, bus_type, is_active) VALUES (1, 'B-001', 'govt', 1)
  INTO buses (bus_id, bus_number, bus_type, is_active) VALUES (2, 'B-002', 'govt', 1)
  INTO buses (bus_id, bus_number, bus_type, is_active) VALUES (3, 'B-003', 'pvt', 1)
SELECT * FROM dual;

INSERT ALL
  INTO drivers (driver_id, name, is_active) VALUES (1, 'Ram', 1)
  INTO drivers (driver_id, name, is_active) VALUES (2, 'Gopal', 1)
  INTO drivers (driver_id, name, is_active) VALUES (3, 'Sekhar', 1)
SELECT * FROM dual;

INSERT ALL
  INTO routes (route_id, route_number, route_name, total_distance, start_stop_id, end_stop_id, frequency_minutes) 
    VALUES (1, 'R1', 'Route 1', 25, 1, 6, 20)
  INTO routes (route_id, route_number, route_name, total_distance, start_stop_id, end_stop_id, frequency_minutes) 
    VALUES (2, 'R2', 'Route 2', 33, 5, 6, 25)
  INTO routes (route_id, route_number, route_name, total_distance, start_stop_id, end_stop_id, frequency_minutes) 
    VALUES (3, 'R3', 'Route 3', 29, 6, 5, 30)
SELECT * FROM dual;

INSERT ALL
  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (101, 1, 1, 1, 0, 0)
  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (102, 1, 2, 2, 4, 5)
  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (103, 1, 4, 3, 8, 10)
  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (104, 1, 3, 4, 10, 14)
  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (105, 1, 7, 5, 13, 19)
  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (106, 1, 6, 6, 25, 38)

  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (201, 2, 5, 1, 0, 0)
  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (202, 2, 4, 2, 10, 20)
  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (203, 2, 1, 3, 13, 25)
  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (204, 2, 2, 4, 17, 30)
  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (205, 2, 7, 5, 21, 35)
  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (206, 2, 6, 6, 33, 48)

  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (301, 3, 6, 1, 0, 0)
  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (302, 3, 4, 2, 6, 10)
  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (303, 3, 2, 3, 10, 15)
  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (304, 3, 1, 4, 14, 20)
  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (305, 3, 3, 5, 22, 35)
  INTO route_stops (route_stops_id, route_id, stop_id, stop_sequence, distance_from_start, minutes_from_start) 
    VALUES (306, 3, 5, 6, 29, 47)
SELECT * FROM dual;

INSERT ALL
  -- 1. Standard Monday morning route
  INTO assignments (assignment_id, bus_id, driver_id, route_id, assignment_day, departure_time, arrival_time, shift) 
    VALUES (1, 1, 1, 1, 'Monday', '08:00', '08:38', 'Morning')
    
  -- 2. Different bus, driver, and route on Monday
  INTO assignments (assignment_id, bus_id, driver_id, route_id, assignment_day, departure_time, arrival_time, shift) 
    VALUES (2, 2, 2, 2, 'Monday', '09:00', '09:48', 'Morning')
    
  -- 3. Evening shift testing on Monday
  INTO assignments (assignment_id, bus_id, driver_id, route_id, assignment_day, departure_time, arrival_time, shift) 
    VALUES (3, 3, 3, 3, 'Monday', '17:00', '17:47', 'Evening')
    
  -- 4. Driver 2 swapped to Bus 1 on Route 3 (Tuesday)
  INTO assignments (assignment_id, bus_id, driver_id, route_id, assignment_day, departure_time, arrival_time, shift) 
    VALUES (4, 1, 2, 3, 'Tuesday', '07:00', '07:47', 'Morning')
    
  -- 5. Driver 3 on Bus 2 taking Route 1 (Tuesday Evening)
  INTO assignments (assignment_id, bus_id, driver_id, route_id, assignment_day, departure_time, arrival_time, shift) 
    VALUES (5, 2, 3, 1, 'Tuesday', '16:00', '16:38', 'Evening')
    
  -- 6. Driver 1 testing Route 2 on a Wednesday
  INTO assignments (assignment_id, bus_id, driver_id, route_id, assignment_day, departure_time, arrival_time, shift) 
    VALUES (6, 3, 1, 2, 'Wednesday', '10:00', '10:48', 'Morning')
    
  -- 7. Late evening shift for Driver 3
  INTO assignments (assignment_id, bus_id, driver_id, route_id, assignment_day, departure_time, arrival_time, shift) 
    VALUES (7, 1, 3, 2, 'Thursday', '18:00', '18:48', 'Evening')
    
  -- 8. Early morning shift testing
  INTO assignments (assignment_id, bus_id, driver_id, route_id, assignment_day, departure_time, arrival_time, shift) 
    VALUES (8, 2, 1, 3, 'Thursday', '06:00', '06:47', 'Morning')
    
  -- 9. Friday evening rush testing
  INTO assignments (assignment_id, bus_id, driver_id, route_id, assignment_day, departure_time, arrival_time, shift) 
    VALUES (9, 3, 2, 1, 'Friday', '19:00', '19:38', 'Evening')
    
  -- 10. Repeating the Monday pattern on Friday to test consistency
  INTO assignments (assignment_id, bus_id, driver_id, route_id, assignment_day, departure_time, arrival_time, shift) 
    VALUES (10, 1, 1, 1, 'Friday', '08:00', '08:38', 'Morning')
SELECT * FROM dual;
