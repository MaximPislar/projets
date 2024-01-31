from tkinter import *
from tkinter import ttk
from random import randint
import pygame

delete_blobs = 0                                # для счетчика очков
bee_direction = 0                               # переменная для передвижения пчелы
heart_quantity = 2                              # переменная для изменения количества жизней
blob_list = []                                  # для генерации капель
bee_status = True                               # жива ли пчела
heart_tag = 0                                   # тег для удаления сердец

def start():
    global c0, top_canvas, c, bee0, btn0, bee_status, heart0, heart1, heart2
    bee_status = True
    btn0.destroy()
    c0 = Canvas(bg="lightgrey", height=25)
    top_canvas = c0.create_text(30, 15, text=f"Счёт: {delete_blobs}")
    c0.pack(fill=X)

    c = Canvas()
    c.pack(expand=True, fill=BOTH)

    heart0 = Heart(430)
    heart1 = Heart(440)
    heart2 = Heart(450)

    bee0 = Bee(c, tag="b0", x=20, y=270)

    rain_1()
    root.bind('<Up>', lambda event, direct="Up": bee0.bee_move_event(event, direct))
    root.bind('<Down>', lambda event, direct="Down": bee0.bee_move_event(event, direct))
    root.bind('<Right>', lambda event, direct="Right": bee0.bee_move_event(event, direct))
    root.bind('<Left>', lambda event, direct="Left": bee0.bee_move_event(event, direct))


def restart():
    global delete_blobs, bee_direction, heart_quantity, blob_list, bee_status, bee0, heart_tag
    c0.destroy()
    c.destroy()
    bee0 = 0
    delete_blobs = 0
    bee_direction = 0
    heart_quantity = 2
    blob_list = []
    bee_status = True
    heart_tag = 0
    start()



def end_lvl():
    global bee_direction, bee_status
    bee_direction = "Death"
    bee_status = False
    bee0.bee_death_down()


def score_update():
    c0.itemconfig(top_canvas, text=f"Счёт: {delete_blobs}")


def bees_health_delete():
    global heart_quantity
    heart_tag = f"heart{heart_quantity}"
    c0.delete(heart_tag)
    heart_quantity -= 1
    if heart_quantity == -1:
        end_lvl()
        c.create_text(250, 210, text=f'Ваш счёт: {delete_blobs}')


def stolknovenie():
    pygame.mixer.init()
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play()
    bees_health_delete()


def mouse_coord(event):                    # координаты мыши в названии окна
    x = event.x
    y = event.y
    root.title(f'{x}x{y}')


def rain_1():
    for i in range(100):
        x_coord = randint(0, 500)
        y_coord = randint(-4000, 0)
        blob = Blob(c, x_coord, y_coord, c0)
        blob_list.append(blob)
        root.update()


class Heart:

    def __init__(self, x):
        global heart_tag
        self.tag = f"heart{heart_tag}"
        heart_tag += 1
        self.heart0 = c0.create_oval(x, 10, x+5, 15, fill="red", outline="red", tags=self.tag)
        self.heart1 = c0.create_oval(x+5, 10, x+10, 15, fill="red", outline="red", tags=self.tag)
        self.heart2 = c0.create_polygon(x, 12, x+11, 12, x+5, 20, fill="red", tags=self.tag)



class Blob:

    hit_line_x = [i for i in range(20, 100)]         # списки необходимые для хитбокса
    hit_line_y = [i for i in range(270, 295)]        # списки необходимые для хитбокса
    blob_tag = 0                                     # переменная для тэга капель

    def __init__(self, canvas, x, y, info_canvas):
        self.info_canvas = info_canvas
        self.canvas = canvas
        self.tag = f"blob{Blob.blob_tag}"
        self.blob_part_0 = canvas.create_oval(x, y, x+20, y+20, fill='lightblue', outline='lightblue', tags=self.tag)
        self.blob_part_1 = canvas.create_polygon((x-1, y+10), (x+10, y-7), (x+22, y+10),
                                                 fill='lightblue', tags=self.tag)
        self.x, self.y, *rest = canvas.coords(self.blob_part_0)
        self.speed = 13        # скорость капли
        Blob.blob_tag += 1
        self.blob_move()

    def blob_move(self):
        if bee_status:
            global delete_blobs
            c.move(self.tag, 0, 1)
            if self.canvas.coords(self.blob_part_0)[1]+20 in Blob.hit_line_y:       # проверка на попадание в пчелу
                if (self.canvas.coords(self.blob_part_0)[0] in Blob.hit_line_x or
                        self.canvas.coords(self.blob_part_0)[0]+20 in Blob.hit_line_x):
                    stolknovenie()
                    self.canvas.delete(self.tag)
                    return None             # ретёрн здесь для того чтобы прерывать функцию после удаления капли
            if self.canvas.coords(self.blob_part_0)[1] <= 550:  # удаление капли за пределами экрана
                root.after(self.speed, self.blob_move)
            else:
                delete_blobs += 1
                if bee_status:
                    score_update()
                self.canvas.delete(self.tag)


class Bee:
    def __init__(self, canvas, tag, x, y):
        self.canvas = canvas
        self.tag = tag
        self.bee0 = canvas.create_oval(x, y, x+40, y+25, fill='orange', tags=self.tag)    # отрисовка пчелы
        self.bee1 = canvas.create_oval(x+40, y, x+70, y+20, fill='orange', tags=self.tag)
        self.bee2 = canvas.create_oval(x+70, y, x+80, y+20, fill='orange', tags=self.tag)
        self.bee3 = canvas.create_oval(x+74, y+5, x+77, y+13, fill='black', tags=self.tag)
        self.antena = canvas.create_line(x+76, y+6, x+86, y-2, tags=self.tag)
        self.leg0 = canvas.create_line(x+47, y+15, x+29, y+34, width=2, tags=self.tag)
        self.leg1 = canvas.create_line(x+54, y+18, x+49, y+33, width=1.5, tags=self.tag)
        self.leg2 = canvas.create_line(x+62, y+15, x+64, y+27, width=1.5, tags=self.tag)
        self.lane = canvas.create_line(x+12, y+1, x+10, y+24, width=3, fill='brown', tags=self.tag)
        self.lane1 = canvas.create_line(x+22, y+1, x+19, y+25, width=3, fill='brown', tags=self.tag)
        self.lane2 = canvas.create_line(x+30, y+2, x+29, y+23, width=3, fill='brown', tags=self.tag)
        self.wing0 = canvas.create_arc(x+20, y-70, x+60, y+45,
                                       start=240, extent=100,
                                       style=CHORD, fill='lightblue', tags=self.tag)
        self.wing1 = canvas.create_arc(x+20, y-50, x+60, y+45,
                                       start=340, extent=120,
                                       style=CHORD, fill='lightblue', tags=self.tag)
        # self.rect = canvas.create_rectangle(x,y,x+80,y+25, tags=self.tag)     визуализация хитбокса



    def bee_move_event(self, event, direct):
        global bee_direction
        if direct == "Up" and bee_direction != "Death":
            bee_direction = "Up"
            self.bee_move_up()
        elif direct == "Down" and bee_direction != "Death":
            bee_direction = "Down"
            self.bee_move_down()
        elif direct == "Right" and bee_direction != "Death":
            bee_direction = "Right"
            self.bee_move_right()
        elif direct == "Left" and bee_direction != "Death":
            bee_direction = "Left"
            self.bee_move_left()

    def bee_move_up(self):
        global bee_direction
        if bee_direction == "Up":
            if self.canvas.coords(self.bee0)[1] >= 5:
                self.canvas.move(self.tag, 0, -1)
                Blob.hit_line_x = [i for i in range(int(self.canvas.coords(self.bee0)[0]),
                                                    int(self.canvas.coords(self.bee0)[0]+80))]
                Blob.hit_line_y = [i for i in range(int(self.canvas.coords(self.bee0)[1]),
                                                    int(self.canvas.coords(self.bee0)[1]+25))]
                root.after(10, self.bee_move_up)

    def bee_move_down(self):
        global bee_direction
        if bee_direction == "Down":
            if self.canvas.coords(self.bee0)[1] <= 470:
                self.canvas.move(self.tag, 0, 1)
                Blob.hit_line_x = [i for i in
                                   range(int(self.canvas.coords(self.bee0)[0]),
                                         int(self.canvas.coords(self.bee0)[0]+80))]
                Blob.hit_line_y = [i for i in
                                   range(int(self.canvas.coords(self.bee0)[1]),
                                         int(self.canvas.coords(self.bee0)[1]+25))]
                root.after(10, self.bee_move_down)

    def bee_move_right(self):
        global bee_direction
        if bee_direction == "Right":
            if self.canvas.coords(self.bee0)[0] <= 416:
                self.canvas.move(self.tag, 1, 0)
                Blob.hit_line_x = [i for i in
                                   range(int(self.canvas.coords(self.bee0)[0]),
                                         int(self.canvas.coords(self.bee0)[0]+80))]
                Blob.hit_line_y = [i for i in
                                   range(int(self.canvas.coords(self.bee0)[1]),
                                         int(self.canvas.coords(self.bee0)[1]+25))]
                root.after(10, self.bee_move_right)

    def bee_move_left(self):
        global bee_direction
        if bee_direction == "Left":
            if self.canvas.coords(self.bee0)[0] >= 3:
                self.canvas.move(self.tag, -1, 0)
                Blob.hit_line_x = [i for i in
                                   range(int(self.canvas.coords(self.bee0)[0]),
                                         int(self.canvas.coords(self.bee0)[0]+80))]
                Blob.hit_line_y = [i for i in
                                   range(int(self.canvas.coords(self.bee0)[1]),
                                         int(self.canvas.coords(self.bee0)[1]+25))]
                root.after(10, self.bee_move_left)

    def bee_death_down(self):
        global bee_direction
        if bee_direction == "Death":
            self.canvas.move(self.tag, 0, 1)
            Blob.hit_line_x = [i for i in
                               range(int(self.canvas.coords(self.bee0)[0]),
                                     int(self.canvas.coords(self.bee0)[0] + 80))]
            Blob.hit_line_y = [i for i in
                               range(int(self.canvas.coords(self.bee0)[1]),
                                     int(self.canvas.coords(self.bee0)[1] + 25))]
            root.after(5, self.bee_death_right)

    def bee_death_right(self):
        global bee_direction
        if bee_direction == "Death":
            if self.canvas.coords(self.bee0)[0] <= 550:
                self.canvas.move(self.tag, 1, 0)
                Blob.hit_line_x = [i for i in
                                   range(int(self.canvas.coords(self.bee0)[0]),
                                         int(self.canvas.coords(self.bee0)[0] + 80))]
                Blob.hit_line_y = [i for i in
                                   range(int(self.canvas.coords(self.bee0)[1]),
                                         int(self.canvas.coords(self.bee0)[1] + 25))]
                root.after(5, self.bee_death_down)
            elif self.canvas.coords(self.bee0)[0] >= 550:
                btn = ttk.Button(text="Рестарт", command=restart)
                self.canvas.create_window(200, 225, anchor=NW, window=btn, width=100, height=50)


root = Tk()
# root.resizable(False, False)   # растягивание окна
root.geometry("500x525")
root.title("БджоЛЯЯЯЯ")
root.bind('<Motion>', mouse_coord)    # координаты мыши

btn0 = ttk.Button(text="Ну чё народ погнали нахуй...", command=start)
btn0.pack(expand=1)

root.mainloop()


"""
задачи: анимация крыльев, уровни

Выполнено: счёт, жизни, анимация падения, кнопка старт
"""