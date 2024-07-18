from PIL import Image, ImageDraw

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_gradient_image(width, height, top_color, bottom_left_color, bottom_right_color, top_dominance=1):
    """
    Create a gradient image where the top color dominates more of the top area.

    Parameters:
    width (int): Width of the image.
    height (int): Height of the image.
    top_color (tuple): RGB tuple for the top color.
    bottom_left_color (tuple): RGB tuple for the bottom left color.
    bottom_right_color (tuple): RGB tuple for the bottom right color.
    top_dominance (float): Fraction of the height that the top color should dominate.

    Returns:
    Image: Generated gradient image.
    """
    gradient = Image.new('RGB', (width, height), color=0)
    draw = ImageDraw.Draw(gradient)
    
    for y in range(height):
        for x in range(width):
            if y < top_dominance * height:
                blend_factor = y / (top_dominance * height)
            else:
                blend_factor = 1 + (y - top_dominance * height) / ((1 - top_dominance) * height)

            r = int(top_color[0] * (1 - blend_factor) + ((bottom_left_color[0] * (width - x) + bottom_right_color[0] * x) / width) * blend_factor)
            g = int(top_color[1] * (1 - blend_factor) + ((bottom_left_color[1] * (width - x) + bottom_right_color[1] * x) / width) * blend_factor)
            b = int(top_color[2] * (1 - blend_factor) + ((bottom_left_color[2] * (width - x) + bottom_right_color[2] * x) / width) * blend_factor)

            draw.point((x, y), (r, g, b))
    
    return gradient

# Define the colors (RGB tuples)
top_color = '#c9c9c9'        # White
bottom_left_color = (255, 0, 0)     # Red
bottom_right_color = (0, 0, 255)    # Blue

# Create the gradient image
gradient_image = create_gradient_image(2300, 3300, hex_to_rgb(top_color), bottom_left_color, bottom_right_color)
gradient_image.save("gradient_background.png")