from fastapi.testclient import TestClient
from app.main import app, graph_state
import networkx as nx
import pytest

client = TestClient(app)


@pytest.fixture
def mock_graph():
    G = nx.Graph()
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 1)
    return G


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Mobility Network API is running. Go to /docs for Swagger UI."}


def test_analyze_endpoint_no_data():
    # Ensure graph state is empty
    graph_state.clear()
    response = client.get("/analyze")
    assert response.status_code == 503
    assert response.json()["detail"] == "Graph data not available"


def test_analyze_endpoint_success(mock_graph):
    # Inject mock graph into state
    graph_state["G"] = mock_graph

    response = client.get("/analyze")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["algorithm"] == "Louvain"
    assert "results" in data
    assert data["results"]["total_nodes"] == 3
    assert data["results"]["total_communities_detected"] > 0
