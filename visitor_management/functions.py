import re

def split_post(string):
    """
    Split a string into two parts based on the semi-colon (;) character. The first part is assumed to be the name and the second part is assumed to be the ID.
    The name and ID are stripped of leading and trailing whitespace and returned as a tuple.

    :param string: The string to split
    :type string: str
    :return: A tuple containing the name and ID
    :rtype: tuple (str, str)
    """
    name_id = string

    # Split the string into a list of two elements, separated by the semi-colon character
    ni = name_id.split(';')

    # Extract the name and ID from the list, stripping leading and trailing whitespace
    my_name = ni[0].strip()
    my_id = ni[1].strip()

    # Return the name and ID as a tuple
    return my_name, my_id #  my_pk,
