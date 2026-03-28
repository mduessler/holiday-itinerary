BASE_URL = "/travel"


def test_shortest_path_from_start_to_dest(client):
    response = client.get(f"{BASE_URL}/between/Paris/Bordeaux")
    assert response.status_code == 200
    assert response.json() == [{"path": ["poi1", "poi2"], "distance": 3.5}]


def test_create_roads(client):
    response = client.get(f"{BASE_URL}/around/Paris?distance=10&distance_tol=5&max_hops=3&sort_distance=ASC")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
