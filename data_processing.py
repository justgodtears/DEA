import polars as pl

def icd_data_processing():
    """ICD-10 Data processing"""
    df = pl.read_csv('data_raw/icd1-data(pl).csv', encoding='utf-8', separator=";")
    result = df.filter(pl.col("name18") == "EN")
    data = result.select(
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


if __name__ == "__main__":
    diag_data = diag_data_processing()