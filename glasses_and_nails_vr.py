import cv2
import mediapipe as mp
import numpy as np

# Initialize mediapipe pose, face mesh, and hands classes.
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

# Initialize the pose, face mesh, and hands models.
pose = mp_pose.Pose()
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Load the glasses and nail images with alpha channel.
glasses_img = cv2.imread('images/blackglasses-removebg-preview (3).png', cv2.IMREAD_UNCHANGED)
nail_image = cv2.imread('images/nail (1).png', cv2.IMREAD_UNCHANGED)

# Function to calculate the circumference of landmarks.
def calculate_circumference(landmarks, frame):
    points = []
    for landmark in landmarks:
        x = int(landmark.x * frame.shape[1])
        y = int(landmark.y * frame.shape[0])
        points.append((x, y))

    circumference = 0
    for i in range(len(points) - 1):
        circumference += np.sqrt((points[i + 1][0] - points[i][0]) ** 2 + (points[i + 1][1] - points[i][1]) ** 2)
    circumference += np.sqrt((points[0][0] - points[-1][0]) ** 2 + (points[0][1] - points[-1][1]) ** 2)
    return circumference

# Function to overlay transparent image.
def overlay_transparent(background, overlay, x, y, scale=1):
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape
    rows, cols, _ = background.shape
    if x >= cols or y >= rows:
        return background
    y1, y2 = max(0, y - h // 2), min(rows, y + h // 2)
    x1, x2 = max(0, x - w // 2), min(cols, x + w // 2)
    y1o, y2o = max(0, -y + h // 2), min(h, rows - y + h // 2)
    x1o, x2o = max(0, -x + w // 2), min(w, cols - x + w // 2)
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return background
    alpha_overlay = overlay[y1o:y2o, x1o:x2o, 3] / 255.0
    alpha_background = 1.0 - alpha_overlay
    for c in range(0, 3):
        background[y1:y2, x1:x2, c] = (
                alpha_overlay * overlay[y1o:y2o, x1o:x2o, c] +
                alpha_background * background[y1:y2, x1:x2, c]
        )
    return background

# Function to overlay glasses on the face.
def overlay_glasses(frame, glasses_img, eye_landmarks, scale=1.2):
    # Calculate the bounding box for the glasses based on eye landmarks
    x_min = min([int(landmark.x * frame.shape[1]) for landmark in eye_landmarks])
    x_max = max([int(landmark.x * frame.shape[1]) for landmark in eye_landmarks])
    y_min = min([int(landmark.y * frame.shape[0]) for landmark in eye_landmarks])
    y_max = max([int(landmark.y * frame.shape[0]) for landmark in eye_landmarks])

    glasses_width = int((x_max - x_min) * scale)
    glasses_height = int(glasses_width * (glasses_img.shape[0] / glasses_img.shape[1]))

    # Resize the glasses image to fit the eyes
    resized_glasses = cv2.resize(glasses_img, (glasses_width, glasses_height))

    # Calculate the position to place the glasses
    y_offset = y_min - int(glasses_height / 2)
    x_offset = x_min - int((glasses_width - (x_max - x_min)) / 2)

    # Extract the alpha channel from the glasses image
    alpha_s = resized_glasses[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    # Overlay the glasses image on the frame
    for c in range(0, 3):
        frame[y_offset:y_offset + glasses_height, x_offset:x_offset + glasses_width, c] = (
            alpha_s * resized_glasses[:, :, c] + alpha_l * frame[y_offset:y_offset + glasses_height, x_offset:x_offset + glasses_width, c]
        )

# Start capturing video input from the webcam.
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame.")
        break

    # Convert the BGR image to RGB.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and detect the pose, face mesh, and hands.
    pose_result = pose.process(rgb_frame)
    face_result = face_mesh.process(rgb_frame)
    hands_result = hands.process(rgb_frame)

    face_circumference = 0
    left_hand_circumference = 0
    right_hand_circumference = 0

    # Draw the face mesh annotation on the frame.
    if face_result.multi_face_landmarks:
        for face_landmarks in face_result.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                face_landmarks,
                mp_face_mesh.FACEMESH_CONTOURS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
            )

            face_circumference = calculate_circumference(face_landmarks.landmark, frame)
            cv2.putText(frame, f"Face Circumference: {int(face_circumference)} pixels", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Define the indices for the left and right eyes
            left_eye_indices = [33, 133]  # Inner corner, outer corner of the left eye
            right_eye_indices = [362, 263]  # Inner corner, outer corner of the right eye

            # Collect landmarks for the left and right eyes
            left_eye_landmarks = [face_landmarks.landmark[i] for i in left_eye_indices]
            right_eye_landmarks = [face_landmarks.landmark[i] for i in right_eye_indices]

            # Overlay the glasses image on the frame
            overlay_glasses(frame, glasses_img, left_eye_landmarks + right_eye_landmarks, scale=1.2)

    # Draw the pose annotation on the frame.
    if pose_result.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            pose_result.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
        )

        # Define the indices for the left and right hands
        left_hand_indices = [15, 17, 19, 21]  # Wrist, pinky, index, thumb
        right_hand_indices = [16, 18, 20, 22]  # Wrist, pinky, index, thumb

        # Collect landmarks for the left and right hands.
        left_hand_landmarks = [pose_result.pose_landmarks.landmark[i] for i in left_hand_indices]
        right_hand_landmarks = [pose_result.pose_landmarks.landmark[i] for i in right_hand_indices]

        # Calculate the circumferences for the hands.
        left_hand_circumference = calculate_circumference(left_hand_landmarks, frame)
        right_hand_circumference = calculate_circumference(right_hand_landmarks, frame)

        # Display the circumferences on the frame.
        cv2.putText(frame, f"Left Hand Circumference: {int(left_hand_circumference)} pixels", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Right Hand Circumference: {int(right_hand_circumference)} pixels", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Overlay nails on the hand landmarks.
    if hands_result.multi_hand_landmarks:
        for hand_landmarks in hands_result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
            )

            # Define the indices for the nail regions on each finger (tip and adjacent joints)
            finger_indices = {
                'thumb': 4,
                'index': 8,
                'middle': 12,
                'ring': 16,
                'pinky': 20
            }

            for finger, index in finger_indices.items():
                landmark = hand_landmarks.landmark[index]
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])

                # Overlay the nail image with center alignment
                frame = overlay_transparent(frame, nail_image, x, y, scale=0.5)

    # Display the frame.
    cv2.imshow('Body and Face Circumference and Hand Nail Overlay', frame)

    # Break the loop when 'q' is pressed.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the display window.
cap.release()
cv2.destroyAllWindows()
