def linear_decay(weight, inc):
	return lambda depth : weight - (depth-1)*inc

def poly_decay(weight, inc):
	return lambda depth: weight - (depth-1)**inc

def self_function():
	return 1000000


#Strategies:
strat_one = {
	'food_function' : linear_decay(-100, 10),
	'enemy_function' : linear_decay(100,-10),
	'self_function' : self_function
}