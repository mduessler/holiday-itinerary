from ui.handlers.itinerary import Itinerary


def test_roundtrip_with_mock(df_poi, mock_request_get):
    poi_order, total_distance, route = Itinerary().roundtrip(df_poi, df_poi["city"].iloc[0])
    assert poi_order == df_poi["poiId"].tolist()
    assert total_distance == 100
    assert route[0] == route[-1]


def test_one_way_trip_flex_end_with_mock(df_poi, mock_request_get):
    poi_order, total_distance, route = Itinerary().one_way_trip_flex_end(df_poi, df_poi["city"].iloc[0])
    assert poi_order == df_poi["poiId"].tolist()
    assert total_distance == 100
    assert route[0] != route[-1]


def test_one_way_trip_fixed_end_with_mock(df_poi, mock_request_get):
    poi_order, total_distance, route = Itinerary().one_way_trip_flex_fixed_end(
        df_poi, df_poi["city"].iloc[0], df_poi["city"].iloc[-1]
    )
    assert poi_order == df_poi["poiId"].tolist()
    assert total_distance == 100
    assert route[0] != route[-1]
