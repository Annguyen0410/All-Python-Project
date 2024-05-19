import cv2
import numpy as np
import matplotlib.pyplot as plt
import yfinance


# Load image
img = cv2.imread(('<img src="data:image/png;base64,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
'))

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur
blur = cv2.GaussianBlur(gray, (5,5), 0)

# Detect edges
edges = cv2.Canny(blur, 50, 200)

# Find contours and draw them on original image
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contour_img = img.copy()
cv2.drawContours(contour_img, contours, -1, (0,255,0), 2)

# Display contour image
plt.imshow(contour_img)
plt.show()
