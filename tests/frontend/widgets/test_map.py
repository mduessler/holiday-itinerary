from unittest.mock import patch

import pandas as pd
import pytest
import streamlit as st
from ui.widgets.map import Map  # passe den Import an


@pytest.fixture(autouse=True)
def session_state_setup(df_poi, poi):
    st.session_state.clear()
    st.session_state.cities = [
        {"name": row["city"], "latitude": row["latitude"], "longitude": row["longitude"]}
        for _, row in df_poi.iterrows()
    ]
    st.session_state.route = pd.DataFrame(
        [
            {"poiId": row["poiId"], "latitude": row["latitude"], "longitude": row["longitude"]}
            for _, row in df_poi.iterrows()
        ]
    )
    st.session_state.route_coords = [(row["latitude"], row["longitude"]) for _, row in df_poi.iterrows()]

    st.session_state.selected_poi = poi


def test_map_initialization():
    with patch("streamlit.pydeck_chart") as mock_pydeck_chart, patch("pydeck.Deck") as mock_deck:

        Map()

        mock_deck.assert_called_once()
        deck_instance = mock_deck.call_args[1]
        assert "layers" in deck_instance
        layers = deck_instance["layers"]

        layer_ids = [layer.id for layer in layers]
        assert "route" in layer_ids or any("route" in str(layer) for layer in layers)
        assert "selected-poi" in layer_ids or any("selected-poi" in str(layer) for layer in layers)

        mock_pydeck_chart.assert_called_once_with(mock_deck.return_value, height=734)


def test_center_map_and_zoom():
    map_obj = Map()
    _, _, zoom = map_obj.center_map(st.session_state.route)
    assert isinstance(zoom, int)
