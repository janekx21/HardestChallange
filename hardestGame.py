from pygame import *
import random

init()
WIDHT = 64
HEIGHT = 64
SCALE = 8
SIZE = (WIDHT*SCALE,HEIGHT*SCALE)

screen = display.set_mode(SIZE)
surf = Surface((WIDHT,HEIGHT))

map = {}
entetys = []

units = [25,55,15,120]
#"gold":,"holz":,"eisen":,"kabeljau":
#[0,0,0,0,0,0,0,0]
#Einheiten  Holz,Stein,Eisen,Bronze,Gold,Diamanten,Zwiebeln,Kaka
unitpic = image.load("pics/units.png")
numbers = image.load("pics/numbers.png")
cam = 0,0
selected = 0

clock = time.Clock()

def camtrans(pos):
	global cam
	return pos[0]-cam[0],pos[1]-cam[1]

def clamp(my_value,min_value,max_value):
	return max(min(my_value, max_value), min_value)

class Building:
	sprite = image.load("pics/buildings.png")
	shadows = image.load("pics/shadows.png")
	roofs = image.load("pics/roofs.png")
	id = 0
	price = [0,0,0,0] #gold,holz,eisen,kabeljau
	def __init__(self,pos):
		self.pos = pos
		self.capacity = [0,0,0,0,0,0,0,0]#Holz,Stein,Eisen,Bronze,Gold,Diamanten,Zwiebeln,Kaka
		map[pos]=self
	def draw(self,screen,layer): # color,entety,shadow,roof
		if layer == 0:
			screen.blit(self.sprite,camtrans(self.pos),(self.id%16*16,self.id//16*16,16,16))
		elif layer == 2:
			screen.blit(self.shadows,camtrans(self.pos),(self.id%16*16,self.id//16*16,16,16))
		elif layer == 3:
			screen.blit(self.roofs,camtrans(self.pos),(self.id%16*16,self.id//16*16,16,16))
	def update(self):
		pass

class House(Building):
	id = 1
	price = [0,4,0,0]#gold,holz,eisen,kabeljau
	def __init__(self,pos):
		Building.__init__(self,pos)
		Worker((pos[0]+6,pos[1]+8)) # Worker 1
		Worker((pos[0]+8,pos[1]+9))	# Worker 2
		Worker((pos[0]+8,pos[1]+7)) # Worker 3

class SmallCasle(Building):
	id = 2
	price = [0,10,10,0]#gold,holz,eisen,kabeljau
	def __init__(self,pos):
		Building.__init__(self,pos)
		self.capacity = [10,0,0,0,0,2,5,0]#Holz,Stein,Eisen,Bronze,Gold,Diamanten,Zwiebeln,Kaka

class Tower(Building):
	id = 3
	price = [1,5,2,0]#gold,holz,eisen,kabeljau
	def __init__(self,pos):
		Building.__init__(self,pos)
class Stock(Building):
	id = 4
	price = [0,5,1,5]#gold,holz,eisen,kabeljau
	
	def __init__(self,pos):
		Building.__init__(self,pos)
		self.capacity = [0,0,0,0,0,0,0,0]#Holz,Stein,Eisen,Bronze,Gold,Diamanten,Zwiebeln,Kaka
	def update(self):
		global units
		Building.update(self)
		for i,c in enumerate(self.capacity):
			if c>0:
				units[0]+=c 			#debug adding units
				units[1]+=c
				units[2]+=c
				units[3]+=c
				self.capacity[i] = 0

class Tree(Building):
	id = 5
	price = [0,0,0,0]#gold,holz,eisen,kabeljau
	
	def __init__(self,pos):
		Building.__init__(self,pos)
		self.capacity = [50,0,0,0,0,0,0,0]#Holz,Stein,Eisen,Bronze,Gold,Diamanten,Zwiebeln,Kaka


buildingClasses = [Building,House,SmallCasle,Tower,Stock,Tree]

class Entety:
	id = 0
	color = (255,0,0)
	def __init__(self,pos):
		self.pos = pos
		entetys.append(self)
	def draw(self,screen):
		screen.set_at(camtrans(self.pos),self.color)
	def update(self):
		pass

class Worker(Entety):
	color = (0,255,255)
	def __init__(self,pos):
		Entety.__init__(self,pos)
		self.task = None #{"destpos":(0,0),"destB":Buling Instance,"seaching":False}
		self.carrying = None # {"id":0,"number":0}
	def update(self):
		rbuilding = None
		if self.task: 								# er hat ein ziel
			offset = self.task["destpos"][0]-self.pos[0],self.task["destpos"][1]-self.pos[1]	#MOVING
			offset = clamp(offset[0],-1,1),clamp(offset[1],-1,1)
			if offset[0] == 0 and offset[1]==0: 					# wenn er ankommt
				if self.task["destB"].id == Stock.id: 				#abladen
					if self.carrying:
						self.task["destB"].capacity[self.carrying["id"]]+=self.carrying["number"]
						self.carrying = None
						self.task = None


				elif self.carrying == None: 	# er hat nix mit dabei
					for i,c in enumerate(self.task["destB"].capacity):
						if c>0:
							self.carrying = {"id":i,"number":1}
							self.task["destB"].capacity[i]-=1
							self.task = None
							break
					self.task=None
					#print("task = NONE Reset")
					
			##Random Walk adding
			#offset = offset[0]+random.randrange(-1,2),offset[1]+random.randrange(-1,2)
			#offset = clamp(offset[0],-1,1),clamp(offset[1],-1,1)
			self.pos = self.pos[0]+offset[0],self.pos[1]+offset[1]
		else:
			if self.carrying:
				for pos,item in map.iteritems():
						if item.id == Stock.id:
							rbuilding = item
			else:
				for pos,item in map.iteritems():
					if item.id != Stock.id:
						for c in item.capacity:
							if c>0:
								rbuilding = item
		if rbuilding:
			self.task = {"destpos":(rbuilding.pos[0]+random.randrange(0,16),rbuilding.pos[1]+random.randrange(0,16)),"destB":rbuilding}
		#print(self.task,self.carrying) 			#DEBUG




def spawn(pos,id):
	global units,map
	bu = None
	try:
		bu = buildingClasses[id]
	except:
		print("index:"+str(id)+" not found")
	if bu:
		u = units[:]
		for i,x in enumerate(u):
			u[i]-=bu.price[i]
			if u[i]<0:
				print("zu wenig Resorzen")
				return
		if pos in map:
			print("da steht schon was")
			return
		units = u[:]
		b= bu(pos)


def loop():
	global cam,selected
	while True:
		clock.tick(60)
		mpos = mouse.get_pos()
		npos = mpos[0]//SCALE,mpos[1]//SCALE
		tpos = npos[0]-8,npos[1]-8
		mrel = mouse.get_rel()

		apos = (npos[0]+cam[0])//16*16,(npos[1]+cam[1])//16*16

		menus = [False,False]

		if mouse.get_pressed()[2]:
			cam = mrel[0]+cam[0],mrel[1]+cam[1]
		rpos = tpos[0]+cam[0],tpos[1]+cam[1]
		for e in event.get():
			if e.type == QUIT:
				return
			if e.type == MOUSEBUTTONDOWN:
				if npos[1]>HEIGHT-16:
					mhaspressed = True
					sel = npos[0]//8
					selected = sel
				elif e.button == 1:
					spawn(apos,selected)

		for pos,item in map.iteritems():
			item.update()

		for entety in entetys:
			entety.update()
	

		#surf.fill((27,28,22))
		surf.fill((24, 224, 67))

		for pos,item in map.iteritems():
			item.draw(surf,0)

		for pos,item in map.iteritems():
			item.draw(surf,1)

		for entety in entetys:
			entety.draw(surf)

		for pos,item in map.iteritems():
			item.draw(surf,2)

		for pos,item in map.iteritems():
			item.draw(surf,3)

		if npos[1] < 16:
			menus[0] = True
			trans = Surface((WIDHT,HEIGHT),SRCALPHA)					#UI Rect
			draw.rect(trans,(27+20,28+20,22+20,245),(0,0,WIDHT,16))
			draw.rect(trans,(27+10,28+10,22+10,255),(1,1,WIDHT-2,16-2),1)
			surf.blit(trans,(0,0))

			for i,item in enumerate(units):								#Unit Drawing
				n = item
				if n>99:n =99
				if n <0:n=0;print("n is too low")
				num = str(n)
				surf.blit(numbers,(i*8,8),(int(num[0])*8,0,8,8))
				if len(num) == 2:
					surf.blit(numbers,(i*8+4,8),(int(num[1])*8,0,8,8))
		else:
			trans = Surface((WIDHT,HEIGHT),SRCALPHA)					#UI Rect
			draw.rect(trans,(27+20,28+20,22+20,127),(0,0,WIDHT,8))
			draw.rect(trans,(27+10,28+10,22+10,255),(1,1,WIDHT-2,8-2),1)
			surf.blit(trans,(0,0))
		surf.blit(unitpic,(0,0))										#Unit Texture

		if npos[1] > HEIGHT-16:
			menus[1] = True
			trans = Surface((WIDHT,HEIGHT),SRCALPHA)					#UI Rect
			draw.rect(trans,(27+20,28+20,22+20,245),(0,HEIGHT-16,WIDHT,16))
			draw.rect(trans,(27+10,28+10,22+10,255),(1,HEIGHT-16+1,WIDHT-2,16-2),1)
			surf.blit(trans,(0,0))
			for i,cl in enumerate(buildingClasses):						#Buildings
				b = Surface((16,16),SRCALPHA)
				b.blit(cl.sprite,(0,0),(cl.id%16*16,cl.id//16*16,16,16))
				b.blit(cl.roofs,(0,0),(cl.id%16*16,cl.id//16*16,16,16))
				surf.blit(transform.scale(b,(8,8)),(i*8,HEIGHT-16))
			draw.rect(surf,(255,255,255),(selected*8,HEIGHT-16,8,8),1)
		else:
			trans = Surface((WIDHT,HEIGHT),SRCALPHA)					#UI Rect
			draw.rect(trans,(27+20,28+20,22+20,127),(0,HEIGHT-8,WIDHT,8))
			draw.rect(trans,(27+10,28+10,22+10,255),(1,HEIGHT-8+1,WIDHT-2,8-2),1)
			surf.blit(trans,(0,0))
			if selected < len(buildingClasses):							#Buildings Small
				b = Surface((16,16),SRCALPHA)
				cl = buildingClasses[selected]
				b.blit(cl.sprite,(0,0),(cl.id%16*16,cl.id//16*16,16,16))
				b.blit(cl.roofs,(0,0),(cl.id%16*16,cl.id//16*16,16,16))
				surf.blit(transform.scale(b,(8,8)),(0,HEIGHT-8))

		if not menus[0] and not menus[1]:
			draw.rect(surf,(255,255,255),((apos[0]-cam[0],apos[1]-cam[1]),(16,16)),1)
		b = transform.scale(surf,SIZE)
		screen.blit(b,(0,0))
		display.flip()

if __name__ == '__main__':
	loop()