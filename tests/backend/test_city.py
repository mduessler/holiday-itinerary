BASE_URL = "/city"


def test_get_all_cities(client):
    response = client.get(f"{BASE_URL}/all")
    assert response.status_code == 200
    assert response.json() == {"id": "1", "name": "Paris"}


def test_get_city(client):
    response = client.get(f"{BASE_URL}/1")
    assert response.status_code == 200
    assert response.json() == {"id": "1", "name": "Paris"}


def test_get_city_pois(client):
    response = client.get(f"{BASE_URL}/1/pois")
    assert response.status_code == 200
    assert response.json() == [{"id": "poi1", "name": "Eiffel Tower"}]


def test_get_nearby_city_points(client):
    response = client.get(f"{BASE_URL}/1/pois_nearby")
    assert response.status_code == 200
    assert response.json() == [{"id": "poi2", "name": "Louvre"}]


def test_get_poi_types_for_city(client):
    response = client.get(f"{BASE_URL}/1/poi_types")
    assert response.status_code == 200
    assert response.json() == ["museum", "monument"]


def test_get_city_by_coordinates(client):
    response = client.get(f"{BASE_URL}/48.8566/2.3522")
    assert response.status_code == 200
    assert response.json() == {"id": "1", "name": "Paris"}
