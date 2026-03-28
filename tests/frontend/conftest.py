import json
from os import getenv
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pandas as pd
import pytest
import streamlit as st
from ui.session_states import init_session_states

TEST_DATA = Path(__file__).resolve().parent.parent / "data"

URL = getenv("API_URL")


@pytest.fixture(scope="function")
def df_poi():
    return pd.read_csv(TEST_DATA / "france_pois.csv")


@pytest.fixture(scope="session")
def poi():
    return pd.Series(
        {
            "label": "Château de Villandry",
            "city": "Villandry",
            "description": "Famous castle with beautiful gardens",
            "street": "",
            "postal_code": "37510",
            "homepage": "http://www.chateauvillandry.fr",
            "additional_information": "Open all year",
            "comment": "Must see the Renaissance gardens",
            "latitude": 47.3300,
            "longitude": 0.9950,
            "poiId": 21,
            "types": ["castle", "garden", "tourist_attraction"],
        }
    )


@pytest.fixture(scope="function")
def mock_request_get(df_poi):
    assert URL

    def side_effect(url, *args, **kwargs):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.raise_for_status = Mock()
        if "/test-endpoint" in url:
            mock_resp.text = '{"key": "value"}'
        elif "/bad-endpoint" in url:
            mock_resp.status_code = 404
            mock_resp.text = "Not found"
        elif f"{URL}/tsp/shortest-round-tour" in url:
            mock_resp.text = json.dumps(
                {
                    "poi_order": df_poi["poiId"].tolist(),
                    "total_distance": 100,
                    "route": [[row["longitude"], row["latitude"]] for _, row in df_poi.iterrows()],
                }
            )
        elif f"{URL}/tsp/shortest-path-no-return" in url:
            mock_resp.text = json.dumps(
                {
                    "poi_order": df_poi["poiId"].tolist(),
                    "total_distance": 100,
                    "route": [[row["longitude"], row["latitude"]] for _, row in df_poi.iterrows()],
                }
            )
        elif f"{URL}/tsp/shortest-path-fixed-dest" in url:
            mock_resp.text = json.dumps(
                {
                    "poi_order": df_poi["poiId"].tolist(),
                    "total_distance": 100,
                    "route": [[row["longitude"], row["latitude"]] for _, row in df_poi.iterrows()],
                }
            )
        elif url == f"{URL}/city/all":
            mock_resp.text = json.dumps({"cities": [{"name": "Paris"}, {"name": "Bordeaux"}]})
        elif url == f"{URL}/poi/types":
            mock_resp.text = json.dumps({"types": ["Church", "Restaurant"]})
        elif "/poi/filter" in url:
            mock_resp.text = json.dumps({"pois": df_poi.to_dict(orient="records")})
        else:
            mock_resp.status_code = 500
            mock_resp.text = "{}"

        return mock_resp

    with patch("ui.handlers.get_request.get") as mock_get:
        mock_get.side_effect = side_effect
        yield mock_get


@pytest.fixture(scope="function")
def mock_streamlit(monkeypatch):
    with (
        patch("streamlit.subheader", MagicMock()) as subheader,
        patch("streamlit.multiselect") as mock_multiselect,
        patch("streamlit.date_input") as mock_date_input,
        patch("streamlit.slider") as mock_slider,
        patch("streamlit.container") as mock_container,
        patch("streamlit.subheader") as mock_subheader,
        patch("streamlit.caption") as mock_caption,
        patch("streamlit.markdown") as mock_markdown,
        patch("streamlit.write") as mock_write,
        patch("streamlit.button") as mock_button,
    ):
        mock_container.return_value.__enter__.return_value = MagicMock()
        mock_container.return_value.__exit__.return_value = None
        st.session_state.clear()
        yield (
            mock_multiselect,
            mock_date_input,
            mock_slider,
            mock_container,
            mock_subheader,
            mock_caption,
            mock_markdown,
            mock_write,
            mock_button,
            subheader,
        )


@pytest.fixture(scope="function")
def create_session_states():
    init_session_states()
