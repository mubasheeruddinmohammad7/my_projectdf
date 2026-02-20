from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np


def remove_white_background(image):
    """
    Removes white background from image (basic method).
    Converts white pixels to transparent.
    """
    image = image.convert("RGBA")
    data = np.array(image)

    # Identify white pixels
    red, green, blue, alpha = data.T
    white_areas = (red > 240) & (green > 240) & (blue > 240)

    data[..., :-1][white_areas.T] = (0, 0, 0)
    data[..., -1][white_areas.T] = 0

    return Image.fromarray(data)


def enhance_colors(image):
    """
    Improves color vibrance
    """
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(1.5)


def create_depth_map(image):
    """
    Creates a pseudo depth map using grayscale + blur
    """
    gray = ImageOps.grayscale(image)
    depth = gray.filter(ImageFilter.GaussianBlur(radius=5))
    return depth


def create_3d_effect(image):
    """
    Creates a 3D illusion using emboss + edge enhancement
    """
    embossed = image.filter(ImageFilter.EMBOSS)
    edges = image.filter(ImageFilter.FIND_EDGES)
    combined = Image.blend(embossed, edges, alpha=0.5)
    return combined


def full_2d_to_3d_pipeline(image):
    """
    Complete pipeline:
    1. Remove background
    2. Enhance color
    3. Generate depth map
    4. Apply 3D effect
    """
    cleaned = remove_white_background(image)
    enhanced = enhance_colors(cleaned)
    depth = create_depth_map(enhanced)
    final_3d = create_3d_effect(enhanced)

    return cleaned, depth, final_3d