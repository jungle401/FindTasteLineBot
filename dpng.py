from PIL import Image

def crop_image(input_image_path, output_image_prefix, crop_size):
    # Open the input image
    input_image = Image.open(input_image_path)

    img_width, img_height = input_image.size
    crop_width, crop_height = crop_size

    x = 0
    while x + crop_width <= img_width:
        y = 0
        while y + crop_height <= img_height:
            # Define the bounding box
            box = (x, y, x + crop_width, y + crop_height)

            # Crop the image
            cropped_image = input_image.crop(box)

            # Generate output filename
            output_image_path = f"{output_image_prefix}_{x}_{y}.png"

            # Save cropped image
            cropped_image.save(output_image_path)

            y += crop_height

        x += crop_width

# Example usage:
input_image_path = "r2.png"
output_image_prefix = "r3.png"
crop_size = (2500, 843)

crop_image(input_image_path, output_image_prefix, crop_size)

