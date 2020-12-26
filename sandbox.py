import random

def main():
    random.seed(3)
    print(random.randint(1,1000))
    random.seed(244)
    print(random.randint(1,1000))


if __name__ == '__main__':
    main()
