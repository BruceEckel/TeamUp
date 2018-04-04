import random

def test_random_shuffle_reproduceability(capsys):
    length = 100
    random.seed(47)
    list1 = random.sample(list(range(length)), length)
    random.seed(47)
    list2 = random.sample(list(range(length)), length)
    assert list1 == list2
    random.seed(48)
    list3 = random.sample(list(range(length)), length)
    assert list3 != list1
    # with capsys.disabled():
    #     print(list1)
    #     print(list3)