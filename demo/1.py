# coding=utf-8
def geta():
    getbasic = lambda: ('+ ',) + ('- ',) * 4
    return getbasic() * 4 + ('+', '\n')


def getb():
    getbasic = lambda: ('|',) + (' ',) * 9
    return getbasic() * 4 + ('|', '\n')


def getbasic():
    return geta() + getb() * 4

print ''.join(getbasic() * 4 + geta())
