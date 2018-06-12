from .tests_db import get_irr, get_sentence
from numpy import arange, random, delete, zeros
from random import shuffle


# Choice 'num' random numbers from 'numb'
def un_numbers(numb, num):
    n = zeros(num)
    for i in range(num):
        j = 0
        while j < num:
            flag = True
            n[i] = random.choice(numb, 1)
            for k in range(0, i - 1):
                if n[i] == n[k]:
                    flag = False
            if flag:
                j += 1
    return n

# Get text with specific verbs
def get_text(verbs, numreg):
    result = []
    new_verbs = []
    for verb in verbs:
        sentence, verbs_array = get_sentence(False, verb)
        result.append(sentence)
        new_verbs.append(verbs_array)
    for i in range(numreg):
        result.append(get_sentence(True, ''))
    shuffle(result)
    return result, new_verbs

def test_ir(oft, num):
    verbs = get_irr(oft)
    numbers = arange(len(verbs))
    delnum = un_numbers(numbers, len(verbs) - num)
    numbers = delete(numbers, delnum)
    random.shuffle(numbers)
    result = []
    for i in range(num):
        result.append(verbs[numbers[i]])
    return result
