import tkinter
import json
import math
import random
import pygame
from datetime import datetime
from PIL import ImageTk, Image

class Kamvas:

    def __init__(self):
        self.window = tkinter.Tk()
        self.data_file = "data/data.json"
        self.clock = None
        self.tag = "Empty"
        self.desc = "..."
        self.bg_color = "#E8E8E8"
        self.timer = 0
        self.current_timer = 0
        self.canvas_img = None
        self.logo_label = None
        self.canvas_label = None
        self.text_label = None
        self.paint_button = None
        self.time_slider = None

    #========================== WINDOW =====================================
    def setup(self):
        pygame.mixer.init()

        # Window setup
        self.window.title("Kamvas")
        self.window.geometry("255x511")
        self.window.resizable(width=False, height=False)
        self.window.config(bg=self.bg_color)
        self.window.iconbitmap("img/icon.ico")
        
        # Logo
        tk_logo_img = ImageTk.PhotoImage(Image.open("img/icon.png").resize((45, 45), Image.ANTIALIAS))
        self.logo_label = tkinter.Label(self.window, image=tk_logo_img, bg=self.bg_color)
        self.logo_label.image = tk_logo_img
        self.logo_label.pack(pady=(30,0))

        # Canvas
        self.canvas_img = Image.new('RGB', (128, 128), (255, 255, 255))
        tk_canvas_img = ImageTk.PhotoImage(self.canvas_img)
        self.canvas_label = tkinter.Label(self.window, image=tk_canvas_img, relief='solid', border=1)
        self.canvas_label.image = tk_canvas_img
        self.canvas_label.pack(pady=(20,0))

        # Text and Timer
        self.text_label = tkinter.Label(self.window, text="Καμβάς", font=("Times New Roman", 30), bg=self.bg_color)
        self.text_label.pack(pady=(30,0))

        # Paint & Stain button
        self.paint_button = tkinter.Button(self.window, command=self.paint, text="Paint", font=("Times New Roman", 15), relief='solid', border=1, bg=self.bg_color)
        self.paint_button.pack(ipadx=(10), pady=(5,0))

        # Time slider
        self.time_slider = tkinter.Scale(self.window, length=108, from_=25, to=240, resolution=5, bg=self.bg_color, border=0, orient=tkinter.HORIZONTAL)
        self.time_slider.pack(pady=(50,0))

    def open(self):
        self.window.mainloop()

    #========================== ACTIONS =====================================
    def paint(self):
        if self.timer < 1:
            self.timer = self.time_slider.get() * 60
            self.current_timer = self.timer;

        if self.clock == None:
            self.count_down()
            self.play_toast_sound()
        else:
            if (self.timer - self.current_timer) > 10:
                self.stain_canvas()
                self.update_canvas()
                self.save_session()
                self.play_F_sound()
            else:
                self.reset_canvas()
                self.update_canvas()
                self.play_menu_click_sound()
            
            self.reset_canvas()
            self.stop_painting()

    def stop_painting(self):
        self.window.after_cancel(self.clock)
        self.clock = None
        self.timer = 0
        self.paint_button.config(text="Paint")
        self.text_label.config(text="Καμβάς")

    def count_down(self):
        time_min = math.floor(self.current_timer / 60)
        time_sec = self.current_timer % 60

        if time_min < 10:
            time_min = f"0{time_min}"

        if time_sec < 10:
            time_sec = f"0{time_sec}"
        
        self.text_label.config(text=f"{time_min}:{time_sec}")

        if self.current_timer > 0:
            if (self.timer - self.current_timer) > 10:
                self.paint_button.config(text="Give up")
            else:
                self.paint_button.config(text="Cancel (" + str(self.timer - self.current_timer) + ")")
            
            self.clock = self.window.after(1000, self.count_down)
            self.current_timer -= 1

            self.generate_pixel()
            self.update_canvas()
        else:
            self.save_session()
            self.stop_painting()
            self.play_dragon_end_sound()

    #========================== SOUNDS =====================================
    def play_toast_sound(self):
        pygame.mixer.music.load("audio/toast.ogg")
        pygame.mixer.music.play(loops=0)

    def play_dragon_end_sound(self):
        pygame.mixer.music.load("audio/dragon_end.ogg")
        pygame.mixer.music.play(loops=0)

    def play_F_sound(self):
        pygame.mixer.music.load("audio/F.mp3")
        pygame.mixer.music.play(loops=0)

    def play_menu_click_sound(self):
        pygame.mixer.music.load("audio/menu_click.mp3")
        pygame.mixer.music.play(loops=0)

    #========================== CANVAS UTILS =====================================
    def reset_canvas(self):
        self.canvas_img = Image.new('RGB', (128, 128), (255, 255, 255))

    def stain_canvas(self):
        self.canvas_img = Image.new('RGB', (128, 128), (0, 0, 0))

    def generate_pixel(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = (r, g, b)

        x = random.randint(0, 7) * 16
        y = random.randint(0, 7) * 16
        coords = [x, y, x + 16, y + 16]

        self.canvas_img.paste(color, coords)

    def update_canvas(self):
        tk_img = ImageTk.PhotoImage(self.canvas_img)
        self.canvas_label.configure(image=tk_img)
        self.canvas_label.image = tk_img

    #========================== DATA =====================================
    def read_sessions(self):
        return json.load(open(self.data_file))
        
    def save_session(self):
        tile = Image.new('RGB', (8, 8), (255, 255, 255))

        for i in range(0, 8):
            for j in range(0, 8):
                color = self.canvas_img.getpixel((i * 16, j * 16))
                tile.putpixel((i, j), color)

        date = str(datetime.now().strftime('%Y-%m-%dT%H%M%S'))

        tile.save("data/" + date + ".png")

        data = self.read_sessions()

        data.append({
            "date": date,
            "timer": int(self.timer / 60),
            "tag": self.tag,
            "desc": self.desc
        })

        with open(self.data_file, 'w') as f:
            json.dump(data, f)

kamvas = Kamvas()
kamvas.setup()
kamvas.open()
