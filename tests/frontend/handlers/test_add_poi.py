import pytest
from ui.handlers import AddPoi


def test_add_poi_to_df_valid(df_poi, poi):
    assert poi["poiId"] not in df_poi["poiId"].values
    df = AddPoi().add_poi_to_df(df_poi, poi)
    assert poi["poiId"] in df["poiId"].values


def test_add_poi_to_df_failure(df_poi):
    poi = df_poi.iloc[[0]].copy()
    with pytest.raises(ValueError):
        AddPoi().add_poi_to_df(df_poi, poi)
