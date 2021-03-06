from pygame import *
import random

init()
WIDHT = 128#64
HEIGHT = 128#64
SCALE = 8
SIZE = (WIDHT*SCALE,HEIGHT*SCALE)

screen = display.set_mode(SIZE)
surf = Surface((WIDHT,HEIGHT))

map = {}
entetys = []
deathgroup = []

units = [25,55,15,120,0,0]
#holz,stein,eisen,gold,kabeljau,bambus
#[0,0,0,0,0,0,0,0]
#Einheiten  Holz,Stein,Eisen,Bronze,Gold,Diamanten,Zwiebeln,Kaka
unitpic = image.load("pics/units.png")
numbers = image.load("pics/numbers.png")

selected = 0

clock = time.Clock()

def camtrans(pos):
	global cam
	return pos[0]-cam[0],pos[1]-cam[1]

def clamp(my_value,min_value,max_value):
	return max(min(my_value, max_value), min_value)

def drawnumber(number,x,y):
	global surf
	n = number
	if n>99:n =99
	if n <0:n=0;print("n is too low")
	num = str(n)
	surf.blit(numbers,(x,y),(int(num[0])*8,0,8,8))
	if len(num) == 2:
		surf.blit(numbers,(x+4,y),(int(num[1])*8,0,8,8))

def mapupdate():
	global map
	for k,item in map.iteritems():
		item.on_mapupdate()

class Building:
	sprite = image.load("pics/buildings.png")
	shadows = image.load("pics/shadows.png")
	roofs = image.load("pics/roofs.png")
	cancapacity = True
	id = 0
	price = [0,0,0,0,0,0] #gold,holz,eisen,kabeljau
	def __init__(self,pos):
		self.pos = pos
		self.capacity = [0,0,0,0,0,0,0,0]#Holz,Stein,Eisen,Bronze,Gold,Diamanten,Zwiebeln,Kaka
		self.owned = []
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
	def on_hover(self,screen):
		draw.rect(screen,(255,255,255),(0,HEIGHT-16,WIDHT,16))
		#draw.rect(screen,(0,0,0),(0,HEIGHT-8,WIDHT,8),1)
		for i,item in enumerate(self.capacity):
			drawnumber(item,i%4*16+8,HEIGHT-16+i//4*8)
			screen.blit(unitpic,(i%4*16,HEIGHT-16+i//4*8),(i*8,0,8,8))
	def on_pressed(self):
		print(self.id)
	def on_mapupdate(self):
		pass
	def on_hold(self,screen):
		pass
	def die(self):
		global deathgroup
		deathgroup.append(self)
	def rem(self):
		global map
		del map[self.pos]
		for o in self.owned:
			try:
				o.die()
			except:
				print("{} cant die".format(o))

class House(Building):
	id = 1
	price = [0,4,0,0,0,0]#gold,holz,eisen,kabeljau
	def __init__(self,pos):
		Building.__init__(self,pos)
		self.owned.append(WoodWorker((pos[0]+6,pos[1]+8)))# Worker 1
		self.owned.append(StoneWorker((pos[0]+8,pos[1]+9)))	# Worker 2
		self.owned.append(Worker((pos[0]+8,pos[1]+7))) # Worker 3

class SmallCasle(Building):
	id = 2
	price = [0,10,10,0,0,0]#gold,holz,eisen,kabeljau
	def __init__(self,pos):
		Building.__init__(self,pos)
class Tower(Building):
	id = 3
	sprite = image.load("pics/tower.png")
	shadows = image.load("pics/towershadow.png")
	price = [1,5,2,0,0,0]#gold,holz,eisen,kabeljau
	def __init__(self,pos):
		Building.__init__(self,pos)
		self.index = 0
	def draw(self,screen,layer):
		if layer == 0:
			pass
		elif layer == 2:
			screen.blit(self.shadows,camtrans(self.pos),(self.index%4*16,self.index//4*16,16,16))
		elif layer == 3:
			screen.blit(self.sprite,camtrans(self.pos),(self.index%4*16,self.index//4*16,16,16))
	def on_mapupdate(self):
		global map
		self.index = 0
		x,y = self.pos
		try:
			if map[x+16,y].id==self.id:
				self.index+=1
		except:pass
		try:
			if map[x,y-16].id==self.id:
				self.index+=2
		except:pass
		try:
			if map[x-16,y].id==self.id:
				self.index+=4
		except:pass
		try:
			if map[x,y+16].id==self.id:
				self.index+=8
		except:pass

class Stock(Building):
	id = 4
	price = [0,5,1,5,0,0]#gold,holz,eisen,kabeljau
	
	def __init__(self,pos):
		Building.__init__(self,pos)
		self.capacity = [0,0,0,0,0,0,0,0]#Holz,Stein,Eisen,Bronze,Gold,Diamanten,Zwiebeln,Kaka
	def update(self):
		global units
		Building.update(self)
	def on_pressed(self):
		for i,c in enumerate(self.capacity):
			if c>0:
				units[0]+=c 			#debug adding units
				units[1]+=c
				units[2]+=c
				units[3]+=c
				self.capacity[i] = 0

class Tree(Building):
	id = 5
	price = [0,0,0,0,0,0]#gold,holz,eisen,kabeljau
	
	def __init__(self,pos):
		Building.__init__(self,pos)
		self.capacity = [50,0,0,0,0,0,0,0]#Holz,Stein,Eisen,Bronze,Gold,Diamanten,Zwiebeln,Kaka
	def update(self):
		Building.update(self)
		a = 0
		for x in self.capacity:
			if x ==0:
				a+=1
		if a == len(self.capacity):
			self.die()

class Stone(Building):
	id = 6
	price = [0,0,0,0,0,0]
	def __init__(self,pos):
		Building.__init__(self,pos)
		self.capacity = [0,50,0,0,0,0,0,0]#Holz,Stein,Eisen,Bronze,Gold,Diamanten,Zwiebeln,Kaka
	def update(self):
		Building.update(self)
		a = 0
		for x in self.capacity:
			if x ==0:
				a+=1
		if a == len(self.capacity):
			self.die()

class WoodWorkerHouse(Building):
	id = 7
	price = [0,0,0,0,0,0]#gold,holz,eisen,kabeljau
	def __init__(self,pos):
		Building.__init__(self,pos)
		self.owned.append(WoodWorker((pos[0]+6,pos[1]+8))) # Worker 1

class StoneWorkerHouse(Building):
	id = 8
	price = [0,0,0,0,0,0]#gold,holz,eisen,kabeljau
	def __init__(self,pos):
		Building.__init__(self,pos)
		self.owned.append(StoneWorker((pos[0]+6,pos[1]+8))) # Worker 1



buildingClasses = [Building,House,SmallCasle,Tower,Stock,Tree,Stone,WoodWorkerHouse,StoneWorkerHouse]

class Entety:
	id = 0
	color = (255,0,0)
	def __init__(self,pos):
		self.pos = pos
		self.wait_time = 0
		entetys.append(self)
	def draw(self,screen):
		screen.set_at(camtrans(self.pos),self.color)
	def update(self):
		if self.wait_time>0:
			self.wait_time-=1
			return False
		return True
	def die(self):
		global deathgroup
		deathgroup.append(self)
	def rem(self):
		entetys.remove(self)

class Worker(Entety):
	color = (0,255,255)
	canpickup = [] # all ids
	def __init__(self,pos):
		Entety.__init__(self,pos)
		self.task = None #{"destpos":(0,0),"destB":Buling Instance,"seaching":False}
		self.carrying = None # {"id":0,"number":0}
		
	def update(self):
		if not Entety.update(self):
			return
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
						self.wait_time = 5


				elif self.carrying == None: 	# er hat nix mit dabei
					for i,c in enumerate(self.task["destB"].capacity):
						if c>0:
							self.carrying = {"id":i,"number":1}
							self.task["destB"].capacity[i]-=1
							self.task = None
							self.wait_time = 5
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
							self.wait_time = 5
			else:
				for pos,item in map.iteritems():
					if item.id != Stock.id:
						for i,c in enumerate(item.capacity):
							if c>0 and i in self.canpickup:
								rbuilding = item
								self.wait_time = 5
		if rbuilding:
			self.task = {"destpos":(rbuilding.pos[0]+random.randrange(0,16),rbuilding.pos[1]+random.randrange(0,16)),"destB":rbuilding}
		#print(self.task,self.carrying) 			#DEBUG


class WoodWorker(Worker):
	canpickup = [0] # all ids
	color = (50,250,150)
	def __init__(self,pos):
		Worker.__init__(self,pos)
class StoneWorker(Worker):
	canpickup = [1] # all ids
	color = (250,50,150)
	def __init__(self,pos):
		Worker.__init__(self,pos)
		



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
		mapupdate()

prePos = (0,0)
camD = 0,0
cam = 0,0
justpressed = [False,False,False,False]
frame = 0

def loop():
	global cam,selected,prePos,camD,frame,deathgroup

	while True:
		clock.tick(60)
		frame+=1
		deathgroup = []

		mpos = mouse.get_pos()
		
		npos = mpos[0]//SCALE,mpos[1]//SCALE
		tpos = npos[0]-8,npos[1]-8
		mrel = mouse.get_rel()
		#mrel = mpos[0]-prePos[0],mpos[1]-prePos[1]

		apos = (npos[0]+cam[0])//16*16,(npos[1]+cam[1])//16*16
		justpressed = [False,False,False,False,False,False]

		menus = [False,False]

		if mouse.get_pressed()[2]:
			camD =-mrel[0]*.2+camD[0],-mrel[1]*.2+camD[1]

		cam = int(camD[0]),int(camD[1])

		rpos = tpos[0]+cam[0],tpos[1]+cam[1]
		for e in event.get():
			if e.type == QUIT:
				return
			if e.type == MOUSEBUTTONDOWN:
				justpressed[e.button]=True
				if npos[1]>HEIGHT-16:
					mhaspressed = True
					sel = npos[0]//8 + (npos[1]-HEIGHT+16)//8*8
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
			draw.rect(trans,(27+20,28+20,22+20,127),(0,0,WIDHT,16))
			#draw.rect(trans,(27+10,28+10,22+10,255),(1,1,WIDHT-2,16-2),1)
			surf.blit(trans,(0,0))	
		else:
			trans = Surface((WIDHT,HEIGHT),SRCALPHA)					#UI Rect
			draw.rect(trans,(27+20,28+20,22+20,127),(0,0,WIDHT,8))
			#draw.rect(trans,(27+10,28+10,22+10,255),(1,1,WIDHT-2,8-2),1)
			surf.blit(trans,(0,0))
		for i,item in enumerate(units):								#Unit Drawing
			n = item
			if n>99:n =99
			if n <0:n=0;print("n is too low")
			num = str(n)
			surf.blit(numbers,(i*16+8,0),(int(num[0])*8,0,8,8))
			if len(num) == 2:
				surf.blit(numbers,(i*16+4+8,0),(int(num[1])*8,0,8,8))

		for i,item in enumerate(units):
			surf.blit(unitpic,(i*16,0),(i*8,0,8,8))										#Unit Texture

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
				surf.blit(transform.scale(b,(8,8)),(i%8*8,HEIGHT-16+i//8*8))
			draw.rect(surf,(255,255,255),(selected%8*8,HEIGHT-16+selected//8*8,8,8),1)
		else:
			trans = Surface((WIDHT,HEIGHT),SRCALPHA)					#UI Rect
			draw.rect(trans,(27+20,28+20,22+20,127),(0,HEIGHT-8,WIDHT,8))
			#draw.rect(trans,(27+10,28+10,22+10,255),(1,HEIGHT-8+1,WIDHT-2,8-2),1)
			surf.blit(trans,(0,0))
			if selected < len(buildingClasses):							#Buildings Small
				b = Surface((16,16),SRCALPHA)
				cl = buildingClasses[selected]
				b.blit(cl.sprite,(0,0),(cl.id%16*16,cl.id//16*16,16,16))
				b.blit(cl.roofs,(0,0),(cl.id%16*16,cl.id//16*16,16,16))
				surf.blit(transform.scale(b,(8,8)),(0,HEIGHT-8))

		if not menus[0] and not menus[1]:
			x,y = apos
			
			try:
				building = map[x,y]
				building.on_hover(surf)
				if mouse.get_pressed()[0]:
					building.on_hold(surf)
				if justpressed[1]:
					building.on_pressed()
				if justpressed[2]:
					building.die()
			except:
				draw.rect(surf,(255,255,255),((apos[0]-cam[0],apos[1]-cam[1]),(16,16)),1)

		b = transform.scale(surf,SIZE)
		screen.blit(b,(0,0))
		display.flip()

		for item in deathgroup:
			item.rem()
		

if __name__ == '__main__':
	loop()