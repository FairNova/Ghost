
global bob;

class Person:
    def __init__(self, name):
        self.name = name


bob = Person('Bob')
bob.name  # 'Bob'
alice = Person('Alice')
alice.name  # 'Alice'

def main():

    print( bob.name )
    return bob.name;
