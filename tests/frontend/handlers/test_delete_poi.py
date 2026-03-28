from ui.handlers import DeletePoi


def test_delete_poi_of_df(df_poi, poi):
    assert not df_poi.empty
    df_poi[0, "poiId"] = poi["poiId"]
    p = df_poi.rename(columns={"poiId": "poi_id"})
    df = DeletePoi().remove_df_from_df(df_poi, p)
    assert df.empty
