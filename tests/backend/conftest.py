from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    with patch("neo4j_driver.neo4j_driver.Neo4jDriver") as MockDriver:
        driver_instance = MockDriver.return_value

        driver_instance.get_cities.return_value = {"id": "1", "name": "Paris"}
        driver_instance.get_city.return_value = {"id": "1", "name": "Paris"}
        driver_instance.get_poi_for_city.return_value = [{"id": "poi1", "name": "Eiffel Tower"}]
        driver_instance.get_poi_near_city.return_value = [{"id": "poi2", "name": "Louvre"}]
        driver_instance.get_poi_types_for_city.return_value = ["museum", "monument"]
        driver_instance.get_nearest_city_by_coordinates.return_value = {"id": "1", "name": "Paris"}
        driver_instance.calculate_shortest_path_from_start_to_dest.return_value = {
            "path": ["poi1", "poi2"],
            "distance": 3.5,
        }
        driver_instance.create_roads.return_value = {"status": "OK"}
        driver_instance.calculate_distance_between_two_nodes.return_value = 2.7
        driver_instance.get_poi.return_value = {"id": "poi1", "name": "Eiffel Tower"}
        driver_instance.get_nearby_points.return_value = {"points": ["poi2", "poi3"]}
        driver_instance.get_types.return_value = {"types": ["museum", "monument"]}
        driver_instance.get_filtered_pois.return_value = {"pois": ["poi1"]}
        driver_instance.get_route_between_cities.return_value = [{"path": ["poi1", "poi2"], "distance": 3.5}]
        driver_instance.get_roundtrip.return_value = {"status": "OK"}
        driver_instance.calculate_shortest_round_tour.return_value = {
            "poi_order": ["poi1", "poi2"],
            "total_distance": 5.0,
            "route": [[0, 0], [1, 1]],
        }
        driver_instance.calculate_shortest_path_no_return.return_value = {
            "poi_order": ["poi1", "poi2"],
            "total_distance": 4.0,
            "route": [[0, 0], [1, 1]],
        }
        driver_instance.calculate_shortest_path_fixed_dest.return_value = {
            "poi_order": ["poi1", "poi2"],
            "total_distance": 6.0,
            "route": [[0, 0], [1, 1]],
        }

        driver_instance.close = AsyncMock()

        from neo4j_api.main import app

        app.state.driver = driver_instance

        with TestClient(app) as client:
            yield client
