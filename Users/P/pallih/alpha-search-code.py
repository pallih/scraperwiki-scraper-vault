import string

parts = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
last = ['']

alphabet = string.ascii_lowercase 
digits = string.digits
punctuation = string.punctuation

def succ(word=''):
    ''' Takes a string, and returns the next successive value. '''
    
    parts = [string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation]
    last = ['']
    

    # if none of the characters are in 'A-Z', 'a-z', or '0-9',
    #   then also include symbols
    if not any(ch for ch in word for part in parts if ch in part):
        parts = [string.printable[
            string.printable.index('!'):string.printable.index(' ')+1]]
        
    for index, ch in enumerate(word[::-1]):
        for part in parts:
            if ch in part:
                last = part
                ndx = part.index(ch)+1
                complete = True
                # if there's not an overflow (9+1=overflow),
                #    immediately return
                if ndx >= len(part):
                    complete = False
                    ndx = 0
                word = word[:(index+1)*-1]+part[ndx]+word[len(word)-index:]
                if complete:
                    return word
    return last[0] + word

if __name__ == '__main__':
    assert succ("abcd") == 'abce'
    assert succ("THX1138") == 'THX1139'
    assert succ("<<koala>>") == '<<koalb>>'
    assert succ("1999zzz") == '2000aaa'
    assert succ("ZZZ9999") == 'AAAA0000'
    assert succ("***") == "**+"


count = 1
a = 'a'
#while (a != 'aaaa'):
#    a = succ(a)
#    print a, count
#    count = count +1

alpha = string.lowercase
#alpha = ['a','b','c']
#alpha = list(string.ascii_lowercase) + list(string.digits)
alpha = list(string.ascii_lowercase)
#print alpha

def generator(choices, length):
    for a in choices:
        if length > 1:
            for g in generator(choices, length-1):
                yield a + g
        else:
            yield a


#print punctuation
two = []
for a in generator(alpha, 2):
     two.append( a)
print two



