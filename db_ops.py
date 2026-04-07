import duckdb
import polars



"""Main ICD-10 table with all information"""
with duckdb.connect("database/medbase.db") as con:
    con.sql("""CREATE TABLE icd_codes AS
    SELECT *
    FROM read_csv("data_processed/icd10-dict.csv")
    """)

