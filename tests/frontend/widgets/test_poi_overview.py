from unittest.mock import MagicMock, patch

import streamlit as st
from ui.handlers import Handler
from ui.widgets import PoiOverview


def test_poi_overview(poi, mock_streamlit, create_session_states):
    st.session_state.selected_poi = poi
    (_, _, _, _, mock_subheader, mock_caption, mock_markdown, mock_write, mock_button, _) = mock_streamlit

    mock_handler = MagicMock(spec=Handler)
    with patch.object(PoiOverview, "parse_readable_string", return_value=poi["additional_information"]):
        PoiOverview(mock_handler)

    mock_subheader.assert_any_call(poi["label"])
    mock_caption.assert_any_call(f"📍 {poi['street']}, {poi['postal_code']} {poi['city']}")
    mock_write.assert_any_call(poi["description"])
    mock_markdown.assert_any_call(f"🌐 **Website**: [🌐 Visit website]({poi['homepage']})")
    mock_button.assert_called_once_with("Add POI", on_click=mock_handler.add_poi)


def test_poi_overview_no_poi(create_session_states):
    st.session_state.clear()
    st.session_state.selected_poi = None

    mock_handler = MagicMock(spec=Handler)

    with (
        patch("streamlit.subheader") as mock_subheader,
        patch("streamlit.container") as mock_container,
        patch("streamlit.button") as _,
    ):

        mock_container.return_value.__enter__.return_value = MagicMock()
        mock_container.return_value.__exit__.return_value = None

        PoiOverview(mock_handler)

        mock_subheader.assert_called_once_with("POI Overview")
