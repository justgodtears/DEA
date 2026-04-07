import polars as pl


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


