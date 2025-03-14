from ai_img_gen import (
    AIImageGeneratorClient, 
    ClientConfig, 
    ImageGenerationOptions,
    ResizeImageOptions,
    ConvertImageOptions,
    OptimizeImageOptions
)
import os
import time

# Initialize the client
client = AIImageGeneratorClient(
    ClientConfig(
        base_url="https://api.img-gen.ai",
        api_key=os.environ.get("AI_IMG_GEN_API_KEY", "your_api_key_here")
    )
)

def extract_image_id(url):
    """Extract the image ID from the URL."""
    # This is a simplified example - adjust based on your actual URL structure
    return url.split('/')[-1].split('.')[0]

try:
    # Generate an image
    print("Generating image...")
    options = ImageGenerationOptions(
        width=512,
        height=512,
        prompt="A beautiful mountain landscape with a lake",
        model="dall-e-2",
        format="png",
        quality=90,
        optimize=True
    )
    
    image_url = client.generate_image(options)
    print(f"Generated image URL: {image_url}")
    
    # Extract the image ID from the URL
    image_id = extract_image_id(image_url)
    print(f"Image ID: {image_id}")
    
    # Wait a moment to ensure the image is processed
    time.sleep(2)
    
    # Resize the image
    print("\nResizing image...")
    resize_options = ResizeImageOptions(
        width=256,
        height=256,
        format="png",
        quality=90
    )
    
    resized_url = client.resize_image(image_id, resize_options)
    print(f"Resized image URL: {resized_url}")
    
    # Convert the image to JPEG
    print("\nConverting image to JPEG...")
    convert_options = ConvertImageOptions(
        format="jpeg",
        quality=85
    )
    
    converted_url = client.convert_image(image_id, convert_options)
    print(f"Converted image URL: {converted_url}")
    
    # Optimize the image for web
    print("\nOptimizing image for web...")
    optimize_options = OptimizeImageOptions(
        format="webp",
        quality=75
    )
    
    optimized_url = client.optimize_image(image_id, optimize_options)
    print(f"Optimized image URL: {optimized_url}")
    
    # Get supported formats
    print("\nGetting supported formats...")
    formats = client.get_supported_formats()
    print("Supported formats:")
    for fmt in formats:
        print(f"- {fmt.name} ({fmt.mime_type}): {', '.join(fmt.extensions)}")
    
except Exception as e:
    print(f"Error: {e}")