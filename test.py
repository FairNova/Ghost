import pygame
import time
import random
import json

pygame.init()



class Ghost:
    def __init__(self):
        #ghost start position
        self.x1 = 640/4
        self.y1 = 480/2

class Branch:
    def __init__(self):
        #treee branch position
        self.x1 = 300
        self.y1 = 200
        self.mirror = False
        self.size = 1.0
        self.counted = False # ветка посчитанная что б указать какой счет

def mirror_Coords(ghost):
    if(ghost.y1<0):
        ghost.y1 = 480
    if(ghost.y1>480):
        ghost.y1 = 0


def drawScore(score):
    value = font_style.render("Your Score: " + str(score), True, (0,0,0)) #вывод счета в углу екрана, булевое значение для сглаженого текста
    window.blit(value, [0, 0])


def DrawStartScreen():
    window.fill((20, 128, 128))# background
    mes = font_style.render("Press R to Start", True, (255,0,0)) #последние это задание цвета
    window.blit(mes, [640/3, 480/2])
    pygame.display.update()
    startGame = False
    while startGame==False:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    startGame=True
            if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    quit()


def YouDied(score):
    window.fill((0, 0, 0))# background
    #сообщение о результате
    mes = font_style.render("YOU DIED. Score: "+ str(score) +" | " + "Press Q for restart", True, (255,0,0)) #последние это задание цвета
    window.blit(mes, [640/3, 480/2])
    #считать результат
    bestScore = ReadBestScore()
    #сообщение о лучших результатах
    mes2 = font_style.render("Best Score: ", True, (255,0,255)) 
    window.blit(mes2, [640/3, 520/2])
    for x in range(5):
        score_res = font_style.render(bestScore[x]['name'] + " " + str(bestScore[x]['score']), True, (255,255,0)) #последние это задание цвета
        window.blit(score_res, [640/3, 560/2+20*x])
    pygame.display.update()

def updateScreen(ghost, score):
    window.fill((20, 128, 128))# background
    window.blit(textures['background'], (0, 0))  # нанесение второго слоя
    drawScore(score)
    window.blit(textures['player'], (ghost.x1, ghost.y1))
    for branch in branches:
        if(branch.mirror):
            window.blit(pygame.transform.scale(pygame.transform.flip(textures['tree'], False, True),(60, int(150*branch.size))), (branch.x1,branch.y1))
            #window.blit(textures['tree'], (branch.x1,branch.y1))
        else:
            window.blit(pygame.transform.scale(textures['tree'],(60, int(150*branch.size))), (branch.x1,branch.y1))#??
    pygame.display.update()


def BranchLocomotion():
    for branch in branches:
        branch.x1 -= 3*difficulty
        if(branch.x1<0):
            branch.x1 = 640
            branch.size = random.uniform(0.9, 1.4)
            branch.counted = False

def CheckCollision(ghost):
    ghostRect = pygame.Rect(ghost.x1, ghost.y1, 50, 50) # создаем квадраты у игрока и веток для проверки коллизии
    for branch in branches:
        branchRect = pygame.Rect(branch.x1, branch.y1, 60, int(150*branch.size))
        if ghostRect.colliderect(branchRect): # проверка столкновеий
            return True

def initialization():
    global window
    global clock
    global font_style
    global textures
    global g_force
    global branches
    window = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Flappy ghost 1.0')
    clock = pygame.time.Clock()
    font_style = pygame.font.SysFont("arial.ttf", 25)
    textures = {} #словарь ( обращение к елементу по имени а не числу)
    g_force = 3 * difficulty
    branches = [] #список (обращение к числу)
    pygame.mixer.music.load("music/music.mid")
    pygame.mixer.music.play()

def AddScore(ghost):
    for branch in branches:
        if(branch.x1 < ghost.x1 and branch.counted == False):
            branch.counted = True
            return 1
    return 0

def SaveScore(score):
    #запись лучшего результата
    answer = "r"
    while answer!= "y" and answer!="n":
        answer = input("Save score(y/n): ")
    if(answer == "y"):
        name = input("Insert name: ")
        name_nw = name.replace(" ", "")  # удалить пробелы
        score_data = {
            "name": name_nw,
            "score": score
        }
        with open("score.json",'r+') as file:
            file_data = json.load(file)
            file_data["High_Score"].append(score_data) 
            file.seek(0)
            json.dump(file_data, file , indent = 4)
    
   # for x in range(5):
    #    print(test[x]['name'] + " " + str(test[x]['score']))

def ReadBestScore():
    # считываем из файла json резултаты в порядке от лучшего к худшему

    with open("score.json", 'r', encoding='utf-8') as file:
        score = json.load(file)
    
    data =  sorted(score['High_Score'], key=lambda d: d['score'], reverse=True) 

    return data

def main():
    game_over = False

    score = 0

    #spawn ghost
    player = Ghost()

    i = 0
    for branch in range(4):
        branch = Branch()
        branch.x1 = i * 200 +1
        if(i % 2 == 0):
            branch.mirror = True
            branch.y1 = 340
        else:
            branch.y1 = 0
        i+=1
        branches.append(branch)

    y_vector = 0
    impulse = 0

    tree_image = 'images/tree_branch.png'
    background_image = 'images/background.jpg'
    player_image = 'images/ghost.png'

    textures['player'] = pygame.image.load(player_image).convert_alpha()

    textures['background'] = pygame.image.load(background_image).convert_alpha()
    textures['background'] = pygame.transform.scale(textures['background'], (640, 480))

    textures['tree'] = pygame.image.load(tree_image).convert_alpha()
    textures['tree'] = pygame.transform.scale(textures['tree'], (60, 150))

    while True:

        if game_over == True:
            branches.clear()
            YouDied(score)
            exitB = False
            while exitB==False:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            exitB=True
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    SaveScore(score)
                    quit()
            pygame.event.clear()
            main()

        #controll keys check
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    impulse = -15*difficulty
            # exit game with window control
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                SaveScore(score)
                quit()

        updateScreen(player, score)

        if(CheckCollision(player)):
            game_over = True

        y_vector = impulse + g_force

        if(impulse < 0):
            impulse = impulse + g_force
        else:
            impulse = 0

        player.y1 += y_vector

        mirror_Coords(player) # отзеркаливание координат при выходе за экран

        BranchLocomotion() # движение веток
        score += AddScore(player) #

        clock.tick(30)



global difficulty

difficulty = 0

while difficulty!=1 and difficulty!=2 and difficulty!=3: 
    difficulty = int(input("Select level 1-3: "))

initialization()
DrawStartScreen()
main()
