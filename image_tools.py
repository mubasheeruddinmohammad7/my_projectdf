from PIL import Image, ImageDraw

def create_before_after_comparison(before_img, after_img, slider_position):
    after_img_resized = after_img.resize(before_img.size)
    w, h = before_img.size

    cropped = after_img_resized.crop((0, 0, slider_position, h))
    composite = Image.new('RGB', (w, h))
    composite.paste(before_img, (0, 0))

    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle([0, 0, slider_position, h], fill=255)

    composite.paste(cropped, (0, 0), mask)
    return composite