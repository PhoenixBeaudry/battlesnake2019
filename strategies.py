#return a function that linearly increments the weight
def linear_decay(weight, inc):
	return lambda depth : weight + inc

#return a function that increments the weight polynomially
def poly_decay(weight, poly, sign=1):
    return lambda depth: weight + (-1*sign)poly**depth

def self_function():
	return 1000000

#Strategies:
strat_one = {
	'food_function' : poly_decay(-10000, 3, -1),
	'enemy_function' : poly_decay(10000, 3),
	'self_function' : self_function
}