# Mobility Network Community Detection API

A production-ready microservice for analyzing bike sharing networks using community detection algorithms. Built with FastAPI, this service provides RESTful endpoints to detect communities in mobility networks using the Louvain algorithm.

## 🚀 Features

- **RESTful API** for community detection analysis
- **Louvain Algorithm** implementation for efficient community detection
- **Docker Support** for containerized deployment
- **CI/CD Pipeline** with automated testing and linting
- **Production-Ready** with proper error handling and logging

## 📋 API Endpoints

### `GET /`
Health check endpoint
- **Response**: `{"message": "Mobility Network API is running. Go to /docs for Swagger UI."}`

### `GET /analyze`
Analyze the bike sharing network and detect communities
- **Response**:
```json
{
  "status": "success",
  "algorithm": "Louvain",
  "results": {
    "modularity_score": 0.42,
    "total_communities_detected": 5,
    "total_nodes": 234
  }
}
```

### `GET /docs`
Interactive Swagger UI for API documentation

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Docker (optional, for containerized deployment)

### Local Development

1. **Clone the repository**
```bash
git clone <repository-url>
cd <repository-folder>
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

4. **Access the API**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## 🐳 Docker Deployment

### Build the Docker image
```bash
docker build -t mobility-network-api .
```

### Run the container
```bash
docker run -p 8000:8000 mobility-network-api
```

The API will be available at http://localhost:8000

## 🧪 Testing

### Run all tests
```bash
pytest -v
```

### Run tests with coverage
```bash
pytest --cov=app --cov-report=html
```

### Run linting
```bash
flake8 . --count --statistics --max-line-length=120
```

## 📁 Project Structure

```
.
├── app/
│   ├── __init__.py          # Application package initialization
│   ├── main.py              # FastAPI application and endpoints
│   └── processing.py        # Graph processing and community detection
├── data/
│   └── Databike.csv         # Bike sharing dataset
├── tests/
│   └── test_main.py         # Unit tests
├── .github/
│   └── workflows/
│       └── ci_pipeline.yml  # GitHub Actions CI/CD pipeline
├── Dockerfile               # Container configuration
├── requirements.txt         # Python dependencies
├── pytest.ini              # Pytest configuration
└── README.md               # This file
```

## 🔬 Algorithm Details

### Louvain Algorithm
The Louvain method is a greedy optimization algorithm that:
- Maximizes modularity to detect communities
- Runs in O(n log n) time complexity
- Provides hierarchical community structure

**Modularity Score**: Measures the quality of community division (range: -0.5 to 1.0)
- Higher values indicate stronger community structure
- Values > 0.3 typically indicate significant community structure

## 📊 Dataset

The project uses bike sharing data (`Databike.csv`) with the following structure:
- **departure_id**: Starting station ID
- **return_id**: Ending station ID
- Each row represents a bike trip between two stations

For performance, the API loads a subset of 1000 trips during initialization.

## 🔄 CI/CD Pipeline

The project includes a GitHub Actions workflow that:
1. ✅ Sets up Python environment
2. ✅ Installs dependencies
3. ✅ Runs automated tests with pytest
4. ✅ Performs code linting with flake8
5. ✅ Builds Docker image to validate Dockerfile

## 👥 Contributors

- Avinash Kumar (B22ME014)
- Chintan Limbachiya (B22ME036)
- Sumit (B22CH037)
- Shashwat Meena (B22BB037)

## 📝 License

This project was created as part of an academic assignment.

## 🔮 Future Enhancements

- Add support for Girvan-Newman algorithm
- Implement graph visualization endpoints
- Add support for larger datasets with pagination
- Implement caching for frequently analyzed networks
- Add authentication and rate limiting
