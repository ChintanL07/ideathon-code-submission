from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from app.processing import load_graph_data, detect_communities, generate_graph_image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    DATA_PATH: str = "data/Databike.csv"


settings = Settings()


# Global state for the graph
graph_state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the graph data on startup
    logger.info("Loading graph data...")
    try:
        graph_state["G"] = load_graph_data(settings.DATA_PATH)
        logger.info(f"Graph loaded successfully with {len(graph_state['G'].nodes)} nodes.")
    except Exception as e:
        logger.error(f"Failed to load graph data: {e}")
        graph_state["G"] = None
    yield
    # Clean up resources on shutdown
    graph_state.clear()
    logger.info("Graph data cleared.")

app = FastAPI(title="Mobility Network Community Detection", lifespan=lifespan)


class AnalysisResult(BaseModel):
    modularity_score: float
    total_communities_detected: int
    total_nodes: int


class AnalysisResponse(BaseModel):
    status: str
    algorithm: str
    results: AnalysisResult


@app.get("/")
def home():
    return {"message": "Mobility Network API is running. Go to /docs for Swagger UI."}


@app.get("/analyze", response_model=AnalysisResponse)
def analyze_network():
    if graph_state.get("G") is None:
        raise HTTPException(status_code=503, detail="Graph data not available")

    try:
        results = detect_communities(graph_state["G"])
        return {
            "status": "success",
            "algorithm": "Louvain",
            "results": results
        }
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/visualize")
def visualize_network():
    """Generate and return a visualization of the network with community colors."""
    if graph_state.get("G") is None:
        raise HTTPException(status_code=503, detail="Graph data not available")

    try:
        img_buf = generate_graph_image(graph_state["G"])
        return StreamingResponse(img_buf, media_type="image/png")
    except Exception as e:
        logger.error(f"Error generating visualization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

