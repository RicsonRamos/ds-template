"""Pydantic schemas for API request and response validation."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response schema."""

    status: str = Field(default="ok", description="Service health status")
    version: str = Field(default="0.1.0", description="API version")


class PredictionRequest(BaseModel):
    """Inference request schema with feature vector."""

    features: list[list[float]] = Field(
        ...,
        description="2D array of numerical features for inference",
        examples=[[[0.5, 1.2, -0.3, 0.8, -1.1]]],
    )


class PredictionResponse(BaseModel):
    """Inference response schema."""

    predictions: list[int] = Field(
        ...,
        description="Predicted class labels",
    )
