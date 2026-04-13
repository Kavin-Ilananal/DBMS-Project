create table stops
(
    stop_id number primary key,
    stop_name varchar2(100) not null,
    landmark varchar2(100),
    latitude number(10,6),
    longitude number(10,6)
);
create table buses
(
    bus_id number primary key,
    bus_number varchar2(30) unique not null,
    model varchar2(50),
    bus_type varchar2(20),
    is_active number(1) default 1 check(is_active in (0,1))
);

create table drivers
(
    driver_id number primary key,
    name varchar2(50) not null,
    phone_no varchar2(20),       -- for numbers like +91 9182...
    license_number varchar2(50) unique,
    experience_years number,
    photo_url varchar2(100),
    is_active number(1) default 1 check(is_active in (0,1))
);

create table users
(
    user_id number primary key,
    name varchar2(50) not null,
    phone_no varchar2(20),
    email varchar2(50) unique not null,
    password varchar2(100) not null,
    created_at timestamp default current_timestamp
);

create table routes
(
    route_id number primary key,
    route_number varchar2(20) unique not null,     -- like route 103A or 51E
    route_name varchar2(50),
    is_active number(1) default 1 check(is_active in (0,1)),
    total_distance number(10,6),
    start_stop_id number,
    end_stop_id number,
    constraint fk_route_start foreign key(start_stop_id) references stops(stop_id),
    constraint fk_route_end foreign key(end_stop_id) references stops(stop_id)
);

create table search_history
(
    history_id number primary key,
    user_id number not null,
    from_stop_id number,
    to_stop_id number,
    searched_at timestamp default current_timestamp,
    result_snapshot varchar2(2000),      --we can have a json or something
    constraint fk_search_user foreign key(user_id) references users(user_id),
    constraint fk_search_from_stop foreign key(from_stop_id) references stops(stop_id),
    constraint fk_search_to_stop foreign key(to_stop_id) references stops(stop_id)
);







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
  INTO routes (route_id, route_number, route_name, total_distance, start_stop_id, end_stop_id) VALUES (1, 'R1', 'Route 1', 25, 1, 6)
  INTO routes (route_id, route_number, route_name, total_distance, start_stop_id, end_stop_id) VALUES (2, 'R2', 'Route 2', 33, 5, 6)
  INTO routes (route_id, route_number, route_name, total_distance, start_stop_id, end_stop_id) VALUES (3, 'R3', 'Route 3', 29, 6, 5)
SELECT * FROM dual;

INSERT ALL
  INTO route_stops VALUES (101, 1, 1, 1, 0, 0)
  INTO route_stops VALUES (102, 1, 2, 2, 4, 5)
  INTO route_stops VALUES (103, 1, 4, 3, 8, 10)
  INTO route_stops VALUES (104, 1, 3, 4, 10, 14)
  INTO route_stops VALUES (105, 1, 7, 5, 13, 19)
  INTO route_stops VALUES (106, 1, 6, 6, 25, 38)
    
  INTO route_stops VALUES (201, 2, 5, 1, 0, 0)
  INTO route_stops VALUES (202, 2, 4, 2, 10, 20)
  INTO route_stops VALUES (203, 2, 1, 3, 13, 25)
  INTO route_stops VALUES (204, 2, 2, 4, 17, 30)
  INTO route_stops VALUES (205, 2, 7, 5, 21, 35)
  INTO route_stops VALUES (206, 2, 6, 6, 33, 48)
    
  INTO route_stops VALUES (301, 3, 6, 1, 0, 0)
  INTO route_stops VALUES (302, 3, 4, 2, 6, 10)
  INTO route_stops VALUES (303, 3, 2, 3, 10, 15)
  INTO route_stops VALUES (304, 3, 1, 4, 14, 20)
  INTO route_stops VALUES (305, 3, 3, 5, 22, 35)
  INTO route_stops VALUES (306, 3, 5, 6, 29, 47)
SELECT * FROM dual;





    
