from pathlib import Path
import shutil
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from src.image_prediction import predict_disease
from src.recommendations import get_recommendation
from src.query_detection import detect_disease_from_query


app = FastAPI(
    title="Smart Crop Advisory - Disease Detection API",
    version="1.0.0",
)


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {
        "message": "Smart Crop Advisory Disease Detection API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "disease_detection",
    }


@app.post("/predict/image")
async def predict_image(file: UploadFile = File(...)):

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file.",
        )

    suffix = Path(file.filename or ".jpg").suffix

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            shutil.copyfileobj(
                file.file,
                temp_file,
            )

            temp_path = temp_file.name

        prediction = predict_disease(
        temp_path
        )

        predicted_class = prediction["class_name"]
        confidence = prediction["confidence"]

        recommendation = prediction["recommendation"]
        return {
            "success": True,
            "input_type": "image",
            "plant": recommendation["plant"],
            "disease": recommendation["disease"],
            "class": predicted_class,
            "confidence": round(confidence, 4),
            "confidence_percent": round(
                confidence * 100,
                2,
            ),
            "description": recommendation["description"],
            "treatment": recommendation["treatment"],
            "fertilizer": recommendation["fertilizer"],
            "prevention": recommendation["prevention"],
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    finally:

        if temp_path and Path(temp_path).exists():
            Path(temp_path).unlink()


@app.post("/predict/query")
def predict_query(request: QueryRequest):

    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty.",
        )

    result = detect_disease_from_query(
        query
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="No matching disease was found.",
        )

    return {
        "success": True,
        "input_type": "query",
        "plant": result["plant"],
        "disease": result["disease"],
        "class": result["class_name"],
        "description": result["description"],
        "treatment": result["treatment"],
        "fertilizer": result["fertilizer"],
        "prevention": result["prevention"],
    }