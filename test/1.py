from time import perf_counter


class A:

    def __init__(self):
        self.end = False
        self.del_ = False

    def __iter__(self):
        self.n = range(20)
        self.num = 0
        return self

    def __next__(self):
        self.num += 1
        if self.num == 20:
            self.end = True
            if self.del_:
                return
            raise StopIteration
        return self.n[self.num]

    def __del__(self):
        self.del_ = True
        if not self.end:
            while not self.end:
                self.__next__()


def b(a):
    for i in a:
        if i == 10:
            break


time1 = perf_counter()
b(A())
print(perf_counter() - time1)
