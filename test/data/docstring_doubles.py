
"""
Double quotes multiline module docstring
"""

"""
this is not a docstring
"""

l = []

class Cls:
    """
    Double quotes multiline class docstring
    """

    """
    this is not a docstring
    """

    # The colon in the list indexing below is an edge case for the docstring scanner
    def f(self, val=l[Cls():3]):
        """
        Double quotes multiline function docstring
        """

        some_expression = 'hello world'

        """
        this is not a docstring
        """
