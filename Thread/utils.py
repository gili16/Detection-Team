import cv2

def draw_bbox_with_text(image, bbox, text, color=(0, 255, 0), thickness=2, font_scale=0.5):
    """
    Draws a bounding box with a label on an image.
    
    Parameters:
        image (numpy array): The image to draw on.
        bbox (tuple): The bounding box coordinates in the format (x1, y1, x2, y2).
        text (str): The label to display.
        color (tuple): The color of the bounding box and text in BGR format (default is green).
        thickness (int): Thickness of the bounding box lines (default is 2).
        font_scale (float): Scale of the font for the label text (default is 0.5).
    
    Returns:
        image (numpy array): The image with the bounding box and label drawn on it.
    """
    x1, y1, x2, y2 = bbox
    
    # Draw the bounding box
    cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
    
    # Get the text size to place it appropriately
    text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
    
    # Draw a filled rectangle for the text background
    cv2.rectangle(image, (x1, y1 - text_size[1] - 4), (x1 + text_size[0], y1), color, -1)
    
    # Put the label text on the image
    cv2.putText(image, text, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
    
    return image

import cv2

def draw_line(image, line_start, line_end, color=(0, 255, 0), thickness=2):
    """
    Draws a line on the image.

    Args:
        image (numpy array): The image on which to draw the line.
        line_start (tuple): Starting point of the line as (x1, y1).
        line_end (tuple): Ending point of the line as (x2, y2).
        color (tuple): Color of the line in (B, G, R) format (default: green).
        thickness (int): Thickness of the line (default: 2).

    Returns:
        image (numpy array): The image with the line drawn on it.
    """
    # Draw the line on the image
    cv2.line(image, line_start, line_end, color, thickness)
    
    return image


import cv2

def put_text_top_center(image, text, color=(255, 255, 255), font_scale=1, thickness=2):
    """
    Puts the given text at the top center of the image.

    Args:
        image (numpy array): The image on which to put the text.
        text (str): The text to display.
        color (tuple): The color of the text in (B, G, R) format (default: white).
        font_scale (float): The scale of the font (default: 1).
        thickness (int): Thickness of the text (default: 2).

    Returns:
        image (numpy array): The image with the text placed at the top center.
    """
    # Get the image dimensions
    img_height, img_width = image.shape[:2]

    # Get the text size
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]

    # Calculate the text's starting position (top center)
    text_x = (img_width - text_size[0]) // 2  # Center the text horizontally
    text_y = text_size[1] + 10  # Add some padding from the top

    # Put the text on the image
    cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

    return image