import cv2

class DroneController:
    def __init__(self):
        self.is_flying = False

    def start_flying(self):
        if not self.is_flying:
            self.is_flying = True
            print("Command received: START")
            print("Drone is now flying")
        else:
            print("Drone is already flying")

    def stop_flying(self):
        if self.is_flying:
            self.is_flying = False
            print("Command received: STOP")
            print("Drone stopped")
        else:
            print("Drone is already stopped")


def main():
    controller = DroneController()
    detector = cv2.QRCodeDetector()

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: camera not found")
        return

    last_command = ""

    print("Show QR code with START or STOP command")
    print("Press Q to exit")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: cannot read camera frame")
            break

        data, bbox, _ = detector.detectAndDecode(frame)

        if data:
            command = data.strip().upper()

            if command != last_command:
                if command == "START":
                    controller.start_flying()
                    last_command = command

                elif command == "STOP":
                    controller.stop_flying()
                    last_command = command

                else:
                    print(f"Unknown QR command: {command}")

            if bbox is not None:
                bbox = bbox.astype(int)
                for i in range(len(bbox[0])):
                    pt1 = tuple(bbox[0][i])
                    pt2 = tuple(bbox[0][(i + 1) % len(bbox[0])])
                    cv2.line(frame, pt1, pt2, (255, 0, 0), 3)

            cv2.putText(
                frame,
                f"QR: {command}",
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        cv2.imshow("QR Flight Command System", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    



