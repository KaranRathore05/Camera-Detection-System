import cv2
import time
from loitering import check_loitering

# Initialize HOG person detector (AI model)
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def start_camera():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    time.sleep(2)

    if not cap.isOpened():
        print("Camera error")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (800, 600))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect people
        boxes, weights = hog.detectMultiScale(
            gray,
            winStride=(8, 8),
            padding=(16, 16),
            scale=1.03
        )

        person_id = 0  # reset every frame

        for i, (x, y, w, h) in enumerate(boxes):
            if weights[i] < 0.6:
                continue

            person_id += 1

            # CHECK LOITERING
            is_loitering = check_loitering(person_id)

            color = (0, 255, 0)
            label = "Normal"

            if is_loitering:
                color = (0, 0, 255)
                label = "LOITERING"

                with open("alerts.log", "a") as f:
                    f.write(f"Loitering detected at {time.ctime()}\n")

            # Draw box + label
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(
                frame,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

        cv2.imshow("Smart Surveillance", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

start_camera()
