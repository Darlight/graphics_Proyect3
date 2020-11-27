"""
Universidad del Valle de Guatemala
Curso de Graficas por computadora
Lic. Dennis Aldana 
Lab4
Mario Perdomo
Carnet 18029
"""
import pygame
from math import pi, cos, sin, atan2

#Fps to show ingame
CLOCK = pygame.time.Clock()

colors = {
    "1":(255,0,0),
    "2":(0,255,0),
    "3":(0,0,255)
}
#Walls regarding Megaman Snes Tiles, thin it's the first game
wall1 = pygame.image.load('./sprites/wall1.png')
wall2 = pygame.image.load('./sprites/wall2.png')
wall3 = pygame.image.load('./sprites/wall3.png')
wall4 = pygame.image.load('./sprites/wall4.png')
wall5 = pygame.image.load('./sprites/wall5.png')


enemies = [
  {
    "x": 100,
    "y": 190,
    "texture": pygame.image.load('./sprites/mob1.png')
  },
  {
    "x": 400,
    "y": 220,
    "texture": pygame.image.load('./sprites/mob2.png')
  },
  {
    "x": 125,
    "y": 330,
    "texture": pygame.image.load('./sprites/mob3.png')
  },
  {
    "x": 400,
    "y": 325,
    "texture": pygame.image.load('./sprites/mob4.png')
  }
]

textures = {
    "1": wall1,
    "2": wall2,
    "3": wall3,
    "4": wall4,
    "5": wall5
}
#More sprites to cover inside the gamme
hud = pygame.image.load('./sprites/hud.png')
hand = pygame.image.load('./sprites/LaserGun.png')
white = (255,255,255)
black = (0,0,0)
random_color = (0,155,255)
face = pygame.image.load('./sprites/face.png')
zero = pygame.image.load('./sprites/0.png')
two = pygame.image.load('./sprites/2.png')
three = pygame.image.load('./sprites/3.png')
music_meter = pygame.image.load('./sprites/nostalgia.png')
#size of the enemies divided by the blocksize
aspect_ratio = 128/50
#size of the tiles divided by the blocksize
sprite = 128
#tiles_ratio_width = 100/50
#tiles_ratio_height = 98/50
#
#menu screen props
logo = pygame.image.load('./sprites/megaman_logo.png')

class Raycaster:
    def __init__(self, screen):
        _, _, self.width, self.height = screen.get_rect()
        self.screen = screen
        self.blocksize = 50
        self.map = []
        #
        self.player = {
            "x": self.blocksize + 25,
            "y": self.blocksize + 25,
            "j": 0,
            "a": 0,
            "fov": pi/3
        }
        #map atributes
        self.zbuffer = [-float('inf') for z in range(0, 500)]

    def point(self, x, y, c):
        screen.set_at((x, y), c)

    def draw_rectangle(self, x, y, texture):
        for cx in range(x, x + self.blocksize):
            for cy in range(y, y + self.blocksize):
                tx = int((cx - x)*aspect_ratio)
                ty = int((cy - y)*aspect_ratio)
                c = texture.get_at((tx, ty))
                self.point(cx, cy, c)

    def draw_stake(self, x, h, texture, tx):
        start = int(250 - h*0.5) + self.player["j"]
        end = int(250 + h*0.5)
        for y in range(start, end):
            #modificador de la altura
            ty = int(((y - start)*sprite)/(end - start))
            c = texture.get_at((tx, ty))
            #^ mejorar la resolucion de cada sprite y tile
            self.point(x, y, c)


    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))
    
    def cast_ray(self, a):
        d = 0
        while True:
            x = self.player["x"] + d * cos(a)
            y = self.player["y"] + d * sin(a)

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)
            if self.map[j][i] != ' ':
                hitx = x - i*50
                hity = y - j*50

                if 1< hitx < 49:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit* aspect_ratio)

                return d, self.map[j][i], tx

            self.point(int(x),int(y), white)
            d += 1

    
    
    def draw_sprite(self, sprite):
        sprite_a = atan2(sprite["y"] - self.player["y"], sprite["x"] - self.player["x"])

        sprite_d = ((self.player["x"] - sprite["x"])**2 + (self.player["y"] - sprite["y"])**2)**0.5
        sprite_size = (500/sprite_d) * 75

        sprite_x = 500 + (sprite_a - self.player["a"]) * 500/self.player["fov"] + 250 - sprite_size/2
        sprite_y = 250 - sprite_size/2

        sprite_x = int(sprite_x)
        sprite_y = int(sprite_y)
        sprite_size = int(sprite_size)

        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                if 500 < x < 1000 and self.zbuffer[x-500] >= sprite_d:
                    tx = int((x-sprite_x) * 128/sprite_size)
                    ty = int((y-sprite_y) * 128/sprite_size)
                    c = sprite["texture"].get_at((tx,ty))
                    #esto sirve para no colorear lo morado de las imagenes
                    #explicado en clase y utilizado para quitar el verde de los enemigos
                    if c!= (109,167,131):
                        self.point(x,y,c)
                        self.zbuffer[x - 500] = sprite_d

    def draw_Hud(self,xi,yi, w = 515, h = 128):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 128/w)
                ty = int((y - yi) * 128/h)
                c = hud.get_at((tx, ty))
                self.point(x,y,c)
    
    def draw_Face(self,xi,yi, w = 128, h = 128):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 128/w)
                ty = int((y - yi) * 128/h)
                c = face.get_at((tx, ty))
                if c != (0,0,0):
                    self.point(x,y,c)

    def numbers_Mason(self,number,xi,yi, w = 28, h = 28):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 128/w)
                ty = int((y - yi) * 128/h)
                c = number.get_at((tx, ty))
                self.point(x,y,c)

    def draw_player(self, xi, yi, w = 128, h = 128):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 128/w)
                ty = int((y - yi) * 128/h)
                c = hand.get_at((tx, ty))
                if c != (237,28,36):
                    self.point(x,y,c)
                #esto sirve para no colorear lo morado de las imagenes
                #explicado en clase
                #if c != (152, 0, 136, 255):
                


    def render(self):
        #map, still pending for minimap
        for x in range(0, 500, self.blocksize):
            for y in range(0, 500, self.blocksize):
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)
                if self.map[j][i] != ' ' :
                    self.draw_rectangle(x, y, textures[self.map[j][i]])

        self.point(self.player["x"], self.player["y"], white)

        for i in range(0,500):
            a = self.player["a"] - self.player["fov"]/2 + i * self.player["fov"]/500
            d, c, tx = self.cast_ray(a)
            x = 500 + i
            h = 500/(d* cos(a- self.player["a"])) * 50
            self.draw_stake(x, h, textures[c], tx)
            self.zbuffer[i] = d
        
        for enemy in enemies:
            self.point(enemy["x"], enemy["y"],black)
            self.draw_sprite(enemy)
        
        self.draw_player(815, 250)
        self.draw_Hud(500,380)
        self.draw_Face(880,376)
        self.numbers_Mason(zero,640,462)
        self.numbers_Mason(two,610,462)
        self.numbers_Mason(three,580,462)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def main_menu():
    #Sacado de https://pythonprogramming.net/pygame-start-menu-tutorial/
    menu_background = pygame.image.load('./sprites/megaman_logo.png')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.4)
    start = False
    while start == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = True
        screen.fill(random_color)
        screen.blit(menu_background, (425,75))
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects("Press Enter to start!", largeText) 
        TextRect.center = (500,250)        
        screen.blit(TextSurf,TextRect)
        TextSurf2, TextRect2 = text_objects("Shoot with Z. Move with Arrow keys!", largeText) 
        TextRect2.center = (500,350)        
        screen.blit(TextSurf2,TextRect2)
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(15)

def win_screen():
    win_background = pygame.image.load('./sprites/endingbg.jpg')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.4)
    start = False
    while start == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = True
        screen.fill(random_color)
        screen.blit(win_background, (0,0))
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects("Game on!", largeText)
        TextRect.center = (500,250)
        screen.blit(TextSurf,TextRect)
        pygame.display.update()
        clock = pygame.time.Clock()
        clock.tick(15)

def show_fps(clock,screen):
        string = "FPS: " + str(int(clock.get_fps()))
        font = pygame.font.SysFont('Arial', 20, True)
        fps = font.render(string,0,white)
        screen.blit(fps, (950,5))

pygame.init()
#music
pygame.mixer.init()
screen = pygame.display.set_mode((1000, 500))
raymap = Raycaster(screen)
raymap.load_map('map.txt')
#camera shaking when moving
camera_movement = 0
#first music load in the menu
pygame.mixer.music.load('./music_sound_effects/title.mp3')
#Menu with intro
main_menu()
#second music load in the ingame
pygame.mixer.music.load('./music_sound_effects/theme.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)

#megaman X without the clasic shot isn't megaman X
shoot_sound = pygame.mixer.Sound('./music_sound_effects/MMX01.wav')
#charging_sound = pygame.mixer.Sound('./music_sound_effects/MMX02.wav')
#loopcharging_sound = pygame.mixer.Sound('./music_sound_effects/MMX02A.wav')
#charge_shot = pygame.mixer.Sound('./music_sound_effects/MMX03.wav')
# Loop para que continue el juego
while True:
    #cantidad de pixeles por movimiento
    d = 10
    #camara 
    camera_movement += 5
    screen.fill(black)

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            exit(0)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                raymap.player["a"] -= pi/20
            if e.key == pygame.K_RIGHT:
                raymap.player["a"] += pi/20

            if e.key == pygame.K_UP:
                raymap.player["x"] += int(d * cos(raymap.player["a"]))
                raymap.player["y"] += int(d * sin(raymap.player["a"]))
                #camera movememt when moving.
                raymap.player["j"] = int( cos(camera_movement) * 10)
                
            if e.key == pygame.K_DOWN:
                raymap.player["x"] -= int(d * cos(raymap.player["a"]))
                raymap.player["y"] -= int(d * sin(raymap.player["a"]))
                #camera movement backwards
                raymap.player["j"] = int( cos(camera_movement) * 10)

            if e.key == pygame.K_z:
                shoot_sound.play()
        




    #evento cuando se acerca al tile de la x
    if(335<raymap.player["x"]<400 and 399<raymap.player["y"]<427):
        break
    raymap.render()
    show_fps(CLOCK,screen)
    pygame.display.flip()
    CLOCK.tick(60)
#win screen with ending theme
pygame.mixer.music.load('./music_sound_effects/ending.mp3')
win_screen()