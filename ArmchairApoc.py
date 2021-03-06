import pygame
import os
from os import path
import random
import operator
from datetime import datetime
import atexit

logFolder=path.join(os.path.dirname(__file__),"logs.txt")
logFile=open(logFolder,("a+"))
def save():
	try:
		temp=score
	except NameError:
		score=None
		
	logFile.write(Name)
	logFile.write(" " + str(datetime.now()))
	logFile.write("\n")
	
	print("End Score: ",score)
	for i in log:
		logFile.write(i)
		logFile.write("\n")
	logFile.write(str(score))
	logFile.write("\n")
	if insanity_mode:
		logFile.write("Insanity")
		logFile.write("\n")
	logFile.write("\n")
	logFile.close()
atexit.register(save)

scores={}
highscore=open(path.join(os.path.dirname(__file__),'highscores.txt'),('r'))
highscore=highscore.read()
highscore=highscore.split("\n")
try:
	highscore.remove("")
except ValueError:
	pass
print("High Score List:\n-----------")
for i in reversed(highscore):
	print(i)
print("-----------")
highscores=highscore

for i in highscores:
	highscores[highscores.index(i)]=i.split(":")
for i in highscores:
	scores[i[0]]=int(i[1])

spritesPath=path.join(os.path.dirname(__file__),'sprites')
def get_image(name):
	temp=path.join(spritesPath,name)
	if name != "background.png":
		image = pygame.image.load(temp).convert_alpha()
	else:
		image = pygame.image.load(temp)
	return image		
	
def borderCheck(input,max):
	if input > max: input=0
	elif input < 0: input=max
	return(input)

class Drop():
	def __init__(self,x,y,type):
		self.time=0
		self.lifespan=300
		self.x=x
		self.y=y
		self.type=type
	def update(self):
		self.blit=screen.blit(self.type,(self.x,self.y))
		self.time+=1
	
class Player():
	def __init__(self):
		self.speed=3
		self.health=3
		self.x=round(screen_x/2)
		self.y=round(screen_y/2)
		self.direction = main_up
	def move(self,direction):
		self.direction=direction
		if direction == main_up: self.y-=self.speed
		elif direction == main_down: self.y+=self.speed
		elif direction == main_left: self.x-=self.speed
		elif direction == main_right: self.x+=self.speed
	def update(self):
		self.blit=screen.blit(self.direction,(self.x,self.y))
		for i in range(self.health):
			screen.blit(heart,(i*int(heart.get_width())+175,15))
			
class Enemy():
	def __init__(self):
		self.start=True
		self.x=0
		self.y=0
		while (self.x == int(round(screen_x/2)) and self.y == int(round(screen_y/2))) or self.start == True:
			self.start=False
			self.x=random.choice([0,screen_x,int(round(screen_x/2))])
			self.y=random.choice([0,screen_y,int(round(screen_y/2))])
		self.phase=0
		self.counter=0
		self.speed=1
		self.timer=0
	def chase(self):
		self.goalx=player.x
		self.goaly=player.y
		if player.x > screen_x - 100 and self.x < round(screen_x/2) :
			self.goalx=-10
		if player.y > screen_y - 100 and self.y < round(screen_y/2):
			self.goaly=-10
		if player.x < 100 and self.x > round(screen_x/2):
			self.goalx=screen_x+10
		if player.y < 100 and self.y > round(screen_y/2):
			self.goaly=screen_y+10
		if self.x < self.goalx:
			self.x+=self.speed
		if self.x > self.goalx:
			self.x-=self.speed
		if self.y < self.goaly:
			self.y+=self.speed
		if self.y > self.goaly:
			self.y-=self.speed
		self.x=borderCheck(self.x,screen_x)
		self.y=borderCheck(self.y,screen_y)
	def phaseChange(self):
		self.counter+=1
		if self.counter > 20:
			self.counter=0
			self.phase+=1
			if self.phase > len(enemy_states)-1:
				self.phase=0
	def update(self):
		self.blit=screen.blit(enemy_states[self.phase],(self.x,self.y))
		if insanity_mode:
			self.timer+=1
			if self.timer > 600:
				self.speed=2
	def refresh(self):
		self.chase()
		self.phaseChange()
		self.update()

class Sniper():
	def __init__(self):
		self.speed=2
		self.x=random.randint(0,screen_x)
		self.y=random.randint(0,screen_y)
		self.counter=0
		self.choice=random.choice(["+","-"])
		self.phase=0
		
		self.direction=random.choice(["l","r","u","d"])
		self.opacity=0
		self.beam_time=0
		if self.direction == "l" or self.direction == "r":
			self.beam_surface=pygame.Surface((750,25))
		else:
			self.beam_surface=pygame.Surface((25,750))

	def dodge(self,fireball):
		if (fireball.image == fire_left and fireball.x - 300 < self.x) and (fireball.y < (self.y + sniper_0.get_height() + 20) and fireball.y > (self.y - 20)):
			if self.choice == "+":
				self.y+=self.speed	
			else:
				self.y-=self.speed
		elif (fireball.image == fire_right and fireball.x + 300 > self.x) and (fireball.y < (self.y + sniper_0.get_height() + 20) and fireball.y > (self.y - 20)):
			if self.choice == "+":
				self.y+=self.speed
			else:
				self.y-=self.speed
		elif (fireball.image == fire_up and fireball.y + 300 > self.y) and (fireball.x < (self.x + sniper_0.get_width() + 20) and fireball.x > (self.x - 20)):
			if self.choice == "+":
				self.x+=self.speed
			else:
				self.x-=self.speed
		elif (fireball.image == fire_down and fireball.y - 300 < self.y) and (fireball.x < (self.x + sniper_0.get_width() + 20) and fireball.x > (self.x - 20)):
			if self.choice == "+":
				self.x+=self.speed
			else:
				self.x-=self.speed
	def shoot(self):
		
		self.beam_surface.set_alpha(int(self.opacity*4))
		if int(self.opacity) == 48:
			self.beam_surface.fill((255,0,0))
			self.beam_time+=1
			self.dangerous=True
		else:
			self.beam_surface.fill((self.opacity*5+1,0,0))
			self.opacity+=1
			self.dangerous=False
		if self.beam_time == 60:
			self.opacity=0
			self.beam_time=0
			
		
		if self.direction == "l":
			self.beam=screen.blit(self.beam_surface,(self.x-760,self.y))
		elif self.direction == "r":
			self.beam=screen.blit(self.beam_surface,(self.x+10,self.y))
		elif self.direction == "u":
			self.beam=screen.blit(self.beam_surface,(self.x,self.y+10))
		else:
			self.beam=screen.blit(self.beam_surface,(self.x,self.y-760))
	
	def update(self):
		self.blit=screen.blit(sniper_states[self.phase],(self.x,self.y))
	def phaseChange(self):
		self.counter+=1
		if self.counter > 20:
			self.counter=0
			self.phase+=1
			if self.phase > (len(sniper_states)-1):
				self.phase=0
	def refresh(self):
		self.phaseChange()
		self.update()
		self.shoot()

class PacMan():
	def __init__(self):
		self.x=100
		self.y=100
		self.health=2
		self.direction=pac_right
		self.injured=False
		self.image=pac_right
		self.speed=4
		self.state=0
	def move(self):
		if self.direction == pac_right:
			if self.x > screen_x-100:
				self.direction=pac_down
			else:
				self.x+=self.speed
		if self.direction == pac_left:
			if self.x < 100:
				self.direction = pac_up
			else:
				self.x-=self.speed
		if self.direction == pac_down:
			if self.y > screen_y-100:
				self.direction=pac_left
			else:
				self.y+=self.speed
		if self.direction == pac_up:
			if self.y < 100:
				self.direction=pac_right
			else:
				self.y-=self.speed	
	def update(self):
		self.move()
		if self.state > 30:
			if self.state == 60:
				self.state=0
			if self.injured:
				self.blit=screen.blit(self.direction[3],(self.x,self.y))
			else:
				self.blit=screen.blit(self.direction[1],(self.x,self.y))
		elif self.injured:
			self.blit=screen.blit(self.direction[2],(self.x,self.y))
		else:
			self.blit=screen.blit(self.direction[0],(self.x,self.y))
		self.state+=1

class Fireball():
	def __init__(self):
		self.x=player.x
		self.y=player.y
		self.start_x=self.x
		self.start_y=self.y
		self.speed=5
		if player.direction == main_up:
			self.image=fire_up
			self.y-=50
		elif player.direction == main_down:
			self.image=fire_down
			self.y+=50
		elif player.direction == main_left:
			self.image=fire_left
			self.x-=50
		elif player.direction == main_right:
			self.image=fire_right
			self.x+=50
	def update(self):
		self.blit=screen.blit(self.image,(self.x,self.y))
	def move(self):
		if self.image == fire_right:
			self.x+=self.speed
		elif self.image == fire_left:
			self.x-=5
		elif self.image == fire_up:
			self.y-=5
		elif self.image == fire_down:
			self.y+=5
	def refresh(self):
		if insanity_mode:
			self.x=borderCheck(self.x,screen_x)
			self.y=borderCheck(self.y,screen_y)
		self.move()
		self.update()

class Wall():
	def __init__(self,x,y,size,direction):
		self.x=x
		self.y=y
		self.size=size
		self.direction=direction
		Walls.append(self)
		self.collisions={"left":False,"right":False,"up":False,"down":False}
	def draw(self):
		if self.direction == "vertical":
			self.rect=pygame.draw.rect(screen,(255,255,255),[self.x,self.y,10,self.size],0)
		elif self.direction == "horizontal":
			self.rect=pygame.draw.rect(screen,(255,255,255),[self.x,self.y,self.size,10],0)
		
screen_x=1366
screen_y=768

Name=""
log=[]
log.append("LOG: Initial launch, name input")
print("\t\tWelcome to\n\t    ArmChair Apocalypse\n\tThe Retro Survival Shooter!\n\nArrow Keys or WASD to Move, Spacebar to Shoot")

while Name == "":
	Name=input("Name? : ")
	game_mode=input("game_mode? (insanity,normal) : ")

if game_mode == "insanity":
	insanity_mode = True
else:
	insanity_mode = False
log.append("LOG: Initializing display and sprites")
pygame.init()
screen = pygame.display.set_mode((screen_x,screen_y))
clock = pygame.time.Clock()	

main_up = get_image("main_0.png")
main_down = get_image("main_1.png")	
main_right = get_image("main_2.png")
main_left = get_image("main_3.png")

fire_right = get_image('fireball_0.png')
fire_left = get_image('fireball_1.png')
fire_down = get_image('fireball_2.png')
fire_up = get_image('fireball_3.png')

heart = get_image('heart_0.png')

exit = [get_image('exit_0.png'),get_image('exit_1.png')]

background = get_image('background.png')
background=pygame.transform.scale(background,(screen_x,screen_y))

invul_background = get_image('background2.png')
invul_background=pygame.transform.scale(invul_background,(screen_x,screen_y))

backgroundBright=get_image('backgroundBright.png')
backgroundBright=pygame.transform.scale(backgroundBright,(screen_x,screen_y))


enemy_states=[get_image('enemy_0.png'),get_image('enemy_1.png'),get_image('enemy_2.png'),get_image('enemy_3.png'),get_image('enemy_4.png'),get_image('enemy_5.png'),get_image('enemy_6.png')]
sniper_states=[get_image('sniper_0.png'),get_image('sniper_1.png'),get_image('sniper_2.png'),get_image('sniper_3.png'),get_image('sniper_4.png'),get_image('sniper_5.png')]
sniper_0=get_image('sniper_0.png')


pac_right=[get_image('pacman_right.png'),get_image('pacman_right_closed.png'),get_image('pacman_right_injured.png'),get_image('pacman_right_closed_injured.png')]
pac_down=[get_image('pacman_down.png'),get_image('pacman_down_closed.png'),get_image('pacman_down_injured.png'),get_image('pacman_down_closed_injured.png')]
pac_left=[get_image('pacman_left.png'),get_image('pacman_left_closed.png'),get_image('pacman_left_injured.png'),get_image('pacman_left_closed_injured.png')]
pac_up=[get_image('pacman_up.png'),get_image('pacman_up_closed.png'),get_image('pacman_up_injured.png'),get_image('pacman_up_closed_injured.png')]


wind=get_image('wind_0.png')


Game_Over_font = pygame.font.SysFont("comicsansms", 72)
Game_Over_text = Game_Over_font.render("Game Over", True, (0, 128, 0))

Score_font = pygame.font.SysFont("arial", 18)

score=0
Enemy_timer=0	
Fireball_timer=0
Invul_timer=0
Drop_timer=0
Sniper_timer=0

invul=False
cooldown=True
cooldown_time=480
cooldown_time_default=cooldown_time
done = False
game_over = False
Enemies=[Enemy()]
Snipers=[]
Fireballs=[]
Drops=[]
	
Walls=[]#,Wall(300,300,300,"horizontal")]
#Wall(screen_x/2+100,screen_y/2+100,100,"vertical")
#Wall(screen_x/2+100,screen_y/2+100,100,"horizontal")



fireball_continue=True
color=(255,255,255)
player=Player()
pac=PacMan()

cooldown_time_length=360
this2=0
noMoveUp=False
noMoveRight=False
noMoveDown=False
noMoveLeft=False

temp2=0
temp3=0

DISPLAYSURF = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)


log.append("LOG: Variables and screen initialized")
print("LOG: Variables and screen initialized")
while not done:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			log.append("LOG: X button clicked to end game")
			print("LOG: X button clicked to end game")
			done = True
		if game_over:
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if exit_button.collidepoint(pygame.mouse.get_pos()):
					done=True
					pygame.quit()
	
	if game_over != True and done != True:
		screen.fill((0,0,0))
		if invul:
			screen.blit(backgroundBright,(0,0))
		else:
			screen.blit(background,(0,0))
		
		pygame.draw.rect(screen,(255,255,255),[0,0,170+25*player.health,40],2)
		
		#######
		#Enemy#
		#######
		
		Fireball_timer+=1
		if Fireball_timer > cooldown_time and cooldown == False:
			cooldown=True
		Enemy_timer+=1
		if score > 15:
			this=45
		else:
			this=round(360/((score+1/2)))
		if Enemy_timer > this and len(Enemies) < 25:
			Enemies.append(Enemy())
			Sniper_timer+=1
			Enemy_timer=0
		if Sniper_timer > 5 and score > 25:
			Snipers.append(Sniper())
			Sniper_timer=0
		for enemy in Enemies:
			enemy.refresh()
		for sniper in Snipers:
			for fireball in Fireballs:
				sniper.dodge(fireball)
			sniper.refresh()
		pac.update()
	##################
	#Character Inputs#
	##################
	
		if cooldown:
			if cooldown_time == cooldown_time_default:
				screen.blit(fire_right,(50,10))
			else:
				screen.blit(fire_up,(50,10))
		else:	
			pygame.draw.rect(screen,(255,0,0),[2,4,round((Fireball_timer/cooldown_time)*75),29],0)
			pygame.draw.rect(screen,(0,255,0),[1,3,75,31],1)

			
		Score_message="Score:" + str(score)
		Score_text = Score_font.render(Score_message, True, (255,255,255))
		screen.blit(Score_text,
        (125 - Score_text.get_width() // 2, 24 - Score_text.get_height() // 2))
		
		pressed = pygame.key.get_pressed()
		if (pressed[pygame.K_UP] or pressed[pygame.K_w]) and (not noMoveUp): 
			player.move(main_up)
		if (pressed[pygame.K_DOWN] or pressed[pygame.K_s]) and (not noMoveDown): 
			player.move(main_down)
		if (pressed[pygame.K_LEFT] or pressed[pygame.K_a]) and (not noMoveLeft): 
			player.move(main_left)
		if (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]) and (not noMoveRight): 
			player.move(main_right)
		player.update()
		if pressed[pygame.K_SPACE] and cooldown == True:
			cooldown=False
			Fireball_timer=0
			Fireballs.append(Fireball())
		for fireball in Fireballs:
			fireball.refresh()
		for drop in Drops:
			
			temp=0
			if drop.time > int(drop.lifespan/2):
				temp+=1
				if temp == 2:
					drop.update()
			else:
				drop.update()
			if drop.time > drop.lifespan:
				del Drops[Drops.index(drop)]
		message=True
		
	#############
	#Environment#
	#############
		for wall in Walls:
			wall.draw()

	elif done == False:
		if message:
			log.append("LOG: Game over, but screen open")
			print("LOG: Game over, but screen open")
			message=False
			
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_ESCAPE]:
			done=True
			log.append("LOG: Escape button pressed to close game")
			print("LOG: Escape button pressed to close game")
		else:
			this+=1
			if this == 15:
				this=0
				this2+=1
			if this2 == len(exit):
				this2=0
			screen.fill((150,150,150))
			screen.blit(Game_Over_text,
			(320 - Game_Over_text.get_width() // 2, 240 - Game_Over_text.get_height() // 2))
			exit_button=screen.blit(exit[this2],(screen_x/2,screen_y/2))
	

	
	
	##############
	#Interactions#
	##############
	
	if invul:
		Invul_timer+=1
		pygame.draw.rect(screen,(255,255,255),[player.x,player.y,25,25],-1)
		
		if Invul_timer > 120:
			Invul_timer=0
			invul=False
	
	for enemy in Enemies:
		if player.blit.colliderect(enemy.blit) == 1 and invul == False:
			invul = True
			player.health-=1
			

	for drop in Drops:
		if player.blit.colliderect(drop.blit) == 1:
			if drop.type == heart:
				log.append("LOG: Heart powerup picked up")
				player.health+=1
			elif drop.type == fire_right:
				log.append("LOG: Fire powerup picked up")
				cooldown_time=60
				cooldown_time_length=360
			elif drop.type == wind:
				log.append("LOG: Wind powerup picked up")
				player.speed=6
				cooldown_time_length=360
			del Drops[Drops.index(drop)]
	
	if cooldown_time == 60 or player.speed == 6:
		cooldown_time_length-=1
		if cooldown_time_length == 0:
			cooldown_time=cooldown_time_default
			player.speed=3
	if insanity_mode != True:
		for fireball in Fireballs:
			if (fireball.x > screen_x or fireball.x < 0) or (fireball.y > screen_y or fireball.y < 0):
				del Fireballs[Fireballs.index(fireball)]
	else:
		for fireball in Fireballs:
			temp=fireball.blit
			if temp.colliderect(player.blit) == 1:
				del Fireballs[Fireballs.index(fireball)]
				player.health-=1
				log.append("LOG: Player hit by fireball")
				if player.health == 0:
					game_over=True
	for enemy in Enemies:
		for fireball in Fireballs:
			temp=fireball.blit
			if temp.colliderect(enemy.blit) == 1:
				del Enemies[Enemies.index(enemy)]
				chance=random.randint(1,25)
				if chance == 10:
					temp=Drop(enemy.x,enemy.y,heart)
					Drops.append(temp)
				if chance == 9:
					temp=Drop(enemy.x,enemy.y,fire_right)
					Drops.append(temp)
				if chance == 8:
					temp=Drop(enemy.x,enemy.y,wind)
					Drops.append(temp)
				score+=1

	for sniper in Snipers:
		if sniper.blit.colliderect(player.blit) == 1:
			del Snipers[Snipers.index(sniper)]
			score+=2
		if (sniper.beam.colliderect(player.blit) == 1 and sniper.dangerous == True) and (invul == False):
			invul = True
			player.health-=1
			log.append("LOG: Player hit by sniper")
			if player.health == 0:
				game_over=True
		for fireball in Fireballs:
			if fireball.blit.colliderect(sniper.blit) == 1:
				del Snipers[Snipers.index(sniper)]
				score+=2
	for fireball in Fireballs:
		if fireball.blit.colliderect(pac.blit) == 1:
			if pac.injured:
				pac.speed-=3
			else:
				pac.injured=True
				pac.speed=round(pac.speed/2)
			if pac.speed < 1:
				pac.speed=1
			if not insanity_mode:
				del Fireballs[Fireballs.index(fireball)]
	
	for enemy in Enemies:
		if enemy.blit.colliderect(pac.blit) == 1:
			if pac.injured:
				pac.injured=False
			elif pac.speed < 8:
				pac.speed+=1
			del Enemies[Enemies.index(enemy)]

	if player.blit.colliderect(pac.blit) == 1 and invul == False:
		player.health-=2
		invul=True
	
	if player.health < 1:
		game_over=True
	
	####################
	#Inactive Wall Code#
	####################
	if temp2 != player.x or temp3 != player.y:
		print("Player X:",player.x," Player Y:",player.y)
	temp2=player.x
	temp3=player.y 
	
	
	temp=0
	noMoveUp=""
	noMoveDown=""
	noMoveLeft=""
	noMoveRight=""
	for wall in Walls:
		if wall.rect.colliderect(player.blit) == 1:
			temp+=1
			if wall.rect.centery < player.blit.centery:
				print("OK!")
			if player.direction == main_left:
				wall.collisions["left"]=1
			elif player.direction == main_right:
				wall.collisions["right"]=1
			if player.direction == main_down:
				wall.collisions["down"]=1
			elif player.direction == main_up:
				wall.collisions["up"]=1
		for key,value in wall.collisions.items():
			if value == 1:
				print(key,value)
				if key == "left":
					noMoveLeft=True
				elif key == "right":
					noMoveRight=True
				
					
				if key == "up":
					noMoveUp=True
				elif key == "down":
					noMoveDown=True
	if temp == 0:
		for wall in Walls:
			for key in wall.collisions:
				wall.collisions[key]=0
				print(wall.collisions[key])
	temp=0
	for i in noMoveDown,noMoveLeft,noMoveRight,noMoveUp:
		if not i:
			temp+=1
	if temp==0:
		print("they can't move!")
	
	

	player.x=borderCheck(player.x,screen_x)
	player.y=borderCheck(player.y,screen_y)	
	
	if done == False:
		pygame.display.flip()
		clock.tick(60)
pygame.quit()
if done == True and game_over == True:
	log.append("LOG: Saving Highscore")
	print("LOG: Saving Highscore")
	if Name in scores:
		if scores[Name] < score:
			scores[Name]=score
	else:
		scores[Name]=score
	sortedScores={}
	highscore=open(path.join(os.path.dirname(__file__),'highscores.txt'),('w'))
	sortedScores = sorted(scores.items(), key=operator.itemgetter(1))
	for key, value in sortedScores:
		highscore.write(key)
		highscore.write(":")
		highscore.write(str(value))
		highscore.write("\n")
	log.append("LOG: Highscore Saved. Closing..")
	print("LOG: Highscore Saved. Closing..")
else:
	log.append("LOG: Window Closed Before Game Over. Closing...")
	print("LOG: Window Closed Before Game Over. Closing...")
input("press enter to exit")