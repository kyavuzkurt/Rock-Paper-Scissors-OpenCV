import cv2 as cv
import mediapipe as mp
import random as rd

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_draw = mp.solutions.drawing_utils
        self.computer_gesture = None  
        self.space_pressed = False  
        self.player_score = 0  
        self.computer_score = 0  
        self.winner = None  

    def count_fingers(self, hand_landmarks):
        count = 0
        finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
        for tip in finger_tips:
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:  # Check if tip is above the base
                count += 1
        thumb_tip = 4
        thumb_base = 2
        # Determining the thumb position
        if hand_landmarks.landmark[5].x < hand_landmarks.landmark[17].x:
            # Left side
            if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_base].x:
                count += 1
        else:
            # Right side
            if hand_landmarks.landmark[thumb_tip].x > hand_landmarks.landmark[thumb_base].x:
                count += 1
        return count

    def calculate_gesture(self, finger_count):
        if finger_count == 0:
            return "Rock"
        elif finger_count == 2:
            return "Scissors"
        elif finger_count == 5:
            return "Paper"
        else:
            return "Invalid"

    def get_winner(self, gesture1, gesture2):
        if gesture1 == gesture2:
            return "Draw"
        elif gesture1 == "Rock" and gesture2 == "Scissors":
            self.player_score += 1
            return "Player  wins"
        elif gesture1 == "Scissors" and gesture2 == "Paper":
            self.player_score += 1
            return "Player  wins"
        elif gesture1 == "Paper" and gesture2 == "Rock":
            self.player_score += 1
            return "Player  wins"
        else:
            self.computer_score += 1
            return "Computer wins"

    def detect_hands(self, frame):
        img_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                valid_gestures = [0, 2, 5]
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                finger_count = self.count_fingers(hand_landmarks)
                gesture = self.calculate_gesture(finger_count)
                cv.putText(frame, f'You: {gesture}', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if self.space_pressed:
                    self.computer_gesture = self.calculate_gesture(rd.choice(valid_gestures))
                    self.winner = self.get_winner(gesture, self.computer_gesture)
                    self.space_pressed = False  # Reset flag after generating gesture
                if self.computer_gesture:
                    cv.putText(frame, f'Computer: {self.computer_gesture}', (10, 60), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv.putText(frame, f'Winner: {self.winner}', (10, 90), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv.putText(frame, f'Player Score: {self.player_score}', (10, 120), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv.putText(frame, f'Computer Score: {self.computer_score}', (10, 150), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return frame

    def start_video_capture(self):
        cap = cv.VideoCapture(0)
        while True:
            success, frame = cap.read()
            if not success:
                break

            frame = self.detect_hands(frame)
            cv.imshow("Hand Detection", frame)

            key = cv.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '):
                self.space_pressed = True 

        cap.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    detector = HandDetector()
    detector.start_video_capture()