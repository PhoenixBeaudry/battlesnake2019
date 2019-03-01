def linear_decay(weight, inc):
	return lambda depth : (weight - depth*inc) if (weight - depth*inc) > 0 else 0

#return a function that increments the weight polynomially
def poly_decay(weight, poly):
	if weight>0:
		return lambda depth: (weight - depth**poly) if (weight - depth**poly) > 0 else 0
	else:
		return lambda depth: (weight + depth**poly) if (weight + depth**poly) < 0 else 0


# Enemy decay function that allows conjoining segments and edges
# into enemy to be 100000 etc, while still having weighted polynomial
# decay in radius around segments
def enemy_decay(depth, weight=100, poly=3):
	if depth == 0:
		return 100000
	else:
		return poly_decay(weight, poly)(depth)

def self_function(depth):
	return 1000000

def const_zero(depth):
	return 0

#Strategies:
hungry = {
	'food_function' : poly_decay(-200, 3),
	'enemy_function' : enemy_decay,
	'self_function' : self_function
}

nothungry = {
	'food_function' : poly_decay(100, 3),
	'enemy_function' : enemy_decay,
	'self_function' : self_function
}