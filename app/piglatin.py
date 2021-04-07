# Authors: CS For Insight (Summer19 - JG)

import re

def substitute(old_text, dictionary_of_substitutions):
    """ substitution engine:
        old_text: the body of text in which to make substitutions
        dictionary_of_substitutions:
          a Python dictionary with
            keys ~ the strings to replace (get rid of)
            values ~ the strings to replace the keys with! 
    """
    # right now, we replace every letter 'e' with the letter 'E'
    string_to_replace = 'e'
    replacement = 'E'
    # use re.sub
    new_text = re.sub( string_to_replace, replacement, old_text )
    
    # return the result
    return new_text



# Function takes in a string, and returns on which has been 
# translated into pig latin
def pig_translate(S):
    """ pig latin converter from '19 """
    retStr = ''
    V = ['a','A','e','E','i','I','o','O','u','U']
    currFront = S[0]
    seen_vowel = False
    for i in range(len(S)):
        if S[i] == ' ':
            if currFront in V:
                retStr += 'yay '
            else:
                retStr += currFront.lower() + 'ay '
        elif i == len(S)-1:
            if currFront in V:
                retStr += S[i]+ 'yay'
            else:
                retStr += S[i] + currFront.lower() + 'ay'
        else:
            if S[i-1] == ' ' or i == 0:
                seen_vowel = False
                currFront = S[i]
                if currFront in V:
                    retStr += S[i]
                    seen_vowel = True
            else:
                if S[i] in V:
                    seen_vowel = True
                    retStr += S[i]
                else:
                    if not seen_vowel:
                        currFront += S[i]
                    else:
                        retStr += S[i]
    return retStr