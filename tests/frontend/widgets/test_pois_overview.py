from unittest.mock import patch

import pandas as pd
import streamlit as st
from ui.config import POI_COLUMNS
from ui.widgets.pois_overview import PoisOverview


def test_pois_overview_calls_get_request(mock_streamlit, create_session_states, df_poi, mock_request_get):
    st.session_state.destinations = [{"name": "Paris"}, {"name": "Bordeaux"}]
    st.session_state.categories = ["Church", "Restaurant"]
    st.session_state.radius = 5
    st.session_state.old_params = {}

    with patch("streamlit.dataframe") as mock_dataframe:
        PoisOverview()

        df = st.session_state.overview
        assert isinstance(df, pd.DataFrame)
        assert df["poiId"].tolist() == df_poi["poiId"].tolist()

        for col in POI_COLUMNS:
            assert col in df.columns

        mock_dataframe.assert_called_once()
        _, kwargs = mock_dataframe.call_args
        assert kwargs["key"] == "overview-pois"
        assert kwargs["height"] == 500
        assert "column_order" in kwargs
        assert "label" in kwargs["column_order"]


def test_pois_overview_skips_when_no_destinations_or_categories(mock_streamlit, create_session_states):
    st.session_state.destinations = []
    st.session_state.categories = []
    st.session_state.radius = 5
    st.session_state.old_params = {}

    with patch("ui.widgets.pois_overview.get_request") as mock_get, patch("streamlit.dataframe") as mock_dataframe:
        PoisOverview()
        mock_get.assert_not_called()
        mock_dataframe.assert_called_once()
