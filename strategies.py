def linear_decay(weight, inc):
	return lambda depth : weight - (depth-1)*inc

def poly_decay(weight, inc):
	return lambda depth: weight - (depth-1)**inc

def self_function():
	return int("inf")


#Strategies:
strat_one = {
	'food_function' : linear_decay(-10, 2),
	'enemy_function' : linear_decay(10,-2),
	'self_function' : self_function
}