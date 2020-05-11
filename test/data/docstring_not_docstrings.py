
var0 = True
l = []

if var0:
    """ not a  docstring"""
    pass

while(var0 < 0 or "def" in l[:] ):
    """ also not a docstring """
    with open(l["def":]) as f:
        """ not a docstring """
        pass

if var0 < 10:
    """
        not a multiline docstring
    """
    pass


if var0:
    ''' not a  docstring'''
    pass

while(var0 < 0 or "def" in l[:] ):
    ''' also not a docstring '''
    with open(l["def":]) as f:
        ''' not a docstring '''
        pass

if var0 < 10:
    '''
        not a multiline docstring
    '''
    pass

# https://github.com/zheller/flake8-quotes/issues/97
def test():
    {}["a"]
