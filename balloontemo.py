import cv2
import mediapipe as mp
import pygame
import time
import random
import math
import sys

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

pygame.init()
#
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set font
font = pygame.font.Font(None, 36)

# Instruction slides content
slides = [
    {"text": "Welcome to the Game! I am Aditya Agarwal, your instructor.", "image": "first.png"},
    {"text": "Your job is to perform some poses seeing image on screen.", "image": "second.png"},
    {"text": "The more you score, the more this bucket fills.", "image": "fill3.png"},
    {"text": "Do this before the car gets in the hole.", "image": "car.png"},
    {"text": "You need to perform 10 reps of each pose to get 1 point.", "image": "third.png"},
    {"text": "Press any key to start the game!", "image": "forth.png"}
]
def draw_text(text, font, surface, x, y):
    text = str(text)
    textobj = font.render(text, True, (255, 255, 255))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def show_instructions():
    slide_index = 0
    while slide_index < len(slides):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                slide_index += 1
        
        screen.fill((0, 0, 0))
        if(slide_index==6):
            break
        slide = slides[slide_index]
        image = pygame.image.load(slide["image"])
        image = pygame.transform.scale(image, (750,500)) 
        image_rect = image.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(image, image_rect)
  
        draw_text(slide["text"], font, screen, 20, 20)
        
        pygame.display.flip()
        pygame.time.wait(500)
show_instructions()


car_img = pygame.image.load("car.png")
car_img = pygame.transform.scale(car_img, (80,90)) 

bomb_img = pygame.image.load("hole.png")
bomb_img = pygame.transform.scale(bomb_img, (100,100))

bg_img = pygame.image.load("bg.png")
bg_img = pygame.transform.scale(bg_img, (800, 400))
#
width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Exercise Game")
img1 = pygame.image.load('1.jpg')
img1 = pygame.transform.scale(img1, (250, 250))
img2 = pygame.image.load('2.jpg')
img2 = pygame.transform.scale(img2, (250, 250))
img3 = pygame.image.load('3.jpg')
img3 = pygame.transform.scale(img3, (250, 250))
img4 = pygame.image.load('4.jpg')
img4 = pygame.transform.scale(img4, (250, 250))
img5 = pygame.image.load('5.jpg')
img5 = pygame.transform.scale(img5, (250, 250))

info = pygame.image.load('info.png')
info = pygame.transform.scale(info, (400, 200))

imgf0 = pygame.image.load('fill0.png')
imgf0 = pygame.transform.scale(imgf0, (200, 200))
imgf1 = pygame.image.load('fill1.png')
imgf1 = pygame.transform.scale(imgf1, (200, 200))
imgf2 = pygame.image.load('fill2.png')
imgf2 = pygame.transform.scale(imgf2, (200, 200))
imgf3 = pygame.image.load('fill3.png')
imgf3 = pygame.transform.scale(imgf3, (200, 200))
imgf4 = pygame.image.load('fill4.png')
imgf4 = pygame.transform.scale(imgf4, (200, 200))
imgf5 = pygame.image.load('fill5.png')
imgf5 = pygame.transform.scale(imgf5, (200, 200))
imgf6 = pygame.image.load('fill6.png')
imgf6 = pygame.transform.scale(imgf6, (200, 200))
imgf7 = pygame.image.load('fill7.png')
imgf7 = pygame.transform.scale(imgf7, (200, 200))
imgf8 = pygame.image.load('fill8.png')
imgf8 = pygame.transform.scale(imgf8, (200, 200))
imgf9 = pygame.image.load('fill9.png')
imgf9 = pygame.transform.scale(imgf9, (200, 200))
imgf10 = pygame.image.load('fill10.png')
imgf10= pygame.transform.scale(imgf10, (200, 200))
imgf11 = pygame.image.load('fill11.png')
imgf11= pygame.transform.scale(imgf11,(200, 200))
x,y=50,100

LIGHT_BLUE = (173, 216, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Box:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.size = self.img.get_size()

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        # Ensure the box stays within the screen bounds
        if self.x < 0:
            self.x = 0
        if self.x + self.size[0] > width:
            self.x = width - self.size[0]


def detect_hand_squeezes(multi_hand_landmarks):
    for hand_landmarks in multi_hand_landmarks:
       
        if hand_landmarks:
          
            finger_tips = [mp_hands.HandLandmark.THUMB_TIP, 
                           mp_hands.HandLandmark.INDEX_FINGER_TIP, 
                           mp_hands.HandLandmark.MIDDLE_FINGER_TIP, 
                           mp_hands.HandLandmark.RING_FINGER_TIP, 
                           mp_hands.HandLandmark.PINKY_TIP]
            
            squeeze_detected = True
            for tip in finger_tips:
               
                if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[tip - 2].y:
                    squeeze_detected = False
                    break
            
            if squeeze_detected:
                return True  
    
    return False  

def calculate_distance(lm1, lm2):
   
    return ((lm1.x - lm2.x)**2 + (lm1.y - lm2.y)**2)**0.5

def detect_wrist_circles(previous_landmarks, current_landmarks):
    if previous_landmarks is None:
        return False
    
    wrist_current = current_landmarks.landmark[0]
    wrist_previous = previous_landmarks.landmark[0]

   
    dx = wrist_current.x - wrist_previous.x
    dy = wrist_current.y - wrist_previous.y

   
    distance = math.hypot(dx, dy)
    curvature = math.atan2(dy, dx)

 
    min_distance = 0.05
    max_curvature = math.pi / 2  

    

    return distance > min_distance and abs(curvature) > max_curvature

def detect_hand_glides(previous_landmarks, current_landmarks):
    
    if previous_landmarks is None:
        return False
    
   
    palm_current = current_landmarks.landmark[0]
    palm_previous = previous_landmarks.landmark[0]

   
    dx = abs(palm_current.x - palm_previous.x)
    dy = abs(palm_current.y - palm_previous.y)

   
    min_movement = 0.05

  
    return dx > min_movement or dy > min_movement

def detect_finger_opposition(hand_landmarks):
  
    if len(hand_landmarks) != 1:
        return False
    
 
    thumb_tip = hand_landmarks[0].landmark[4]
    finger_tips = [8, 12, 16, 20]

   
    min_distance = 0.05

   
    for tip in finger_tips:
        finger_tip = hand_landmarks[0].landmark[tip]
        distance = math.hypot(thumb_tip.x - finger_tip.x, thumb_tip.y - finger_tip.y)
        if distance < min_distance:
            return True 

    return False  

def detect_atlas_exercise(hand_landmarks):
    if len(hand_landmarks) != 1:
        return False
    
    finger_bases = [5, 9, 13, 17]
    palm_center = hand_landmarks[0].landmark[0]

    for base in finger_bases:
        if hand_landmarks[0].landmark[base].x < palm_center.x:
            return False 

    return True  

scores=pygame.mixer.Sound("pass.mp3")
constbgm=pygame.mixer.Sound("Sakura_girl_bgm.mp3")
red_box = Box(0, height // 2, car_img)
black_box = Box(width - 100, height // 2, bomb_img)
winnn=pygame.mixer.Sound("win.mp3")

running = True
cap = cv2.VideoCapture(0)
clock = pygame.time.Clock()
last_move_time = time.time()
previous_landmarks = None
score = 0 


move_speed = 5  
retreat_speed = 0
reward_distance = 20  

exercise_list = [
    ("Hand Squeezes", detect_hand_squeezes),
    ("Wrist Circles", detect_wrist_circles),
    ("Hand Glides", detect_hand_glides),
    ("Finger Opposition", detect_finger_opposition),
    ("Atlas Exercise", detect_atlas_exercise)
]
current_exercise = None
exercise_start_time = None
exercise_detected = False  
img=img1
number_of_rep=10
rep=0
cooldown_period = 1.0
last_detection_time = 0
pygame.mixer.Sound.play(constbgm)
while running:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if current_exercise is None or (time.time() - exercise_start_time > 20):
        current_exercise, exercise_func = random.choice(exercise_list)
        rep=0
        exercise_start_time = time.time()
        exercise_detected = False 
        print(f"Perform {current_exercise}!")
        red_box.move(reward_distance, 0)
        if(current_exercise=="Hand Squeezes"):
            img=img1
        if(current_exercise=="Wrist Circles"):
            img=img2
        if(current_exercise=="Finger Opposition"):
            img=img3
        if(current_exercise=="Hand Glides"):
            img=img4
        if(current_exercise=="Atlas Exercise"):
            img=img5

        pygame.display.update()

    flag=True
    current_time = time.time()
    
    if current_exercise and not exercise_detected:
       
        detected = False
        if results.multi_hand_landmarks:
            if current_exercise == "Hand Squeezes":
                detected = exercise_func(results.multi_hand_landmarks)
                img=img1
            elif current_exercise == "Wrist Circles":
                if previous_landmarks:
                    detected = exercise_func(previous_landmarks, results.multi_hand_landmarks[0])
                img=img2
            elif current_exercise == "Hand Glides":
                if previous_landmarks:
                    detected = exercise_func(previous_landmarks, results.multi_hand_landmarks[0])
                img=img3
            elif current_exercise == "Finger Opposition":
                if len(results.multi_hand_landmarks) == 1:
                    detected = exercise_func(results.multi_hand_landmarks)
                img=img4
            elif current_exercise == "Atlas Exercise":
                if len(results.multi_hand_landmarks) == 1:
                    detected = exercise_func(results.multi_hand_landmarks)
                img=img5
        if detected and (current_time - last_detection_time >= cooldown_period):  
            rep+=1
            last_detection_time = current_time
            red_box.move(retreat_speed, 0)
            if(rep==10):
                score += 1
                exercise_detected = True
                rep=0
                pygame.mixer.Sound.play(scores)
            

    if red_box.x + red_box.img.get_width() >= black_box.x:
        running = False
        print("Game Over!")
    
    win.fill(WHITE)
    win.blit(bg_img,(0,0))
    win.blit(img,(500,10))
    win.blit(info,(0,400))
    red_box.draw(win)
    black_box.draw(win)

    if current_exercise:
        font = pygame.font.Font(None, 36)
        exercise_text = font.render(f"Perform {current_exercise}!", True, BLACK)
        win.blit(exercise_text, (10, 10))

        time_left = max(0, 20 - (time.time() - exercise_start_time))
        timer_text = font.render(f"Time left: {time_left:.1f}", True, BLACK)
        win.blit(timer_text, (10, 40))
    
    score_text = font.render(f"Your Score: {score}", True, BLACK)
    win.blit(score_text, (10,80))
    rep_text = font.render(f"No. of repetition: {rep}", True, BLACK)
    win.blit(rep_text, (10,120))
    if(score==0):
        win.blit(imgf0,(550,400))
    elif(score==1):
        win.blit(imgf1,(550,400))
    elif(score==2):
        win.blit(imgf2,(550,400))
    elif(score==3):
        win.blit(imgf3,(550,400))
    elif(score==4):
        win.blit(imgf4,(550,400))
    elif(score==5):
        win.blit(imgf5,(550,400))
    elif(score==6):
        win.blit(imgf6,(550,400))
    elif(score==7):
        win.blit(imgf7,(550,400))
    elif(score==8):
        win.blit(imgf8,(550,400))
    elif(score==9):
        win.blit(imgf9,(550,400))
    elif(score==10):
        win.blit(imgf10,(550,400))
    elif(score==11):
        win.blit(imgf11,(550,400))
    else:
        print("you win")
        win.fill(WHITE)
        congrats_text = font.render("Congratulations, you won!", True, BLACK)
        pygame.mixer.Sound.play(winnn)
        win.blit(congrats_text, (width // 2 - 200, height // 2 - 20))
        pygame.display.update()
        time.sleep(5)
        running = False
    pygame.display.update()
    cv2.imshow('MediaPipe Hands', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

    if results.multi_hand_landmarks:
        previous_landmarks = results.multi_hand_landmarks[0]
    else:
        previous_landmarks = None
cap.release()
cv2.destroyAllWindows()
pygame.quit()
     
