import clutter

def clamp(x, min=0, max=1):
	if x>max: return max
	elif x<min: return min
	else: return x

def clamp_angle(x):
	if x<0: x+=360
	if x>360: x-=360
	return x

class AbstractMethodNotImplemented(Exception): pass



