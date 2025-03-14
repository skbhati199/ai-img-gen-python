from ai_img_gen import AIImageGeneratorClient, ClientConfig, ImageGenerationOptions

# Initialize the client
client = AIImageGeneratorClient(
    ClientConfig(
        base_url="https://images.chargingev.app",
        api_key="your_api_key_here"
    )
)

# Generate an image
options = ImageGenerationOptions(
    width=512,
    height=512,
    prompt="A futuristic city with flying cars and neon lights",
    model="dall-e-2",
    format="png",
    quality=90,
    optimize=True
)

try:
    # Generate the image
    image_url = client.generate_image(options)
    print(f"Generated image URL: {image_url}")
    
    # Get supported models
    models = client.get_supported_models()
    print(f"Supported models: {models}")
    
    # Check API health
    health = client.check_health()
    print(f"API health status: {health.status}")
    
    # Get API metrics
    metrics = client.get_metrics()
    print(f"Total requests: {metrics.requests}")
    print(f"Images generated: {metrics.images_generated}")
    print(f"Average response time: {metrics.average_response_time}ms")
    
except Exception as e:
    print(f"Error: {e}")