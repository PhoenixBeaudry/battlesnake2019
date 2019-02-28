def linear_decay(weight, inc):
	return lambda depth : weight - (depth-1)*inc

def poly_decay(weight, inc):
	return lambda depth: weight - (depth-1)**inc

def self_function():
	return 1000000


#Strategies:
strat_one = {
	'food_function' : poly_decay(-10000, 3),
	'enemy_function' : poly_decay(10000, 3),
	'self_function' : self_function
}