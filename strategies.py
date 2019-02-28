def linear_decay(weight, inc):
	return lambda depth : weight - (depth-1)*inc

def poly_decay(weight, inc, sign=1):
    if sign>0:
        return lambda depth: weight - (depth-1)**inc if (weight - sign*(depth-1)**inc) >= 0 else 0
    else:
        return lambda depth: weight + (depth-1)**inc if (weight + (depth-1)**inc) <= 0 else 0

def self_function():
	return 1000000


#Strategies:
strat_one = {
	'food_function' : poly_decay(-10000, 3, -1),
	'enemy_function' : poly_decay(10000, 3),
	'self_function' : self_function
}