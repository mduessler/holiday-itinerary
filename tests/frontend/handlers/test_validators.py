import pytest
from ui.handlers import has_attr, is_column


def test_is_colum_valid(df_poi):
    assert not is_column("poiId", df_poi)


def test_is_colum_failure(df_poi):
    with pytest.raises(KeyError):
        is_column("poi_id", df_poi)


def test_has_attr_valid(poi):
    assert not has_attr("poiId", poi)


def test_has_attr_failure(poi):
    with pytest.raises(KeyError):
        has_attr("poi_id", poi)
