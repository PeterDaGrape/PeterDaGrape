
import ui, io
import math
import PIL
from PIL import Image
import Image
import time

imax = 0

itermax = 600

xtap = 0
ytap = 0

xtapold = 0
ytapold = 0

upscale = 1

screensizex = 2732 / 2
screensizey = 2048 / 2
zoomfactor = 16

iterfactor = 1

screensizex = int(screensizex)
screensizey = int(screensizey)


startx = -2
starty = -1.2
stopx = 0.6
stopy = 1.2


def generator(startx, starty, stopx, stopy, screensizex, screensizey):
	print('Calculating...')
	#halfscreenx = screensizex / 2
	#halfscreeny = screensizey / 2
	global stepsize
	stepsize = (stopy - starty) / (screensizey)
	stopx = stepsize * screensizex + startx
	xn = 0
	yn = 0
	yc = starty
	xnplus1 = 0
	ynplus1 = 0
	imax = 0
	
	for ypix in range(screensizey):
		xc = startx
		for xpix in range(screensizex):
			xn = 0
			yn = 0
								
			for i in range(itermax):
				xnplus1 = xn**2 - yn**2 + xc
				ynplus1 = (2 * xn * yn) + yc
				xn = xnplus1
				yn = ynplus1
				if imax < i:
					imax = i
				if xn*xn + yn*yn > 4:
					break
				#print(i)
			#print(i)

			
			if i < (itermax - 1):
				color = int(round(itermax * (math.sqrt(i / itermax))))
				#color = (int(i / itermax)*255)
			#color = int((1 - (i / itermax))*255)
			
			else:
				color = 0
			
			pmand[xpix, ypix] = (color, color, color)
			xc = (xc + stepsize)
			
		yc = (yc + stepsize)
	
	mandPIL.show()
	print(imax)

def uizoom():
	def pil2ui(imgIn):
		with io.BytesIO() as bIO:
			mandPIL.save(bIO, 'PNG')
			imgOut = ui.Image.from_data(bIO.getvalue())
		return imgOut
		
	class MyView(ui.View):
		def __init__(self, pil, *args, **kwargs):
			super().__init__(self, *args, **kwargs)

			global iv
			iv = ui.ImageView()

			iv.touch_enabled = True

			iv.frame = (0, 0, screensizex*upscale, screensizey*upscale)
			self.add_subview(iv)
			iv.image = pil2ui(pil)
			

		def touch_began(self, touch):
			x,y = touch.location
			self.name = f'x={x} y={y}'
			global xtap, ytap

			xtap = round(x / upscale)
			ytap = round(y / upscale) 
			



		
			
	
	pil = Image.open('test:Lenna')
	wi,hi = pil.size

	
	'''
	w = 400
	h = w * hi/wi
	'''
	w = screensizex *upscale
	h = screensizey *upscale
	mv = MyView(pil,frame=(0,0,w,h))
	mv.present('sheet')
	

mandPIL = Image.new('RGB', (screensizex, screensizey))

pmand = mandPIL.load()



start_time = time.time()
generator(startx, starty, stopx, stopy, screensizex, screensizey)
print("--- %s seconds ---" % (time.time() - start_time))

uizoom()
#print(xtap, ytap)


while True:
	

	if not ((ytap == ytapold) and (xtap == xtapold)):

		xtapold = xtap
		ytapold = ytap	
		
		print(xtap, ytap)
		xtap = int(xtap)
		ytap = int(ytap)

		oldstartx = startx
		oldstarty = starty
		oldstopx = stopx
		oldstopy = stopy
		
		
		itermax = int(itermax * iterfactor)
		print(itermax)
		
		print((stopx - startx) / zoomfactor)
		#print((stopy - starty) / zoomfactor)

		
		
		cptapx = ((stepsize * xtap) + oldstartx)
		cptapy = ((stepsize * ytap) + oldstarty)
		
		stepsize = stepsize / zoomfactor
		
		
		'''
		startx = (cptapx + ((oldstartx - oldstopx) / zoomfactor))
		starty = (cptapx + ((oldstarty - oldstopy) / zoomfactor))
		stopx = (cptapy - ((oldstartx - oldstopx) / zoomfactor))
		stopy = (cptapy - ((oldstarty - oldstopy) / zoomfactor))
		'''


		startx = cptapx - (stepsize * screensizex/2)
		stopx = cptapx + (stepsize * screensizex/2)
		starty = cptapy - (stepsize * screensizey/2)
		stopy = cptapy + (stepsize * screensizey/2)
		
		print(startx, stopx, starty, stopy)


		start_time = time.time()
		generator(startx, starty, stopx, stopy, screensizex, screensizey)
		print("--- %s seconds ---" % (time.time() - start_time))
		
		uizoom()

		


		
print('done')
