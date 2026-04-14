import duckdb
import polars


def icd_dict_table():
    """Main ICD-10 table with all information"""
    with duckdb.connect("database/medbase.db") as con:
        con.sql("""CREATE TABLE icd_codes AS
        SELECT *
        FROM read_csv("data_processed/icd10-dict.csv")
        """)



def diagnosis_table():
    """Main diagnosis table with all information"""
    with duckdb.connect("database/medbase.db") as con:
        con.sql("""CREATE TABLE diagnosis AS
        SELECT *
        FROM read_csv("data_processed/rozpoznanie.csv", types={'hospital_code': 'VARCHAR' })
        """)


def drug_treatment_table():
    """Drug treatment and diagnosis table"""
    with duckdb.connect("database/medbase.db") as con:
        con.sql("""CREATE TABLE drug_treatment AS
        SELECT *
        FROM read_csv("data_processed/drug_treatment.csv", types={'hospital_code': 'VARCHAR', 'drug_code': 'VARCHAR'})
        """)


def drug_registry():
    """Full registry of drugs in Poland"""
    with duckdb.connect("database/medbase.db") as con:
        con.sql("""CREATE TABLE drug_registry AS
        SELECT *
        FROM read_csv("data_processed/drug_registry.csv", types={'ean_code': 'VARCHAR'} )
        """)


if __name__ == "__main__":
    drug_registry()


