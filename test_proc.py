import oracledb

def test_procedure():
    try:
        # CONNECT TO ORACLE
        conn = oracledb.connect(
            user="system",
            password="oracle123",   # change if needed
            dsn="localhost:1521/XEPDB1"
        )

        cursor = conn.cursor()

        print("Connected to DB")

        # INPUTS (change these based on your DB)
        start_stop_id = 1
        end_stop_id = 3
        time = "08:00"
        day = "Monday"

        # CREATE REF CURSOR
        ref_cursor = cursor.var(oracledb.CURSOR)

        print("Calling procedure...")

        # CALL PROCEDURE
        cursor.callproc("get_direct_routes", [
            start_stop_id,
            end_stop_id,
            time,
            day,
            ref_cursor
        ])

        print("Procedure executed")

        # FETCH RESULTS
        result_cursor = ref_cursor.getvalue()
        rows = result_cursor.fetchall()

        print(f"\nRows fetched: {len(rows)}\n")

        # PRINT COLUMN NAMES
        columns = [col[0] for col in result_cursor.description]
        print("Columns:", columns)
        print("-" * 60)

        # PRINT DATA
        for row in rows:
            print(row)

        # CLEANUP
        result_cursor.close()
        cursor.close()
        conn.close()

        print("\nConnection closed")

    except Exception as e:
        print("Error:", e)


# RUN
if __name__ == "__main__":
    test_procedure()