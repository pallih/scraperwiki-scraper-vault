from urllib2 import urlopen

SAMPLE_CELL = 'S4268|S4268|A7859|S4268A |S4268|A7859|S4268A |S4268|A7859|S4268A |S4268|A7859|S4268A'

def remove_duplicates(cell):
    "Take the initial cell blob with duplicates. Remove the duplicates. This doesn't work."
    unique = ''
    cell = cell.strip()
    for letter in cell[::-1]:
        if letter == ' ':
            i = -len(unique)
            if unique == cell[i:]:
                cell = cell[:i].strip()
        else:
            unique = letter + unique
        

remove_duplicates(SAMPLE_CELL)