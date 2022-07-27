def f():
    print('hello')

    def d():
        print('d')
    return(d)


c = f()

c()
