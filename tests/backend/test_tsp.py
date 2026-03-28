BASE_URL = "/tsp"


def test_shortest_round_tour(client):
    response = client.get(f"{BASE_URL}/shortest-round-tour?poi_ids=poi1&poi_ids=poi2")
    assert response.status_code == 200
    assert response.json() == {"poi_order": ["poi1", "poi2"], "total_distance": 5.0, "route": [[0, 0], [1, 1]]}


def test_shortest_path_no_return(client):
    response = client.get(f"{BASE_URL}/shortest-path-no-return?poi_ids=poi1&poi_ids=poi2")
    assert response.status_code == 200
    assert response.json() == {"poi_order": ["poi1", "poi2"], "total_distance": 4.0, "route": [[0, 0], [1, 1]]}


def test_shortest_path_fixed_dest(client):
    response = client.get(f"{BASE_URL}/shortest-path-fixed-dest?poi_ids=poi1&poi_ids=poi2")
    assert response.status_code == 200
    assert response.json() == {"poi_order": ["poi1", "poi2"], "total_distance": 6.0, "route": [[0, 0], [1, 1]]}
