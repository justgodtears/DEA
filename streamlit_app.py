import streamlit as st
import polars as pl
import duckdb

#Backend of app
conn = duckdb.connect("database/medbase.db")
query_icd = """SELECT * FROM medbase.icd_codes"""
query_hospital = """SELECT * FROM medbase.hospital_dict"""
query_diagnosis_most = """SELECT * FROM medbase.diagnosis"""

#Dataframe from query
df_icd = pl.read_database(query=query_icd, connection=conn)
df_hospital = pl.read_database(query=query_hospital, connection=conn)




#Frontend of Streamlit app
st.set_page_config(
   page_title="Data Engineering & Analytics",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)
with st.container():
    st.markdown("""
        <style>
            .container {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 24px;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07);
                max-width: 700px;
                margin-bottom: 24px;
            }
            .main-title {
                font-size: 3rem;
                font-weight: 800;
                letter-spacing: -0.05em;
                color: #0f172a;
                margin: 0;
            }
            .main-desc {
                font-size: 1rem;
                color: #64748b;
                margin-top: 8px;
                margin-bottom: 0;
            }
        </style>
        <div class="container">
            <h1 class="main-title">DEA</h1>
            <p class="main-desc">An analytical database built on public Polish healthcare data (NFZ, GOV, e-Zdrowie, Ministry of Health).</p>
        </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("""
            <style>
                .container-two {
                    background-color: #fafffd;
                    border: 1px solid #e2e8f0;
                    border-radius: 16px;
                    padding: 24px;
                    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07);
                    max-width: 400px;
                    margin-bottom: 24px;
                }
                .main-title-two {
                    font-size: 1rem;
                    color: #0f172a;
                    margin-top: 8px;
                    margin-bottom: 0;
                }
                .main-desc-two {
                font-size: 1rem;
                color: #64748b;
                margin-top: 8px;
                margin-bottom: 0;
                }
            </style>
            <div class="container-two">
                <h5 class="main-title-two">ICD Dictionary</h5>
                <p class="main-desc-two">List of all diseases with polish and english descriptions</p>
            </div>
        """, unsafe_allow_html=True)
    st.dataframe(df_icd)

    st.markdown("""
                <style>
                    .container-three {
                        background-color: #fafffd;
                        border: 1px solid #e2e8f0;
                        border-radius: 16px;
                        padding: 24px;
                        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.07);
                        max-width: 400px;
                        margin-bottom: 24px;
                    }
                    .main-title-three {
                        font-size: 1rem;
                        color: #0f172a;
                        margin-top: 8px;
                        margin-bottom: 0;
                    }
                    .main-desc-three {
                        font-size: 1rem;
                        color: #64748b;
                        margin-top: 8px;
                        margin-bottom: 0;
                    }
                </style>
                <div class="container-three">
                    <h5 class="main-title-three">Hospital Dictionary</h5>
                    <p class="main-desc-three">List of all hospitals included in datasets</p>
                </div>
            """, unsafe_allow_html=True)
    st.dataframe(df_hospital)
    st.caption("This is a string that explains something above.")




