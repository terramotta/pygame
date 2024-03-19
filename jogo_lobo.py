# 1 - Import packages
from sys import exit
import pygame
from random import randint, choice


# 2 - Define constants
BLACK = (0, 0, 0)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
FRAMES_PER_SECOND = 60


# 3 - Define classes - check
class Player(pygame.sprite.Sprite):     # sprite significa que é um objeto que pode ser desenhado na tela
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0

        self.image = self.player_walk[self.player_index]            # Inicialização é com o player andando
        self.rect  = self.image.get_rect(midbottom=(80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")     # self.jump_sound é uma classe do pygame.mixer.Sound
        self.jump_sound.set_volume(0.2)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        mouse_buttons =  pygame.mouse.get_pressed()
        if (keys[pygame.K_SPACE] or mouse_buttons[0]) and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
        elif mouse_buttons[0] and self.is_clicked(pygame.mouse.get_pos()) and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
        
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:              # se o player está acima do chão
            self.image = self.player_jump
        else:
            self.player_index += 0.1            # aumenta o index gradativamente
            if self.player_index >= len(self.player_walk): self.player_index = 0        # se index for maior que 1, retorna index para 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()         # Faz uma ação no player, se pygame.key.get_pressed() tiver algum valor de tecla.
        self.apply_gravity()        # Atualiza a posição vertical do player
        self.animation_state()      # Atualiza a animação do player

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210

        elif type == 'snail':
            snail1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail1, snail2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))          # varia a frequencia que veremos spawn de obstaculos, pois na inicialização uns nascem perto e outros longe
        
    def animation_state(self):
        self.animation_index += 0.1 
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def check_and_destroy(self):
        if self.rect.x <= -100:
            self.kill()         # kill() é um método do pygame.sprite.Sprite que remove o objeto da tela

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.check_and_destroy()


# 4 - Create functions
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time     
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: 
        return True


# 5 - Initialize the world
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Jogo do Lobo")
clock = pygame.time.Clock()

test_font = pygame.font.Font("font/pixeltype.ttf", size=60)
# score_surf = test_font.render("JOGO DO LOBO", False, "#000000")
# score_rect = score_surf.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/6))


# 6 - Initialize variables
# mouse_pos = pygame.mouse.get_pos()
game_active = False
start_time = 0
score = 0

obstacle_timer = pygame.USEREVENT + 1       # Timer 
pygame.time.set_timer(obstacle_timer,1500)  # Timer 


# 7 - Create sprite groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


# 8 - Load assets: images, sounds, etc.
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

bg_music = pygame.mixer.Sound('audio/music.mp3')
bg_music.play(loops=-1)     # loops=-1 faz com que a música toque infinitamente
bg_music.set_volume(0.3)    # range vai de 0 a 1

# 9 - Intro screen
player_stand_surface = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand_surface = pygame.transform.rotozoom(player_stand_surface, 0, 2)
player_stand_rect    = player_stand_surface.get_rect(center = (400, 200))

game_name = test_font.render('Jogo do Lobo', False, (111,196,169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Pressione a tecla SPACEBAR para pular', False, (111,196,169))
game_message_rect = game_message.get_rect(center=(400, 330))


# 10 - Create instances of sprites


# 11 - Loop forever, here we will draw all our elements and update everything
while True:
    # 12 - Check for and handle events
# -------------------------------------------------------------------------------------------- #
#                              TODOS OS EVENTOS DO JOGO
# -------------------------------------------------------------------------------------------- #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       # Se clicar no X da janela, fecha o jogo
            pygame.quit()
            exit()

        # -------------------------------------------------------------------------------------------- #
        #                         EVENTOS SE O JOGO ESTIVER ATIVO
        # -------------------------------------------------------------------------------------------- #
        if game_active == 1:     # Se o jogo estiver ativo, faça:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))      # Adiciona um obstaculo a cada 1.5 segundos

        # -------------------------------------------------------------------------------------------- #
        #                         EVENTOS SE O JOGO NÃO ESTIVER ATIVO
        # -------------------------------------------------------------------------------------------- #
        if game_active == 0:               # Se o jogo não estiver ativo, faça:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)            # Inicia o tempo do jogo


        if event.type == pygame.MOUSEBUTTONDOWN:
            print(f"Mouse pressed at {event.pos}")

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)                     # .draw() é um método do pygame.sprite.GroupSingle que desenha o player na tela
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()        # Se houver colisão, collision_sprite() retorna False e game_active = False

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand_surface, player_stand_rect)

        score_message = test_font.render(f"Your score: {score}", False, (111,196,169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)

    # if event.type == pygame.KEYDOWN:
    #     print(f"Key pressed: {event.key}")
    #     if event.key == 32 and (player_rect.bottom == ground_rect.top):
    #         print("Jump 1!")
    #         player_gravity = -20
    #         jump1 = True
    #     if jump1 and event.key == 32 and (player_rect.bottom < ground_rect.top):
    #         print("Jump 2!")
    #         player_gravity = -10
    #         jump1 = False
        
    # 13 - Do any "per frame" actions
    pygame.display.update()     # or pygame.display.flip() 

    # 14 - Clear the window
    #screen.fill(BLACK)

    # 17 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)

# pylint: disable-all


