import streamlit as st
import polars as pl
import duckdb
import pydeck as pdk

conn = duckdb.connect("database/medbase.db")
query = """SELECT * FROM medbase.hospital_dict"""

df = pl.read_database(query=query, connection=conn).to_pandas()


st.title("Map test")
st.subheader("Map test")


st.pydeck_chart(
    pdk.Deck(
        map_style=None,  # Use Streamlit theme to pick map style
        tooltip={"text": "{hospital_name}"},
        initial_view_state=pdk.ViewState(
            latitude=52.23,
            longitude=21.01,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                df,
                pickable=True,
                opacity=0.8,
                stroked=True,
                filled=True,
                radius_scale=6,
                radius_min_pixels=15,
                radius_max_pixels=250,
                line_width_min_pixels=1,
                get_position="[lon, lat]",
                get_radius="exits_radius",
                get_fill_color=[255, 140, 0],
                get_line_color=[0, 0, 0],
            ),
        ],
    )
)



