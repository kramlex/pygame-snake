import pygame
import random
import time
import os
import pygame_textinput

#
screensize = [1280,720]
backgroud = [0,0,0]
snakelen = 10
aCount = 2
delayi = 0.000
pygame.init()
#

def get_max_record(records):
	return records[0][0]

def get_records():
	records_file = open('records.txt')
	records_lines = records_file.readlines()
	records_file.close()
	records_list = []
	for line in records_lines:
		line = line.split()
		tmp = [ int(line[0]) , str(line[1])]
		records_list.append(tmp)
	return records_list

def sort_records_file():
	records_file = open('records.txt')
	records_lines = records_file.readlines()
	records_file.close()
	records_list = []

	for line in records_lines:
		line = line.split()
		tmp = [ int(line[0]) , str(line[1])]
		records_list.append(tmp)
	records_list.sort(reverse = True)

	records_file = open('records.txt', 'w')
	for i in range( len(records_list) ):
		if i != len(records_list)-1:
			record_string = ""
			record_string += str(records_list[i][0]) + " " + str(records_list[i][1]) + "\n"
			records_file.write(record_string) 
		else:
			record_string = ""
			record_string += str(records_list[i][0]) + " " + str(records_list[i][1])
			records_file.write(record_string) 
def add_new_record(name, score):
	record_name = name.split()
	record_name = record_name[0]
	records_file = open('records.txt', 'a')
	records_file.write('\n'+ score + " " + str(record_name))


class SNAKEGAME:
	def init(self):
		pygame.font.init()
		global snakelen
		snakelen = 10
		self.font = pygame.font.Font('8289.otf', 30)
		self.fscore = pygame.font.Font('8289.otf', 16)
		self.screen = pygame.display.set_mode(screensize)
		self.score = 0
		self.direcion = "right"
		self.Finished = False
		self.gameover = False
		self.pause = False
		self.apple = []
		self.sapple = []
		self.sapplerand = False

		for i in range (aCount):
			self.apple.append(APPLE())
			self.apple[i].init()
		for i in range (aCount):
			self.sapple.append(SAPPLE())
			self.sapple[i].init()
		self.draw()

	def draw(self):
		self.fontscore = snakegame.font.render(str(self.score),True, gsnake.snakecolor1	)
		self.fontscore_size = self.fontscore.get_size()
		self.screen.fill(backgroud)

		for i, f in enumerate(self.apple):
			f.draw()
		for i , f in enumerate(self.sapple):
			if self.sapplerand == True and self.score != 0:
				f.draw()


		snakegame.screen.blit(self.fontscore, [1275 - self.fontscore_size[0], 5 ])
		gsnake.draw()
		pygame.display.flip()




	def update(self):
		for i, f in enumerate(self.apple):
			f.update(i)
		gsnake.update()
		for i , f in enumerate(self.sapple):
			if self.sapplerand == True and self.score != 0:	
				f.update(i)


class SAPPLE:
	def init(self):
		#sapplecolor
		self.sapplecolor1 = [244,0,161]
		self.timeinit = int(time.time())
		#
		while True:
			self.sax = random.randint(20,1260)
			self.say = random.randint(20,700)
			if self.sax % 10 == 0 and self.say % 10 == 0:
				break

	def draw(self):
		if ( int(self.timeinit) - int(time.time()) ) % 2 == 0:
			pygame.draw.rect(snakegame.screen , self.sapplecolor1 , [self.sax , self.say , 10 ,10 ] , 0)
		#[235,235,235]
		else:
			pygame.draw.rect(snakegame.screen , [235,235,235] , [self.sax , self.say , 10 ,10 ] , 0)
			


	def update(self , i):
		if gsnake.snake[0][0] == self.sax and gsnake.snake[0][1] == self.say:
			snakegame.score += 2
			del snakegame.sapple[i]
			snakegame.sapple.append(SAPPLE())
			snakegame.sapple[-1].init()
			global delayi
			delayi += 0.001
			snakegame.sapplerand = False


class APPLE:
	def init(self):
		#foodcolor
		self.applecolor1 = [27,255,111]
		self.applecolor2 = [228, 0, 69]
		#
		while True:
			self.ax = random.randint(20, 1260)
			self.ay = random.randint(20, 700)
			if self.ax % 10 == 0 and self.ay % 10 == 0:
				break
	def draw(self):
		pygame.draw.rect(snakegame.screen , self.applecolor1 , [self.ax , self.ay , 10 ,10] , 0)

	def update(self, i):
		if gsnake.snake[0][0] == self.ax and gsnake.snake[0][1] == self.ay:
			snakegame.score += 1
			del snakegame.apple[i]
			snakegame.apple.append(APPLE())
			snakegame.apple[-1].init()
			global snakelen
			snakelen += 1
			gsnake.snake.append([99999,99999])

			l = random.randint(1,8);
			if l == 3 and snakegame.sapplerand == False:
				snakegame.sapplerand = True

class SNAKE:
	def init(self):
		#snakecolor
		self.snakecolor1 = [240,234,40] #yellow
		self.snakecolor2 = [244,0,161] #purple
		#
		self.initx = 640
		self.inity = 360
		self.snake = []
		for i in range(snakelen):
			self.tmp = [self.initx,self.inity]
			self.snake.append(self.tmp)
			self.initx -= 10

	def draw(self):
		for i in range(snakelen):
			pygame.draw.rect(snakegame.screen, self.snakecolor1 , [ self.snake[i][0] , self.snake[i][1] ,10,10],0)

	def update(self):
		for i in range(snakelen-1,-1,-1):
			if i == 0:
				if snakegame.direcion == "left":
					self.snake[i][0] -= 10
				elif snakegame.direcion == "right":
					self.snake[i][0] += 10
				elif snakegame.direcion == "up":
					self.snake[i][1] -= 10
				elif snakegame.direcion == "down":
					self.snake[i][1] += 10

				if self.snake[i][0] <= -10 and snakegame.direcion == "left":
					self.snake[i][0] = 1270
				if self.snake[i][0] >= 1280 and snakegame.direcion == "right":
					self.snake[i][0] = 0
				if self.snake[i][1] <= -10 and snakegame.direcion == "up":
					self.snake[i][1] = 710
				if self.snake[i][1] >= 720 and snakegame.direcion == "down":
					self.snake[i][1] = 0

				for j in range(1,snakelen-1):
					if self.snake[i][1] == self.snake[j][1] and self.snake[i][0] == self.snake[j][0]:
						snakegame.gameover = True 

			else:
				self.snake[i][0] = self.snake[i-1][0]
				self.snake[i][1] = self.snake[i-1][1]

def game_process():
	global getStart, getMenu
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				snakegame.Finished = True
				break
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					#snakegame.Finished = True
					getStart = False
					getMenu = True
					break
				elif event.key == pygame.K_w and snakegame.direcion != "down":
					snakegame.direcion = "up"
					break
				elif event.key == pygame.K_s and snakegame.direcion != "up":
					snakegame.direcion = "down"
					break
				elif event.key == pygame.K_d and snakegame.direcion != "left":
					snakegame.direcion = "right"
					break
				elif event.key == pygame.K_a and snakegame.direcion != "right":
					snakegame.direcion = "left"
					break
				elif event.key == pygame.K_p and snakegame.pause == False:
					snakegame.pause = True
					continue
				elif event.key == pygame.K_p and snakegame.pause == True:
					snakegame.pause = False
		

		if snakegame.pause == True:
				continue
		if getStart == False:
			break

		if snakegame.gameover == True:
			add_true = False
			while snakegame.gameover == True:
				font_eneter_name = pygame.font.Font('8289.otf', 30)
				sort_records_file()
				allrecords = get_records()
				allrecords_max = get_max_record(allrecords)
				if allrecords_max < snakegame.score and add_true == False:
					textinput = pygame_textinput.TextInput()
					add_new = False
					name = ""
					while True:
						events = pygame.event.get()
						for event in events:
							if event.type == pygame.KEYDOWN:
								if event.key == pygame.K_RETURN:
									name = textinput.get_text()
									add_new = True
									break
						if add_new == True:
							add_true = True
							break
						snakegame.screen.fill([255,50,50])
						enter_name = "Enter your name:"
						font = pygame.font.Font('8289.otf', 30)
						render_enter_name = font.render(enter_name,True,[255,255,255])
						render_enter_name_size = render_enter_name.get_size()
						snakegame.screen.blit( render_enter_name , [360 - render_enter_name_size[0]/2 , 360 - render_enter_name_size[1]])

						textinput.update(events)
						snakegame.screen.blit(textinput.get_surface(), (370 + render_enter_name_size[0]/2, 360 - render_enter_name_size[1] ))
						pygame.display.update()
						pygame.display.flip()
					#-----------------------------------------------
					add_new_record(name, str(snakegame.score))
				snakegame.screen.fill([255,50,50])
				lose = "YOU LOSE! Your Score: "
				font1 = snakegame.font.render(lose + str(snakegame.score),True,[255,255,255])
				font1_size = font1.get_size()
				snakegame.screen.blit(font1, [640 - font1_size[0]/2 , 360 - font1_size[1]])
				font2 = snakegame.font.render('Press R to restart',True,[255,255,255])
				font3 = snakegame.font.render('Press ESC to MENU',True,[255,255,255])
				font2_size = font2.get_size()
				font3_size = font3.get_size()
				snakegame.screen.blit(font2, [640 - font2_size[0]/2 , 360 + font2_size[1]])
				snakegame.screen.blit(font3, [640 - font3_size[0]/2 , 360 + font2_size[1] + font3_size[1]])
				pygame.display.flip()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						getStart = False
						break
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_r:
							snakegame.gameover = False
							gsnake.init()
							snakegame.init()
							pygame.time.wait(500)
							break
						if event.key == pygame.K_ESCAPE:
							getStart = False
							getMenu = True

				if getStart == False:
					break
		snakegame.draw()
		snakegame.update()
		time.sleep(0.045 - delayi)

def record_menu():
	global getRecord, Finished , getMenu
	screen = pygame.display.set_mode(screensize)
	image_name = os.path.join('img' , 'record.png')
	img = pygame.image.load(image_name)
	img = img.convert()
	records = get_records()
	surfy = 150
	fontrec = pygame.font.Font('8289.otf', 30)
	records_surf = []
	if len(records) > 10:
		for i in range(10):
			tmp = [ fontrec.render(str(records[i][1]) + " " + str(records[i][0]) , True , [240,234,40] ) , surfy]
			records_surf.append(tmp)
			surfy += 40
	else:
		for i in range( len(records) ):
			tmp = [fontrec.render(str(records[i][1]) + " " + str(records[i][0]) , True , [240,234,40] ) , surfy]
			records_surf.append(tmp)
			surfy += 40


	fontR = pygame.font.Font('8289.otf', 40)
	record_text = fontR.render("RECORDS", True , [240,234,40])
	score_name_text = pygame.font.Font('8289.otf', 31).render("Name score",True, [240,234,41])
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Finished = True
				break
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
						getRecord = False
						getMenu = True
						break
		if Finished == True:
			break
		if getRecord == False:
			break

		screen.blit(img , [0,0])
		screen.blit(record_text, [670, 30])
		screen.blit(score_name_text, [630, 140 - records_surf[0][0].get_size()[1] ])
		for i in records_surf:
			screen.blit(i[0] , [630, i[1]] )
			pygame.draw.rect(screen, [240,234,40] , [630 - 20, i[1] - 3 + i[0].get_size()[1]/3  , i[0].get_size()[1]/3 , i[0].get_size()[1]/3] , 0)
		pygame.display.flip()

def info_menu():
	global getInfo, Finished , getMenu
	screen = pygame.display.set_mode(screensize)
	image_name = os.path.join('img' , 'record.png')
	img = pygame.image.load(image_name)
	img = img.convert()
	fontI = pygame.font.Font('8289.otf', 40)
	record_text = fontI.render("INFO", True , [240,234,40])
	text_font = pygame.font.Font('8289.otf', 31)
	text_info = []
	textx = 50
	text_info.append( [text_font.render("The game is a classical snake game.",True,[240,234,40]) , textx ] )
	textx += text_font.render("The game is a classical snake game.",True,[240,234,40]).get_size()[1] + 8 

	text_info.append( [text_font.render("Game controls",True,[240,234,40]) , textx ] )
	textx += text_font.render("Game controls",True,[240,234,40]).get_size()[1] + 8 

	text_info.append( [text_font.render("W up",True,[240,234,40]) , textx ] )
	textx += text_font.render("W up",True,[240,234,40]).get_size()[1] + 8 

	text_info.append( [text_font.render("s down",True,[240,234,40]) , textx ] )
	textx += text_font.render("s down",True,[240,234,40]).get_size()[1] + 8 

	text_info.append( [text_font.render("a left",True,[240,234,40]) , textx ] )
	textx += text_font.render("a left",True,[240,234,40]).get_size()[1] + 8 

	text_info.append( [text_font.render("d right",True,[240,234,40]) , textx ] )
	textx += text_font.render("d right",True,[240,234,40]).get_size()[1] + 8 

	text_info.append( [text_font.render("need to pick up apples",True,[240,234,40]) , textx ] )
	textx += text_font.render("need to pick up apples",True,[240,234,40]).get_size()[1] + 8 

	text_info.append( [text_font.render("super Apple gives you 2 points and ",True,[240,234,40]) , textx ] )
	textx += text_font.render("super Apple gives you 2 points and speed boosts",True,[240,234,40]).get_size()[1] + 8 

	text_info.append( [text_font.render("speed boosts",True,[240,234,40]) , textx ] )
	textx += text_font.render("speed boosts",True,[240,234,40]).get_size()[1] + 8 

	text_info.append( [text_font.render("Apple increases the snake and gives",True,[240,234,40]) , textx ] )
	textx += text_font.render("Apple increases the snake and gives you 1 point",True,[240,234,40]).get_size()[1] + 8 

	text_info.append( [text_font.render("you 1 point",True,[240,234,40]) , textx ] )
	textx += text_font.render("you 1 point",True,[240,234,40]).get_size()[1] + 8 

	text_info.append( [text_font.render("The Creator of the game Mark",True,[240,234,40]) , textx ] )
	textx += text_font.render("The Creator of the game Mark",True,[240,234,40]).get_size()[1] + 8 
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				Finished = True
				break
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					getInfo = False
					getMenu = True
					break
		if Finished == True:
			break
		if getInfo == False:
			break

		screen.blit(img , [0,0])
		for i in text_info:
			screen.blit(i[0] , [540, i[1]] )
		pygame.display.flip()







def MENU():
	global getStart, Finished, getRecord , getMenu, getInfo
	screen = pygame.display.set_mode(screensize)
	image_name = os.path.join('img', 'menu.png')
	img = pygame.image.load(image_name)
	punkt_name = os.path.join('img', 'punkt.png')
	punkt = pygame.image.load(punkt_name)
	punkt = punkt.convert()
	img = img.convert()
	mStart = True
	mRecords = False
	mInfo = False
	mExit = False
	Finished = False
	while True:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					Finished = True
					break
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_w and mRecords:
						mRecords = False
						mStart = True
						break
					elif event.key == pygame.K_w and mInfo:
						mInfo = False
						mRecords = True
						break
					elif event.key == pygame.K_w and mExit:
						mExit = False
						mInfo = True
						break

					elif event.key == pygame.K_s and mStart:
						mStart = False
						mRecords = True
						break
					elif event.key == pygame.K_s and mRecords:
						mRecords = False
						mInfo = True
						break
					elif event.key == pygame.K_s and mInfo:
						mInfo = False
						mExit = True 
						break
					
					elif event.key == pygame.K_RETURN and mStart:
						getStart = True
						getMenu = False
						break
					elif event.key == pygame.K_RETURN and mExit:
						Finished = True
						break
					elif event.key == pygame.K_RETURN and mInfo:
						getInfo = True
						getMenu = False
						break
					elif event.key == pygame.K_RETURN and mRecords:
						getRecord = True
						getMenu = False
						break

		if Finished == True:
			break
		if getStart == True:
			break
		if getRecord == True:
			break
		if getInfo == True:
			break
		screen.blit(img , [0,0])
		if mStart:
			screen.blit(punkt, [655,227])
			#pygame.draw.rect(screen, [240,234,40] , [650, 210 , 40 , 40] , 0)
		elif mRecords:
			screen.blit(punkt, [620,227+115])
			#pygame.draw.rect(screen, [240,234,40] , [630, 420 , 40 , 40] , 0)
		elif mInfo:
			screen.blit(punkt, [690,227+230])
			#pygame.draw.rect(screen, [240,234,40] , [630, 420 , 40 , 40] , 0)
		elif mExit:
			screen.blit(punkt, [685,227+ 345])
			#pygame.draw.rect(screen, [240,234,40] , [630, 420 , 40 , 40] , 0)
		pygame.display.flip()


getStart = False
getRecord = False
Finished = False
getMenu = True
getInfo = False
while True:
	if getStart == True:
		gsnake = SNAKE()
		gsnake.init()
		snakegame = SNAKEGAME()
		snakegame.init()
		game_process()
	elif getRecord == True:
		record_menu()
	elif getInfo == True:
		info_menu()
	elif getMenu == True:
		MENU()
		if Finished == True:
			break









