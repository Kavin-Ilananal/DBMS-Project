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
    frequency_minutes number,
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
create table route_stops
(
    route_stops_id number primary key,
    route_id number not null,
    stop_id number not null,
    stop_sequence number not null,
    distance_from_start number(8,2),
    minutes_from_start number,
    constraint fk_rs_route foreign key (route_id) references routes(route_id),
    constraint fk_rs_stop foreign key (stop_id) references stops(stop_id)
);

create table fares
(
    fare_id number primary key,
    route_id number not null,
    from_sequence number,
    to_sequence number,
    fare_amt number(8,2),
    constraint fk_fares_route foreign key(route_id) references routes(route_id)
);

create table assignments
(
    assignment_id number primary key,
    bus_id number not null,
    driver_id number not null,
    route_id number not null,
    assignment_day varchar2(20),         --like sunday/monday/ ...
    departure_time varchar2(5),           --like 08:50 or 17:25
    arrival_time varchar2(5),
    shift varchar2(20),    -- morning or evening
    constraint fk_assign_bus foreign key(bus_id) references buses(bus_id),
    constraint fk_assign_driver foreign key(driver_id) references drivers(driver_id),
    constraint fk_assign_route foreign key(route_id) references routes(route_id)
);
    
