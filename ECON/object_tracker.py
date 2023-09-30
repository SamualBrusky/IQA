import cv2
import numpy as np

# Function to detect and locate blue objects
def detect_blue_color(frame):
    # Convert the frame to the HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the blue color
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Create a mask to isolate the blue color
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

    # Find the contours of the blue objects
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize a list to store the positions of blue objects
    blue_positions = []

    # Iterate through the contours and find the centroid of each blue object
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Ignore small noise
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                blue_positions.append((cx, cy))

                # Draw a circle around the detected blue object
                cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)

    return frame, blue_positions

# Main program
if __name__ == "__main__":
    # Initialize the video capture (you can also use cv2.imread for images)
    cap = cv2.VideoCapture(0)  # 0 for default camera

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        result_frame, blue_positions = detect_blue_color(frame)

        # Display the frame with detected blue objects
        cv2.imshow("Blue Color Detection", result_frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()
