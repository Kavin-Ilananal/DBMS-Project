# Bus Transit System 🚌

A little DBMS project that lets you search for buses between two stops, see direct routes as well as routes that need a transfer, check fares, and view driver/bus details — all backed by an Oracle database and a desktop (Tkinter) UI.

This started as a coursework project, so don't expect production-grade polish everywhere, but the core route-finding logic (including the transfer/connection search) is genuinely non-trivial and was fun to get right.

## What it does

- **Login / Sign up** — basic user accounts stored in the DB (passwords are stored as-is right now, see the "known issues" section below 👀)
- **Search for buses** — pick a start stop, an end stop, a date, and a time
- **Direct routes** — buses that go straight from A to B, with departure/arrival times and fare
- **Routes with one transfer** — if there's no direct bus, it'll try to find a valid connection: bus 1 to a common stop, then bus 2 onward, making sure the second bus actually leaves after the first one arrives
- **Fare calculation** — private buses get a 50% markup over government fare, handled via a SQL function
- **Driver & bus details** — tap into a result to see the driver's name, phone, license, experience, and bus type
- **Search history** — your last searches get saved and you can revisit them from a popup

## Tech stack

- **Database:** Oracle (tested against `XEPDB1` / Oracle XE)
- **Backend:** Python + [`python-oracledb`](https://oracle.github.io/python-oracledb/) for talking to the DB
- **UI:** Tkinter (`tkcalendar` for the date picker)
- **Config:** `.env` file via `python-dotenv`

## Project structure

```
├── table_creation.sql   # DDL — all the tables (stops, buses, drivers, routes, etc.)
├── procedures.sql       # PL/SQL function + procedure for fare calc & direct-route lookup
├── insertions.sql       # Seed data as raw SQL
├── create_db.py         # Sets up tables/sequence/triggers and seeds some users (Python version)
├── insert_data.py       # Seeds sample stops/buses/drivers/routes/assignments/fares
├── db_queries.py        # The actual query logic (direct routes + transfer routes)
├── ui.py                # Tkinter desktop app — login, search, results, history
├── test_proc.py         # Quick script to test the PL/SQL procedure directly
└── search_history.json  # Sample/exported search history data
```

## Database schema (short version)

- `stops` — bus stops with name, landmark, lat/long
- `buses` — bus number, model, type (government / private)
- `drivers` — name, license, experience, phone, photo
- `routes` — route number/name, start & end stop, frequency
- `route_stops` — the stops a route passes through, in order, with distance & time offsets
- `assignments` — which bus + driver runs which route, on which day, at what time
- `fares` — fare between two stop-sequences on a route
- `users` — app users
- `search_history` — what people searched for and when

Foreign keys tie it all together, and there are a couple of triggers (auto-increment ID for search history, and one that blocks a search where the start and end stop are the same).

## Getting started

### 1. Prerequisites

- Oracle Database (XE works fine) running locally
- Python 3.10+

### 2. Install dependencies

```bash
pip install oracledb python-dotenv tkcalendar
```

### 3. Set up your `.env`

Create a `.env` file in the project root:

```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_DSN=localhost:1521/XEPDB1
```

### 4. Create the schema

Either run the SQL directly:

```bash
sqlplus your_user/your_password@localhost:1521/XEPDB1 @table_creation.sql
sqlplus your_user/your_password@localhost:1521/XEPDB1 @procedures.sql
```

...or let the Python script do it (also seeds a few sample users):

```bash
python create_db.py
```

### 5. Load sample data

```bash
python insert_data.py
```

This populates stops, buses, drivers, routes, route stops, fares, and assignments with realistic-ish sample data so you actually have something to search for.

### 6. Run the app

```bash
python ui.py
```

Log in (or sign up), pick your stops, date, and time, and hit search.

## Known issues / things I'd fix with more time

- Passwords are stored in plain text — fine for a class project, not fine for real life. Would hash these with `bcrypt` next.
- Credentials currently live in `.env` with a placeholder default password — swap these out before using this anywhere real.
- The transfer-route query can get slow on larger datasets since it's joining a lot of rows before filtering — could use some indexing / query tuning.
- Not much input validation on the UI side yet.
- No tests beyond `test_proc.py`, which just exercises the direct-route stored procedure manually.
