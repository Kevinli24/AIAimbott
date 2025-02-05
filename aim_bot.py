import cv2
import numpy as np
import pyautogui
from pynput import keyboard
import threading
import time

# Define global variable for aimbot state
aimbot_enabled = False
pyautogui.FAILSAFE = False


def detect_red_target(frame):
    """
    Detect red circular targets in the frame using HSV color range.
    Args:
        frame: The game frame captured.
    Returns:
        The coordinates of the target's center, or None if no target is found.
    """
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define red color range in HSV (two ranges to cover the wrap-around)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for both red ranges
    mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)

    # Combine the masks
    red_mask = mask1 + mask2

    # Find contours of the red areas
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            if perimeter == 0:
                continue
            circularity = 4 * np.pi * (area / (perimeter * perimeter))

            # Check if the contour is sufficiently circular
            if circularity > 0.8 and area > 100:  # Adjust thresholds as needed
                x, y, w, h = cv2.boundingRect(contour)
                target_center = (x + w // 2, y + h // 2)
                return target_center
    return None


def move_mouse_to_target(target_pos, screen_center):
    """
    Move the mouse to the detected target position and perform a click.
    Args:
        target_pos: (x, y) coordinates of the target.
        screen_center: (x, y) center of the screen.
    """
    target_x, target_y = target_pos
    screen_x, screen_y = screen_center
    offset_x = target_x - screen_x
    offset_y = target_y - screen_y

    # Move the mouse by the calculated offset
    pyautogui.moveRel(offset_x, offset_y, duration=0.1)

    # Perform a click after moving the mouse
    pyautogui.click()


def toggle_aimbot():
    """
    Listen for the Caps Lock key to toggle the aimbot.
    """
    global aimbot_enabled

    def on_press(key):
        global aimbot_enabled
        if key == keyboard.Key.caps_lock:
            aimbot_enabled = not aimbot_enabled
            print(f"Aimbot {'enabled' if aimbot_enabled else 'disabled'}")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def main():
    # Define the screen region to capture (adjust as needed)
    screen_width, screen_height = pyautogui.size()
    screen_center = (screen_width // 2, screen_height // 2)

    print("Starting the aimbot. Press Caps Lock to toggle, and 'q' to quit.")

    while True:
        if aimbot_enabled:
            # Capture the screen
            screenshot = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Detect the red target
            target_pos = detect_red_target(frame)

            if target_pos:
                move_mouse_to_target(target_pos, screen_center)

            # For debugging: Display the captured frame with target overlay
            if target_pos:
                cv2.circle(frame, target_pos, 10, (0, 255, 0), 2)
            cv2.imshow("Aimbot View", frame)

            # Exit the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            # Sleep briefly to reduce CPU usage when the aimbot is disabled
            time.sleep(0.1)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Run the toggle listener in a separate thread
    toggle_thread = threading.Thread(target=toggle_aimbot)
    toggle_thread.daemon = True
    toggle_thread.start()

    # Start the main aimbot functionality
    main()
