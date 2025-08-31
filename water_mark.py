from PIL import Image, ImageDraw, ImageFont, ImageOps

FONT_SIZE = 60
OPACITY = 128


def wartermark_image(input_image_path, watermark_text):
    original = Image.open(input_image_path).convert("RGB")
    original = ImageOps.exif_transpose(original)
    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
    width, height = original.size
    line_count = int(height / 100)
    max_count_words = int(width / 100)
    for j in range(line_count):
        for i in range(max_count_words + 1):
            new_image = Image.new("RGBA", (height, width), (255, 255, 255, 0))
            draw = ImageDraw.Draw(new_image)
            draw.text((i * 100, i * 100), watermark_text, font=font, fill=(255, 255, 255, OPACITY))
            new_image = new_image.rotate(45, expand=True)
            original.paste(new_image, (0, -int(height / 1.5) + j * 300), new_image)

    return original


if __name__ == "__main__":
    input_image_path = "iconpf.jpg"
    output_image_path = "iconpf.png"
    watermark_text = "Watermark"

    wartermark_image(input_image_path, output_image_path, watermark_text)
