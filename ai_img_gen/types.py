from dataclasses import dataclass
from typing import Dict, List, Optional, Union, Any


@dataclass
class ClientConfig:
    """Configuration for the AI Image Generator client."""
    base_url: str
    api_key: Optional[str] = None
    timeout: int = 30


@dataclass
class SupportedModel:
    """Represents a supported AI model."""
    id: str
    name: str
    description: str
    max_width: int
    max_height: int


@dataclass
class SupportedSize:
    """Represents a supported image size."""
    width: int
    height: int
    aspect_ratio: str


@dataclass
class SupportedFormat:
    """Represents a supported image format."""
    id: str
    name: str
    mime_type: str
    extensions: List[str]


@dataclass
class ImageGenerationOptions:
    """Options for generating an image."""
    width: int
    height: int
    prompt: str
    model: Optional[str] = "dall-e-2"
    format: Optional[str] = "png"
    quality: Optional[int] = 90
    optimize: Optional[bool] = True


@dataclass
class ResizeImageOptions:
    """Options for resizing an image."""
    width: int
    height: int
    format: str
    quality: int


@dataclass
class ConvertImageOptions:
    """Options for converting an image format."""
    format: str
    quality: int


@dataclass
class OptimizeImageOptions:
    """Options for optimizing an image."""
    format: str
    quality: int


@dataclass
class HealthStatus:
    """Health status of the API."""
    status: str
    info: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    details: Optional[Dict[str, Any]] = None


@dataclass
class Metrics:
    """API usage metrics."""
    requests: int
    images_generated: int
    average_response_time: float