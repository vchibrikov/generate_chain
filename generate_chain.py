# Import packages
import numpy as np
import os
import cv2
import pandas as pd
import math

# Define function to create white image with same size as input image
def create_white_image(image):
    white_image = np.ones(image.shape, dtype=np.uint8) * 255
    return white_image

# Define the function to handle mouse events
def mouse_callback(event, x, y, flags, params):

    # If left mouse button is pressed
    if event == cv2.EVENT_LBUTTONDOWN and len(params['points']) < 6000:
        
        # Add the point to the list
        params['points'].append((x, y))

        # Track clicks
        print('Filename: ', filename ,' | Click number: ', len(params['points']))

        # Draw a circle at the point
        cv2.circle(params['image'], (x, y), 3, (0, 0, 255), -1)

        # Update the display
        cv2.imshow('image', params['image'])

        # If the list of points contains a multiple of 2 points, draw a line between them
        if event == cv2.EVENT_LBUTTONDOWN and len(params['points']) > 1:

            # Define the points
            point1 = params['points'][-2]
            point2 = params['points'][-1]

            # Draw a line between the points
            cv2.line(params['image'], point1, point2, (0, 0, 255), 3)

            # Draw the same line on the white image
            cv2.line(white_image, point1, point2, (0, 0, 255), 3)

            # Save the white image with the line
            cv2.imwrite(os.path.join(path, filename_short + '_lines.tiff'), white_image)

            # Update the display
            cv2.imshow('image', params['image'])

            # Write an image
            # cv2.imwrite(os.path.join(path, filename), params['image'])

        # If right mouse button is pressed, appear following clicks as a separate chain
    if event == cv2.EVENT_RBUTTONDOWN and len(params['points']) < 6000:

        # Add the point to the list
        params['points'].append((x, y))

        # Track clicks
        print('Fiber changed. Filename: ', filename ,' | Click number: ', len(params['points']))

        # Draw a circle at the point
        cv2.circle(params['image'], (x, y), 3, (0, 0, 255), -1)

        # Update the display
        cv2.imshow('image', params['image'])

# Define the folder containing the images
folder = '/Users/---/Desktop/---/generate_chain/input/' 
path = '/Users/---/Desktop/---/generate_chain/output/'

# Define the extensions of the image files
extensions = ('.jpeg','.tiff', '.jpg', '.tif')

# Iterate over the images in the folder
for filename in os.listdir(folder):
    if filename.lower().endswith(extensions):

        filename_short = filename.replace('.tiff', '')

        # Load the image
        image = cv2.imread(os.path.join(folder, filename))

        # Create a copy of the image for display purposes
        image_copy = image.copy()

        # Create a white image to draw lines on
        white_image = create_white_image(image)

        # Define the dictionary of parameters to be passed to the mouse callback function
        params = {'image': image_copy, 'filename': filename, 'points': []}

        # Create a window to display the image
        cv2.namedWindow("image", cv2.WINDOW_FULLSCREEN)

        # Set the mouse callback function
        cv2.setMouseCallback("image", mouse_callback, params)

        # Show the image and wait for user to select points
        cv2.imshow("image", image)
        cv2.setMouseCallback("image", mouse_callback, params)
        cv2.waitKey(0)