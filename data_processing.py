import polars as pl

def icd_data_processing():
    """ICD-10 Data processing"""
    df = pl.read_csv('data_raw/icd1-data(pl).csv', encoding='utf-8', separator=";")
    data = df.select(
        #Main
        pl.col("code11").alias("icd_code"),
        pl.col("ns1:name12").alias("disease_type_pl"),
        pl.col("ns1:attribute13").alias("disease_type_en"),

        #Detailed
        pl.col("code15").alias("icd_disease_details"),
        pl.col("ns1:name16").alias("disease_pl_details"),
        pl.col("ns1:attribute17").alias("disease_en_details")

    )

    save = data.write_csv("data_processed/icd10-dict.csv", separator=";")
    return save


def diag_data_processing():
    """ICD-10 Diagnosis processing"""
    schema_overrides = {
        "KOD_SWIADCZENIODAWCY" : pl.String
    }

    df_diag = pl.read_csv("data_raw/rozpozanieicd10.csv",
                          encoding="utf8",
                          separator=";",
                          schema_overrides=schema_overrides
                          )

    result_diag = df_diag.select(
        pl.col("KOD_SWIADCZENIODAWCY").cast(pl.String).alias("hospital_code"),
        pl.col("ROZPOZNANIE_WG_ICD10").alias("diag_code"),
        pl.when(pl.col("LICZBA_PACJENTOW") == "<5")
        .then(pl.lit(None))
        .otherwise(pl.col("LICZBA_PACJENTOW")).alias("patient_count"),
        pl.when(pl.col("LICZBA_PACJENTOW") == "<5")
        .then(True)
        .otherwise(False).alias("is_suppressed")
    )

    save_diag = result_diag.write_csv("data_processed/rozpoznanie.csv", separator=";")
    return save_diag


def drug_treatment_data():
    """Processind data about drug treatment"""
    schema_overrides = {
        "KOD_SWIADCZENIODAWCY": pl.String,
        "KOD_EAN_LEKU": pl.String
    }

    df_drug = pl.read_csv("data_raw/rozpoznanieicd10lek.csv",
                          encoding="utf8",
                          separator=";",
                          schema_overrides=schema_overrides
                          )

    result_drug = df_drug.select(
        pl.col("KOD_SWIADCZENIODAWCY").cast(pl.String).alias("hospital_code"),
        pl.col("ROZPOZNANIE_WG_ICD10").alias("diag_code"),
        pl.col("KOD_EAN_LEKU").alias("drug_code"),
        pl.when(pl.col("LICZBA_PACJENTOW") == "<5")
        .then(pl.lit(None))
        .otherwise(pl.col("LICZBA_PACJENTOW")).alias("patient_count"),
        pl.when(pl.col("LICZBA_PACJENTOW") == "<5")
        .then(True)
        .otherwise(False).alias("is_suppressed")
    )

    save_drug = result_drug.write_csv("data_processed/drug_treatment.csv", separator=";")
    return save_drug



def drug_registry():
    """Processing data from drug registry"""
    df_registry = pl.read_csv("data_raw/rejestr_lekow.csv",
                          encoding="utf8",
                          separator=";",
                          )

    result_registry = (df_registry
                       .select(
        pl.col("Nazwa Produktu Leczniczego").alias("trade_name"),
        pl.col("Nazwa powszechnie stosowana").alias("substance_name"),
        pl.col("Opakowanie").str.split("\n").alias("ean_code")
    )
                       .explode("ean_code")
                       .with_columns(pl.col("ean_code").str.split("¦"))
                       .explode("ean_code")
                       .with_columns(pl.col("ean_code").str.strip_chars())
                       .filter(pl.col("ean_code").str.contains(r"^\d{13}", literal=False))
                       )

    save_registry = result_registry.write_csv("data_processed/drug_registry.csv", separator=";")
    return save_registry


if __name__ == "__main__":
    icd_data_processing()
