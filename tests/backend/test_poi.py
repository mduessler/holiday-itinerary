BASE_URL = "/poi"


def test_get_poi(client):
    response = client.get(f"{BASE_URL}/?poi_id=poi1")
    assert response.status_code == 200
    assert response.json() == {"id": "poi1", "name": "Eiffel Tower"}


def test_get_nearby_points(client):
    response = client.get(f"{BASE_URL}/nearby?poi_id=poi1&radius=5")
    assert response.status_code == 200
    assert response.json() == {"points": ["poi2", "poi3"]}


def test_get_types(client):
    response = client.get(f"{BASE_URL}/types")
    assert response.status_code == 200
    assert response.json() == {"types": ["museum", "monument"]}


def test_get_filtered_pois(client):
    response = client.get(f"{BASE_URL}/filter?locations=loc1&locations=loc2&types=museum&types=monument&radius=10")
    assert response.status_code == 200
    assert response.json() == {"pois": ["poi1"]}
