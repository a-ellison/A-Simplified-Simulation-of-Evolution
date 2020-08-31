import helper_functions


def main():
    x, y = 2, 10
    x, y = helper_functions.get_new_position(x, y, 720, 10)
    print(x, y)


if __name__ == '__main__':
    main()
