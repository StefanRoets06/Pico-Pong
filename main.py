import time
from lcd_display import LCD_1inch14  # Import the LCD display class

# Initialize the LCD display
lcd = LCD_1inch14()

def draw_loading_bar(progress):
    # Clear the screen (Redraw the entire screen)
    lcd.fill(lcd.black)
    
    # Draw the loading bar background (gray)
    lcd.rect(20, 60, 200, 20, lcd.white)
    
    # Draw the filled part of the loading bar based on the progress
    lcd.fill_rect(20, 60, int(progress * 200), 20, lcd.white)  # Scale progress to the width (200 px)
    
    # Show the progress text
    lcd.text("Loading...", 80, 30, lcd.white)
    
    # Update the display
    lcd.show()

def fake_loading():
    # Simulate a fake loading process
    for progress in range(30):
        draw_loading_bar(progress / 30)  # Update the progress bar
        time.sleep(0.05)  # Adjust the delay for the speed of the loading bar

# Run the fake loading bar
fake_loading()

# After the loading completes, import and run pong.py
import pong
