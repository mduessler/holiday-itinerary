from typing import NamedTuple

import pandas as pd
import streamlit as st
from loguru import logger
from ui.utils import init_empty_df


class StateSpec(NamedTuple):
    name: str
    default: dict | list | pd.DataFrame | str | int | float | None


STATES: list[StateSpec] = [
    StateSpec("cities", {}),
    StateSpec("destinations", []),
    StateSpec("categories", []),
    StateSpec("overview", init_empty_df()),
    StateSpec("selected_poi", None),
    StateSpec("add_point", None),
    StateSpec("route", init_empty_df()),
    StateSpec("old_params", {}),
    StateSpec("itinerary_type", ""),
    StateSpec("start_city", ""),
    StateSpec("dest_city", ""),
    StateSpec("ordered_route", []),
    StateSpec("distance", 0.0),
    StateSpec("radius", 0),
    StateSpec("route_coords", []),
]


def init_session_states() -> None:
    if "_initialized" in st.session_state:
        logger.info("session_state already initialized. Skipping.")
        return
    logger.debug("Initializing session states...")
    for state in STATES:
        if state.name not in st.session_state:
            st.session_state[state.name] = state.default
            logger.debug(f"Set {state.name} to: {st.session_state[state.name]}")
    st.session_state["_initialized"] = True
    logger.info("Initialized session_states.")
