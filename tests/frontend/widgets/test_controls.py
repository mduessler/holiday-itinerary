from datetime import date

import streamlit as st
from ui.widgets import Controls


def test_contols_init(mock_streamlit, mock_request_get, create_session_states):
    mock_multiselect, mock_date_input, mock_slider, _, _, _, _, _, _, _ = mock_streamlit

    assert st.session_state["cities"] == {}
    assert st.session_state["categories"] == []
    Controls()

    assert st.session_state["cities"] == [{"name": "Paris"}, {"name": "Bordeaux"}]
    mock_multiselect.assert_any_call("Itinerary Destinations", options=["Paris", "Bordeaux"], key="destinations")
    mock_multiselect.assert_any_call("Category of POIs", options=["Church", "Restaurant"], key="categories")
    mock_date_input.assert_any_call("Itinerary start", value=date.today(), format="DD/MM/YYYY", key="start")
    mock_date_input.assert_any_call("Itinerary end", value=date.today(), format="DD/MM/YYYY", key="end")
    mock_slider.assert_called_once_with("Distance from city", min_value=0, max_value=100, key="radius")
