import os

import requests
import streamlit as st


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://localhost:8000",
)

st.set_page_config(
    page_title="Electricity Tariff Dispute Triage",
    layout="wide",
)

st.title("Electricity Tariff Dispute Triage")
st.caption(
    "Regulation-grounded recommendations for grievance officers"
)

st.warning(
    "This service provides evidence-based triage. "
    "It does not modify bills or replace the grievance officer."
)

with st.form("dispute_form"):
    consumer_reference = st.text_input(
        "Consumer reference"
    )

    complaint_text = st.text_area(
        "Describe the billing dispute",
        height=150,
    )

    premises_type = st.selectbox(
        "Premises type",
        [
            "domestic",
            "commercial",
            "industrial",
            "mixed_use",
            "other",
        ],
    )

    connected_load_kw = st.number_input(
        "Connected load (kW)",
        min_value=0.1,
        max_value=10000.0,
        value=3.0,
    )

    current_tariff_category = st.text_input(
        "Current tariff category",
        value="domestic",
    )

    submitted = st.form_submit_button(
        "Submit dispute"
    )


if submitted:
    payload = {
        "consumer_reference": consumer_reference,
        "complaint_text": complaint_text,
        "premises_type": premises_type,
        "connected_load_kw": connected_load_kw,
        "current_tariff_category": current_tariff_category,
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/disputes",
            json=payload,
            timeout=15,
        )

        if response.status_code == 422:
            st.error(
                "The request failed validation."
            )
            st.json(response.json())

        else:
            response.raise_for_status()

            result = response.json()

            st.success(
                "The dispute was submitted."
            )

            st.write(
                "Run ID:",
                result["run_id"],
            )

            st.info(
                "Record this ID to retrieve the result."
            )

    except requests.RequestException as exc:
        st.error(
            f"Could not contact the API: {exc}"
        )