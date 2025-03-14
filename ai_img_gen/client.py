import requests
from typing import Dict, List, Optional, Union, Any
from urllib.parse import urljoin

from .types import (
    ClientConfig,
    SupportedModel,
    SupportedSize,
    SupportedFormat,
    ImageGenerationOptions,
    ResizeImageOptions,
    ConvertImageOptions,
    OptimizeImageOptions,
    HealthStatus,
    Metrics
)
from .exceptions import APIError, AuthenticationError, ValidationError


class AIImageGeneratorClient:
    """Client for interacting with the AI Image Generator API."""

    def __init__(self, config: ClientConfig):
        """Initialize the client with the given configuration.
        
        Args:
            config: Configuration for the client
        """
        self.base_url = config.base_url.rstrip('/')
        self.timeout = config.timeout
        
        self.headers = {
            'Content-Type': 'application/json',
        }
        
        if config.api_key:
            self.headers['Authorization'] = f"Bearer {config.api_key}"
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Any:
        """Make a request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            Response data
            
        Raises:
            APIError: If the API returns an error
            AuthenticationError: If authentication fails
        """
        url = urljoin(self.base_url, endpoint)
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            
            if response.status_code == 400:
                raise ValidationError(response.text)
                
            if response.status_code >= 400:
                raise APIError(response.status_code, response.text)
            
            # Handle redirects for image URLs
            if response.status_code == 302 or response.status_code == 303:
                return response.headers.get('Location')
            
            # Try to parse JSON response
            try:
                return response.json()
            except ValueError:
                # If not JSON, return the response URL or text
                return response.url or response.text
                
        except requests.exceptions.RequestException as e:
            raise APIError(500, str(e))
    
    def generate_image(self, options: ImageGenerationOptions) -> str:
        """Generate an image using AI.
        
        Args:
            options: Image generation options
            
        Returns:
            URL of the generated image
        """
        params = {
            'width': options.width,
            'height': options.height,
            'prompt': options.prompt,
        }
        
        if options.model:
            params['model'] = options.model
        
        if options.format:
            params['format'] = options.format
            
        if options.quality:
            params['quality'] = options.quality
            
        if options.optimize is not None:
            params['optimize'] = str(options.optimize).lower()
        
        try:
            return self._make_request('GET', '/images/image-gen', params)
        except APIError as e:
            # If the first endpoint fails, try the alternative endpoint
            if e.status_code >= 500:
                return self._make_request('GET', '/images/image-gen', params)
            raise
    
    def get_supported_models(self) -> List[str]:
        """Get a list of supported AI models.
        
        Returns:
            List of supported models
        """
        return self._make_request('GET', '/images/supported-models')
    
    def get_supported_sizes(self) -> List[SupportedSize]:
        """Get a list of supported image sizes.
        
        Returns:
            List of supported image sizes
        """
        data = self._make_request('GET', '/images/supported-sizes')
        return [SupportedSize(**size) for size in data]
    
    def resize_image(self, image_id: str, options: ResizeImageOptions) -> str:
        """Resize an existing image.
        
        Args:
            image_id: ID of the image to resize
            options: Resize options
            
        Returns:
            URL of the resized image
        """
        params = {
            'width': options.width,
            'height': options.height,
            'format': options.format,
            'quality': options.quality
        }
        
        return self._make_request('GET', f'/images/process/resize/{image_id}', params)
    
    def convert_image(self, image_id: str, options: ConvertImageOptions) -> str:
        """Convert an image to a different format.
        
        Args:
            image_id: ID of the image to convert
            options: Conversion options
            
        Returns:
            URL of the converted image
        """
        params = {
            'format': options.format,
            'quality': options.quality
        }
        
        return self._make_request('GET', f'/images/process/convert/{image_id}', params)
    
    def optimize_image(self, image_id: str, options: OptimizeImageOptions) -> str:
        """Optimize an image for web delivery.
        
        Args:
            image_id: ID of the image to optimize
            options: Optimization options
            
        Returns:
            URL of the optimized image
        """
        params = {
            'format': options.format,
            'quality': options.quality
        }
        
        return self._make_request('GET', f'/images/process/optimize/{image_id}', params)
    
    def get_supported_formats(self) -> List[SupportedFormat]:
        """Get a list of supported image formats.
        
        Returns:
            List of supported image formats
        """
        data = self._make_request('GET', '/images/process/formats')
        return [SupportedFormat(**fmt) for fmt in data]
    
    def get_metrics(self) -> Metrics:
        """Get API metrics.
        
        Returns:
            API metrics
        """
        data = self._make_request('GET', '/monitoring/metrics')
        return Metrics(**data)
    
    def check_health(self) -> HealthStatus:
        """Check API health.
        
        Returns:
            Health status
        """
        data = self._make_request('GET', '/monitoring/health')
        return HealthStatus(**data)