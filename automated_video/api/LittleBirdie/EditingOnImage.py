from PIL import Image, ImageFilter, ImageOps
import numpy as np

def add_transparent_layer(image_path, output_path, canvas_width=1920, canvas_height=1080):
    # Open the original image
    image = Image.open(image_path).convert("RGBA")
    # Create a transparent canvas with the desired size
    canvas = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))

    # Calculate the position to center the image on the canvas
    x_offset = (canvas_width - image.width) // 2
    y_offset = (canvas_height - image.height) // 2

    # Paste the original image onto the transparent canvas
    canvas.paste(image, (x_offset, y_offset), image)
    # Extract the alpha channel (mask) from the canvas
    mask = canvas.split()[-1]  # The last channel in RGBA is the alpha channel

    mask = mask.convert("RGBA")  

    # Save the mask as a separate grayscale image
    mask.save("temp/extracted_mask.png", format="PNG")
    canvas_without_alpha = canvas.convert("RGB")

    # Save the result
    canvas_without_alpha.save(output_path, format="PNG")

def add_borders_and_resize_width(image, target_width=1080):
    # Resize the image to the target width, keeping the aspect ratio
    original_width, original_height = image.size
    scale_factor = target_width / original_width
    new_size = (target_width, int(original_height * scale_factor))
    resized_image = image.resize(new_size, Image.LANCZOS)  # Resize using high-quality filter
    
    # Add the first 1px gray border
    border1_color = (169, 169, 169)
    image_with_border1 = ImageOps.expand(resized_image, border=1, fill=border1_color)
    
    # Add the second 10px white border
    border2_color = (255, 255, 255)
    image_with_border2 = ImageOps.expand(image_with_border1, border=10, fill=border2_color)
    
    # Add the third 1px gray border
    image_with_border3 = ImageOps.expand(image_with_border2, border=1, fill=border1_color)
    
    return image_with_border3

def add_borders_and_resize_height(image, target_height=1080):
    # Resize the image to the target height, keeping the aspect ratio
    original_width, original_height = image.size
    scale_factor = target_height / original_height
    new_size = (int(original_width * scale_factor), target_height)
    resized_image = image.resize(new_size, Image.LANCZOS)  # Resize using high-quality filter

    # Add the first 1px gray border
    border1_color = (169, 169, 169)
    image_with_border1 = ImageOps.expand(resized_image, border=1, fill=border1_color)
    
    # Add the second 10px white border
    border2_color = (255, 255, 255)
    image_with_border2 = ImageOps.expand(image_with_border1, border=10, fill=border2_color)
    
    # Add the third 1px gray border
    image_with_border3 = ImageOps.expand(image_with_border2, border=1, fill=border1_color)
    
    return image_with_border3

def add_drop_shadow(image, offset=(10, 10), shadow_color=(0, 0, 0, 128), blur_radius=10):
    original = image.convert("RGBA")

    # Calculate the size of the new image (original + offset + blur)
    width, height = original.size
    total_width = width + abs(offset[0]) + blur_radius * 4
    total_height = height + abs(offset[1]) + blur_radius * 4

    # Create a transparent canvas
    transparent_canvas = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))

    # Create the shadow layer
    shadow = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))

    # Create a radial gradient for fading edges
    gradient = np.zeros((total_height, total_width), dtype=np.uint8)

    center_x = blur_radius * 2 + width // 2
    center_y = blur_radius * 2 + height // 2

    # Fill the gradient with fading opacity
    for y in range(total_height):
        for x in range(total_width):
            # Calculate the distance from the shadow center
            dist_x = abs(x - center_x)
            dist_y = abs(y - center_y)
            distance = max(dist_x - width // 2, dist_y - height // 2)

            # Compute alpha based on the distance
            if distance <= 0:
                alpha = 255  # Fully opaque in the central rectangle
            elif distance < blur_radius:
                alpha = 255 - int(255 * (distance / blur_radius))  # Fade out
            else:
                alpha = 0  # Fully transparent outside blur radius

            gradient[y, x] = alpha

    # Convert the gradient to an Image
    gradient_image = Image.fromarray(gradient, mode='L')

    # Paste the gradient on top of the shadow layer
    shadow.paste(shadow_color, (0, 0), mask=gradient_image)

    # Apply Gaussian blur to the shadow for smooth fading
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

    # Composite the shadow onto the transparent canvas
    transparent_canvas = Image.alpha_composite(transparent_canvas, shadow)

    # Paste the original image on top of the shadow
    original_position = (blur_radius * 2 + max(0, -offset[0])-5, blur_radius * 2 + max(0, -offset[1])-13)
    transparent_canvas.paste(original, original_position, mask=original)

    return transparent_canvas

# Combined function
def process_image_width(image_path, output_path, target_width=1080):
    # Step 1: Open the image
    image = Image.open(image_path)
    
    # Step 2: Resize and add borders
    bordered_image = add_borders_and_resize_width(image, target_width=target_width)
    
    # Step 3: Apply drop shadow
    final_image = add_drop_shadow(bordered_image, offset=(10, 20), shadow_color=(0, 0, 0, 150), blur_radius=7)
    
    # Step 4: Save the result
    final_image.save(output_path)
    add_transparent_layer(output_path, "temp/final_output.png")
    return bordered_image.height

# Combined function
def process_image_height(image_path, output_path, target_height=1080):
    # Open the image with Pillow
    image = Image.open(image_path)
    
    # Step 2: Resize and add borders
    bordered_image = add_borders_and_resize_height(image, target_height=target_height)
    
    # Step 3: Apply drop shadow
    final_image = add_drop_shadow(bordered_image, offset=(10, 20), shadow_color=(0, 0, 0, 150), blur_radius=7)
    
    # Step 4: Save the result
    final_image.save(output_path)
    add_transparent_layer(output_path, "temp/final_output.png")
    return final_image
