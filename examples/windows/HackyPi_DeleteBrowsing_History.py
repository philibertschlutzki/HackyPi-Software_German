# This program demonstrate how HackyPi can delete browsing history from specific browser
# This code works for Windows based PC/Laptop but can be modified for Other OS
import time
import board
import usb_hid
import digitalio
import board
import busio
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_hid.keyboard import Keyboard, Keycode
from keyboard_layout_win_uk import KeyboardLayout
from adafruit_st7789 import ST7789

#Declare some parameters used to adjust style of text and graphics
BORDER = 12
FONTSCALE = 3
BACKGROUND_COLOR = 0xFF0000  # red
FOREGROUND_COLOR = 0xFFFF00  # Purple
TEXT_COLOR = 0x0000ff

# Release any resources currently in use for the displays
displayio.release_displays()

tft_clk = board.GP10 # must be a SPI CLK
tft_mosi= board.GP11 # must be a SPI TX
tft_rst = board.GP12
tft_dc  = board.GP8
tft_cs  = board.GP9
spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)

# Make the displayio SPI bus and the GC9A01 display
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
display = ST7789(display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR

# This section switch On the backlight of TFT
tft_bl  = board.GP13
led = digitalio.DigitalInOut(tft_bl)
led.direction = digitalio.Direction.OUTPUT
led.value=True

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# This function creates colorful rectangular box 
def inner_rectangle():
    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(display.width - BORDER * 2, display.height - BORDER * 2, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = FOREGROUND_COLOR
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER)
    splash.append(inner_sprite)
    
#Function to print data on TFT
def print_onTFT(text, x_pos, y_pos): 
    text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
    text_group = displayio.Group(scale=FONTSCALE,x=x_pos,y=y_pos,)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)
    
inner_rectangle()
print_onTFT("Welcome to", 30, 40)
print_onTFT("HackPi", 60, 80)

time.sleep(3)


try:
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayout(keyboard)
    time.sleep(0.5)
    keyboard.send(Keycode.WINDOWS, Keycode.R)
    time.sleep(0.5)
    keyboard_layout.write('cmd.exe')
    keyboard.send(Keycode.ENTER)
    time.sleep(0.3)
    keyboard.send(Keycode.F11)
    time.sleep(0.3)  

    keyboard_layout.write("start chrome") #change name of browser(e.g. start brave) for which history needs to be deleted
    
    keyboard.send(Keycode.ENTER)
    time.sleep(2)
    keyboard.send(Keycode.CONTROL,Keycode.SHIFT,Keycode.DELETE)
    time.sleep(1)
    keyboard.send(Keycode.TAB)
    time.sleep(0.2)
    keyboard.send(Keycode.ENTER)
    
    inner_rectangle()
    print_onTFT("History", 70, 40)
    print_onTFT("Deleted!!", 50, 80)
    
    lst = [0.1,0.01]
    for i in range(len(lst)):
        for j in range(5):
            led.value = True
            time.sleep(lst[i])
            led.value = False
            time.sleep(lst[i])

    led.value = True
    keyboard.release_all()
    
except Exception as ex:
    keyboard.release_all()
    raise ex
