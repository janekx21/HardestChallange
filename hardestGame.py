from pygame import *

init()
WIDHT = 64
HEIGHT = 64
SCALE = 8
SIZE = (WIDHT*SCALE,HEIGHT*SCALE)

screen = display.set_mode(SIZE)
surf = Surface((WIDHT,HEIGHT))

map = {}

units = [10,2,99,120]
#"gold":,"holz":,"eisen":,"kabeljau":
unitpic = image.load("pics/units.png")
numbers = image.load("pics/numbers.png")
cam = 0,0
selected = 0

def camtrans(pos):
	global cam
	return pos[0]-cam[0],pos[1]-cam[1]

class Building:
	sprite = image.load("pics/buildings.png")
	shadows = image.load("pics/shadows.png")
	id = 0
	price = [0,0,0,0]
	def __init__(self,pos):
		self.pos = pos
		map[pos]=self
	def draw(self,screen):
		screen.blit(self.sprite,camtrans(self.pos),(self.id%16*16,self.id//16*16,16,16))
		screen.blit(self.shadows,camtrans(self.pos),(self.id%16*16,self.id//16*16,16,16))

class House(Building):
	id = 1
	price = [1,0,0,0]
	def __init__(self,pos):
		Building.__init__(self,pos)

buildingClasses = [Building,House]

def spawn(pos,id):
	global units
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
				return
		units = u[:]
		b= bu(pos)



for x in range(4):
	for y in range(4):
		b = spawn((x*16,y*16),x+y*16)

def loop():
	global cam,selected
	while True:
		mpos = mouse.get_pos()
		npos = mpos[0]//SCALE,mpos[1]//SCALE
		tpos = npos[0]-8,npos[1]-8
		mrel = mouse.get_rel()

		mhaspressed=False

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
					spawn(rpos,selected)
				

		surf.fill((27,28,22))
		

		for pos,item in map.iteritems():
			item.draw(surf)

		if npos[1] < 16:
			trans = Surface((WIDHT,HEIGHT),SRCALPHA)
			draw.rect(trans,(27+20,28+20,22+20,245),(0,0,WIDHT,16))
			draw.rect(trans,(27+10,28+10,22+10,255),(1,1,WIDHT-2,16-2),1)
			surf.blit(trans,(0,0))
			
			for i,item in enumerate(units):
				n = item
				if n>99:n =99
				if n <0:n=0;print("n is too low")
				num = str(n)
				surf.blit(numbers,(i*8,8),(int(num[0])*8,0,8,8))
				if len(num) == 2:
					surf.blit(numbers,(i*8+4,8),(int(num[1])*8,0,8,8))
		else:
			trans = Surface((WIDHT,HEIGHT),SRCALPHA)
			draw.rect(trans,(27+20,28+20,22+20,127),(0,0,WIDHT,8))
			draw.rect(trans,(27+10,28+10,22+10,255),(1,1,WIDHT-2,8-2),1)
			surf.blit(trans,(0,0))
		surf.blit(unitpic,(0,0))

		if npos[1] > HEIGHT-16:
			trans = Surface((WIDHT,HEIGHT),SRCALPHA)
			draw.rect(trans,(27+20,28+20,22+20,245),(0,HEIGHT-16,WIDHT,16))
			draw.rect(trans,(27+10,28+10,22+10,255),(1,HEIGHT-16+1,WIDHT-2,16-2),1)
			surf.blit(trans,(0,0))
			for i,cl in enumerate(buildingClasses):
				b = Surface((16,16),SRCALPHA)
				b.blit(cl.sprite,(0,0),(cl.id%16*16,cl.id//16*16,16,16))
				surf.blit(transform.scale(b,(8,8)),(i*8,HEIGHT-16))
			draw.rect(surf,(255,255,255),(selected*8,HEIGHT-16,8,8),1)
		else:
			trans = Surface((WIDHT,HEIGHT),SRCALPHA)
			draw.rect(trans,(27+20,28+20,22+20,127),(0,HEIGHT-8,WIDHT,8))
			draw.rect(trans,(27+10,28+10,22+10,255),(1,HEIGHT-8+1,WIDHT-2,8-2),1)
			surf.blit(trans,(0,0))


		draw.rect(surf,(255,255,255),(tpos,(16,16)),1)
		b = transform.scale(surf,SIZE)
		screen.blit(b,(0,0))
		display.flip()

if __name__ == '__main__':
	loop()