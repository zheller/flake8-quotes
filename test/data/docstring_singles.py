
'''
Single quotes multiline module docstring
'''

'''
this is not a docstring
'''

l = []

class Cls(MakeKlass('''
    class params \t not a docstring
''')):
    '''
    Single quotes multiline class docstring
    '''

    '''
    this is not a docstring
    '''

    # The colon in the list indexing below is an edge case for the docstring scanner
    def f(self, bar='''
        definitely not a docstring''',
        val=l[Cls():3]):
        '''
        Single quotes multiline function docstring
        '''

        some_expression = 'hello world'

        '''
        this is not a docstring
        '''

        if l:
            '''
            Looks like a docstring, but in reality it isn't - only modules, classes and functions
            '''
            pass


class SingleLinedDocstrings():
    ''' Single quotes single line class docstring '''

    def foo(self, bar='''not a docstring'''):
        ''' Single quotes single line function docstring'''

        a = 10
        ''' just string'''

        for i in range(a):
            ''' not a docstring'''
            if a < i:
                ''' also not a docstring '''
                pass

    class Nested(foo()[:]): ''' inline docstring '''; pass

def foo():
    '''function without params, single line docstring'''
    ''' not a docstring'''
    return

def foo2():
    '''
        function without params, multiline line docstring
    '''
    ''' not a docstring'''
    return
