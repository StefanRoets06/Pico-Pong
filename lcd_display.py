from machine import Pin, SPI
import framebuf

# LCD Pin configuration
BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9
WIDTH = 240
HEIGHT = 135

# Button Pin configuration
BUTTONS = {
    "A": Pin(15, Pin.IN, Pin.PULL_UP),
    "B": Pin(17, Pin.IN, Pin.PULL_UP),
    "UP": Pin(2, Pin.IN, Pin.PULL_UP),
    "MIDDLE": Pin(3, Pin.IN, Pin.PULL_UP),
    "LEFT": Pin(16, Pin.IN, Pin.PULL_UP),
    "DOWN": Pin(18, Pin.IN, Pin.PULL_UP),
    "RIGHT": Pin(20, Pin.IN, Pin.PULL_UP),
}

class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT

        self.cs = Pin(CS, Pin.OUT)
        self.rst = Pin(RST, Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(SCK), mosi=Pin(MOSI))
        self.dc = Pin(DC, Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        # Color constants in RGB565 format
        self.green   = 0x001F   # Green
        self.red     = 0x07E0   # Red
        self.blue    = 0xF800   # Blue
        self.white   = 0xFFFF   # White
        self.black   = 0x0000   # Black

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        self.rst(1)
        self.rst(0)
        self.rst(1)

        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A)
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35)

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F)

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        for d in [0xD0, 0x04, 0x0D, 0x11, 0x13, 0x2B, 0x3F, 0x54, 0x4C, 0x18, 0x0D, 0x0B, 0x1F, 0x23]:
            self.write_data(d)

        self.write_cmd(0xE1)
        for d in [0xD0, 0x04, 0x0C, 0x11, 0x13, 0x2C, 0x3F, 0x44, 0x51, 0x2F, 0x1F, 0x1F, 0x20, 0x23]:
            self.write_data(d)

        self.write_cmd(0x21)
        self.write_cmd(0x11)
        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)

        self.write_cmd(0x2C)

        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)

    def read_buttons(self):
        return {name: not pin.value() for name, pin in BUTTONS.items()}

    def is_pressed(self, name):
        pin = BUTTONS.get(name.upper())
        return pin is not None and not pin.value()
