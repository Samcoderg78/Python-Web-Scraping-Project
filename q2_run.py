"""Run q2_queries.sql against the public Rfam MySQL server and print the results.

Usage:  python q2_run.py
"""
import pymysql

CONNECTION = dict(host="mysql-rfam-public.ebi.ac.uk", port=4497,
                  user="rfamro", database="Rfam")


def load_queries(path="q2_queries.sql"):
    """Split the SQL file into individual statements, dropping '--' comment lines."""
    with open(path, encoding="utf-8") as f:
        lines = [l for l in f if not l.strip().startswith("--")]
    return [q.strip() for q in "".join(lines).split(";") if q.strip()]


def main():
    conn = pymysql.connect(**CONNECTION)
    with conn.cursor() as cur:
        for i, query in enumerate(load_queries(), start=1):
            cur.execute(query)
            columns = [c[0] for c in cur.description]
            print(f"\n--- Query {i} ---")
            print(" | ".join(columns))
            for row in cur.fetchall():
                print(" | ".join(str(v) for v in row))
    conn.close()


if __name__ == "__main__":
    main()
