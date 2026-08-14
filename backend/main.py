from fastapi import FastAPI

app = FastAPI(
    title="Aperture Signs API",
    description="Real-time sign language accessibility platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "Aperture Signs",
        "status": "online",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "aperture-signs-backend",
    }
