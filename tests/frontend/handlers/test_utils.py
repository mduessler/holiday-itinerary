from ui.handlers import remove_poi


def test_remove_poi(df_poi):
    poi_id = df_poi.loc[2, "poiId"]
    assert poi_id in df_poi["poiId"].values
    df = remove_poi(df_poi, poi_id)
    assert poi_id not in df["poiId"].values
