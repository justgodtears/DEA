import streamlit as st
import polars as pl
import duckdb

conn = duckdb.connect("database/medbase.db")
query = """SELECT * FROM medbase.hospital_dict"""

df = pl.read_database(query=query, connection=conn)






st.title("Map test")
st.map(data=df)
st.subheader("Map test")

