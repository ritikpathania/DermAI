class level1:
    height = '7.5'
    weight = '80'


class level2(level1):
    def groot(self):
        print("access")


obj = level2()
print(obj.height)
obj.groot()

class level3(level2):
    def system(self):
        print("corrupt")

obj = level3()
obj.groot()
obj.system()
print(obj.height)
print(obj.weight)
