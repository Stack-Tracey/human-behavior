import json
from copy import copy
from client.actor import game
from PIL import Image, ImageDraw

COLOR_SIMPLE = (0xff,0xff,0xff,0xff)
COLOR_SMOOTH = (0x00,0xff,0x00,0xff)

def drawPath(image, trialframe):
	smoothImage = copy(image)
	simpleImage = copy(image)
	draw = ImageDraw.Draw(image)
	drawSmooth = ImageDraw.Draw(smoothImage)
	drawSimple = ImageDraw.Draw(simpleImage)
	Game = game.Game(None)
	Game.trial_def(trialframe)
	sp = Game.search.behavoir.starpath

	for parent in sp.paths:
		path = parent.simplePath.points
		for point in range(len(path)-1):
			start = path[point]
			next = path[point+1]
			draw.line((start.getXY(), next.getXY()), fill=COLOR_SIMPLE)
			drawSimple.line((start.getXY(), next.getXY()), fill=COLOR_SIMPLE)
		path = parent.smoothPath.points
		for point in range(len(path)-1):
			start = path[point]
			next = path[point+1]
			draw.line((start.getXY(), next.getXY()), fill=COLOR_SMOOTH)
			drawSmooth.line((start.getXY(), next.getXY()), fill=COLOR_SMOOTH)

	del draw
	del drawSmooth
	del drawSimple
	return (image, simpleImage, smoothImage)
	"""
	draw = ImageDraw.Draw(image)
	draw.line((0, 0) + image.size, fill=128)
	draw.line((0, image.size[1], image.size[0], 0), fill=(0xff,0xff,0xff,0xff))
	del draw
	"""

if __name__ == "__main__":
	for i in range(12):
		image = Image.open("paths/trialPNG(%d).png" % (i))
		with open("paths/trialFRAME(%d).txt" % (i), "r") as f:
			frame = json.loads(f.read())
		image, simpleImage, smoothImage = drawPath(image,frame)
		image.save("paths/trialDRAW(%d).png" % (i))
		simpleImage.save("paths/trialSIMPLE(%d).png" % (i))
		smoothImage.save("paths/trialSMOOTH(%d).png" % (i))