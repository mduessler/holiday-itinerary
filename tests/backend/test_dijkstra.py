BASE_URL = "/dijkstra"


def test_get_route_between_cities(client):
    response = client.get(f"{BASE_URL}?poi_ids=1&poi_ids=2")
    assert response.status_code == 200
    assert response.json() == {
        "path": ["poi1", "poi2"],
        "distance": 3.5,
    }


def test_get_roundtrip(client):
    response = client.get(f"{BASE_URL}/create-roads")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
