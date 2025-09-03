from random import shuffle
def randomizer(*ops):
    filtered_ops = [op for op in ops if op is not None]
    shuffle(filtered_ops)
    return filtered_ops