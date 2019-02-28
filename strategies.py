def curry(func):
    f_args = []
    f_kwargs = {}
    def f(*args, **kwargs):
        nonlocal f_args, f_kwargs
        if args or kwargs:
            f_args += args
            f_kwargs.update(kwargs)
            return f
        else:
            return func(*f_args, *f_kwargs)
    return f

def linear_decay(weight, inc):
	return lambda depth : weight - (depth-1)*inc

#def square_decay(weight, inc):

def self_function:
	return int("inf")

test = curry(linear_decay)
print test(1)(50)(-5)


#Strategies:
strat_one = {
	'food_function' : linear_decay(-10, 2),
	'enemy_function' : linear_decay(10,-2),
	'self_function' : self_function
}