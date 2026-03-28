BASE_URL = "/distance"


def test_get_distance(client):
    response = client.get(f"{BASE_URL}/?poi1_id=poi1&poi2_id=poi2")
    assert response.status_code == 200
    assert response.json() == {"distance": 2.7}
