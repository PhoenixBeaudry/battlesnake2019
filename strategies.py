def linear_decay(weight, inc):
	return lambda depth : (weight - depth*inc) if (weight - depth*inc) > 0 else 0

#return a function that increments the weight polynomially
def poly_decay(weight, poly):
	if weight>0:
		return lambda depth: (weight - depth**poly) if (weight - depth**poly) > 0 else 0
	else:
		return lambda depth: (weight + depth**poly) if (weight + depth**poly) < 0 else 0

def self_function(depth):
	return 1000000

def const_zero(depth):
	return 0

#Strategies:
hungry = {
	'food_function' : poly_decay(-200, 3),
	'enemy_function' : poly_decay(100, 3),
	'self_function' : self_function
}

nothungry = {
	'food_function' : poly_decay(100, 3),
	'enemy_function' : poly_decay(100, 3),
	'self_function' : self_function
}