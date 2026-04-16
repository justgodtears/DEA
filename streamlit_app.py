import streamlit as st
import polars as pl
import duckdb

#Backend of app
conn = duckdb.connect("database/medbase.db")
query_icd = """SELECT * FROM medbase.icd_codes"""
query_hospital = """SELECT * FROM medbase.hospital_dict"""

query_diagnosis_most = """SELECT
    diag_code,
    COALESCE(a.disease_type_en, b.disease_type_en) as disease_name,
    SUM(patient_count) as total_patients
FROM diagnosis
LEFT JOIN icd_codes a ON diagnosis.diag_code = a.icd_disease_details
LEFT JOIN icd_codes b ON diagnosis.diag_code = b.icd_code
GROUP BY diag_code,disease_name
ORDER BY total_patients DESC LIMIT 10"""

query_drugs_reg = """SELECT drug_code,trade_name, sum(patient_count) as total_patients
FROM drug_treatment
JOIN drug_registry
ON drug_treatment.drug_code = drug_registry.ean_code
GROUP BY drug_code,trade_name
ORDER BY total_patients DESC LIMIT 10;"""

#Dataframe from query
df_icd = pl.read_database(query=query_icd, connection=conn)
df_hospital = pl.read_database(query=query_hospital, connection=conn)
df_diagnosis = pl.read_database(query=query_diagnosis_most, connection=conn)
df_drugs_reg = pl.read_database(query=query_drugs_reg, connection=conn)

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

    #Dict of ICD Diseases
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
    st.dataframe(df_icd, width="stretch")

    #Dict of hospitals in datasets
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
    st.dataframe(df_hospital,width="stretch")

    #Most common diseases appearing in 2023
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
                        <h5 class="main-title-three">Diagnosis data</h5>
                        <p class="main-desc-three">Most common diseases appearing in dataset</p>
                    </div>
                """, unsafe_allow_html=True)
    st.bar_chart(df_diagnosis,
                 x="disease_name",
                 y="total_patients",
                 x_label="Disease",
                 y_label="Number of patients",
                 sort="-total_patients",
                 horizontal=True,
                 width="stretch",
                 height=400)

    #Most prescribed drugs in 2023 in hospital treatment
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
                            <h5 class="main-title-three">Drugs</h5>
                            <p class="main-desc-three">Most prescribed drugs in hospital treatment</p>
                        </div>
                    """, unsafe_allow_html=True)
    st.bar_chart(df_drugs_reg,
                 x="trade_name",
                 y="total_patients",
                 x_label="Drugs trade name",
                 y_label="Number of patients",
                 sort="-total_patients",
                 horizontal=True,
                 width="stretch",
                 height=400)




