import scraperwiki

# Download Savegame
# The following will need to be decrypted locally and then have the individual files uploded:
# http://jacobjwalker.effectiveeducation.org/blog/wp-content/uploads/2013/05/data.bin


# Future Feature: Decrypting Savegame in Python
# Currently the Savegame decryption needs to occur locally, and then placed online someplace for the scraper
# Information at http://jansenprice.com/blog?id=9-Extracting-Data-from-Wii-Fit-Plus-Savegame-Files
# In the future, I might try porting Segher's Wii.git tools from C to Python, possibly using the following info to help with the porting
# http://pyinsci.blogspot.com/2010/03/converting-c-code-to-python.html


# Parsing Decrypted Savegame
# Based upon code from http://wiifit.googlecode.com/svn/trunk/wiifitparser.py
# Originally created by freeall and mathiasbuus, with additions by huanix, and now me (Jacob J. Walker)

import sys
class PairKeyDict(dict):
    # Super slow way to do a check for the single key. BUT it works :-)
    def __getitem__(self, single_key):
        for pair_key, value in super(PairKeyDict, self).iteritems():
            if single_key in pair_key:
                return value
        raise KeyError
    
    # A nice way to actually, still use the keys as a map
    def other_key(self, single_key):
        for k1, k2 in super(PairKeyDict, self).iterkeys():
            if single_key == k1:
                return k2
            if single_key == k2:
                return k1
        return None        
        
class Shared:
    MAP = PairKeyDict({
        # This map represents where the games are located in the memory
        # For the stars and points the address is relative to the players block
        # address.
        # For highscore, the address is absolute to the RPWiiFit.dat file
        
        # (index, name) : (highscore, stars, points)
        (0, "") : (0x0, 0x0, 0x0),
        (1, "") : (0x0, 0x0, 0x0),
        (2, "") : (0x0, 0x0, 0x0),
        (3, "TABLE TILT") : (0x0, 0x0, 0x0),
        (4, "") : (0x0, 0x0, 0x0),
        (5, "") : (0x0, 0x0, 0x0),
        (6, "") : (0x0, 0x0, 0x0),
        (7, "") : (0x0, 0x0, 0x0),
        (8, "") : (0x0, 0x0, 0x0),
        (9, "SINGLE LEG EXTENSION") : (0x0, 0x0, 0x0),
        (10, "") : (0x0, 0x0, 0x0),
        (11, "") : (0x0, 0x0, 0x0),
        (12, "") : (0x0, 0x0, 0x0),
        (13, "") : (0x0, 0x0, 0x0),
        (14, "") : (0x0, 0x0, 0x0),
        (15, "PRESS-UP AND SIDE STAND") : (0x0, 0x0, 0x0),
        (16, "") : (0x0, 0x0, 0x0),
        (17, "") : (0x0, 0x0, 0x0),
        (18, "") : (0x0, 0x0, 0x0),
        (19, "") : (0x0, 0x0, 0x0),
        (20, "") : (0x0, 0x0, 0x0),
        (21, "") : (0x0, 0x0, 0x0),
        (22, "") : (0x0, 0x0, 0x0),
        (23, "") : (0x0, 0x0, 0x0),
        (24, "DEEP BREATHING") : (0x4AA90, 0x360F, 0x377C),
        (25, "HALF-MOON") : (0x4AB80, 0x3612, 0x3788),
        (26, "WARRIOR") : (0x4AC70, 0x3615, 0x3794),
        (27, "TREE") : (0x0, 0x0, 0x0),
        (28, "") : (0x0, 0x0, 0x0),
        (29, "") : (0x0, 0x0, 0x0),
        (30, "") : (0x0, 0x0, 0x0),
        (31, "") : (0x0, 0x0, 0x0),
        (32, "") : (0x0, 0x0, 0x0),
        (33, "") : (0x0, 0x0, 0x0),
        (34, "") : (0x0, 0x0, 0x0),
        (35, "") : (0x0, 0x0, 0x0),
        (36, "") : (0x0, 0x0, 0x0),
        (37, "") : (0x0, 0x0, 0x0),
        (38, "") : (0x0, 0x0, 0x0),
        (39, "HULLA HOOP") : (0x0, 0x0, 0x0),
        (40, "STEPS BASICS") : (0x0, 0x0, 0x0),
        (41, "") : (0x0, 0x0, 0x0),
        (42, "") : (0x0, 0x0, 0x0),
        (43, "") : (0x0, 0x0, 0x0),
        (44, "") : (0x0, 0x0, 0x0),
        (45, "") : (0x0, 0x0, 0x0),
        (46, "") : (0x0, 0x0, 0x0),
        (47, "") : (0x0, 0x0, 0x0)})
    
    @staticmethod    
    def game_name(game_index):
        def beautify_str(s):
            res = s[0] if s != None and len(s) > 0 else ""
            for i in range(1, len(s)):
                if s[i-1] in (" ", "-"):
                    res += s[i].upper()
                else:
                    res += s[i].lower()
            return res
        return beautify_str(Shared.MAP.other_key(game_index))
    
class Util:
    @staticmethod
    def convert_date_bytes(date_bytes):
        def add_leading_chars(stringg, char, length):
            return char*(length - len(stringg)) + stringg

        # Convert hex to binary (and add leading 0's)
        bin0 = add_leading_chars(bin(ord(date_bytes[0]))[2:], "0", 8)
        bin1 = add_leading_chars(bin(ord(date_bytes[1]))[2:], "0", 8)
        bin2 = add_leading_chars(bin(ord(date_bytes[2]))[2:], "0", 8)
        bin3 = add_leading_chars(bin(ord(date_bytes[3]))[2:], "0", 8)
        bin_date = bin0 + bin1 + bin2 + bin3

        year = int(bin_date[0:12], 2)
        month = int(bin_date[12:16], 2)
        day = int(bin_date[16:21], 2)
        hours = int(bin_date[21:26], 2)
        minutes = int(bin_date[26:32], 2)
        
        return (year, month, day, hours, minutes)

    @staticmethod
    def hex_combine(bytes):
        res = ""
        for b in bytes:
            res += hex(ord(b))[2:]
        return res
        
class Player:
    def __init__(self, data):
        self.data = data
        name = self.data[:20]
        if ord(name[0]) == 0 and ord(name[1]) == 0:
            raise Exception()
        
    def level_table(self):
        data = self.data[0x87:0x267]
        res = []
        for i in range(0,48):
            block = data[10*i:10*(i+1)]
            locked = True if ord(block[0]) == 0 else False
            last_played_level = ord(block[5])
            date = Util.convert_date_bytes(block[6:10])
        
            res.append((locked, last_played_level, date))
        return res
        
    def play_table(self):
        data = self.data[0x267:]
        
        res=[]
        
        i=0
        while ord(data[i*12]) != 0:
            day_data = data[i*12 : (i+1)*12]

            date = Util.hex_combine(day_data[0x0:0x0+2])
            balance_time = int(Util.hex_combine(day_data[0x2:0x2+2]), 16)
            workout_time = int(Util.hex_combine(day_data[0x4:0x4+2]), 16)
            yoga_time = int(Util.hex_combine(day_data[0x6:0x6+2]), 16)
            aerobic_time = int(Util.hex_combine(day_data[0x8:0x8+2]), 16)

            res.append((date, balance_time, workout_time, yoga_time, aerobic_time))
            i+=1
        
        return res
    
    def last_played(self):
        return self.data[0x36:0x36+2]

    def name(self):
        name = self.data[:20]
        res = ""
        for c in name:
            if ord(c) != 0: res += c
        return res

    def height(self):
        return ord(self.data[0x17])
        
    def birthday(self):
        year = int(hex(ord(self.data[0x18]))[2:] + hex(ord(self.data[0x19]))[2:])
        month = int(hex(ord(self.data[0x1A]))[2:])
        day = int(hex(ord(self.data[0x1B]))[2:])
        return (year, month, day)
        
    def totalplayed(self):
        return self.data[0x26D]

    def id(self):
        return Util.hex_combine(self.data[0x2D:0x31])

    def stars(self, game):
        return ord(self.data[Shared.MAP[game.upper()][1]])

    def points(self, game):
        return ord(self.data[Shared.MAP[game.upper()][2]])
    
    def bodytests(self):
        bt_start = 0x3899
        res=[]

        test_nr=0
        while True:
            test_nr += 1
      
            # break after we read 1096 bodytests, since 
            # there is no more space/data for this player
            if test_nr > 1096:
              break
         
            bodytest = self.data[bt_start + 21*(test_nr-1):bt_start + 21*test_nr]
        
            if ord(bodytest[0]) == 0:
                break
            date = Util.convert_date_bytes(bodytest[0:4])

            kg = bodytest[0x4:0x4+2]
            kg = int(hex(ord(kg[0]))[2:] + hex(ord(kg[1]))[2:], 16)
            kg = float(kg) /10
      
            bmi = bodytest[0x6:0x6+2]
            bmi = float("%s.%s"%(ord(bmi[0]), ord(bmi[1])))
        
            right_bal = bodytest[0x8:0x8+2]
            right_bal = int(hex(ord(right_bal[0]))[2:] + hex(ord(right_bal[1]))[2:], 16) / 10.0
            left_bal = 100.0 - right_bal
        
            wii_fit_age = ord(bodytest[0xE])
            
            res.append((date, bmi, kg, right_bal, left_bal, wii_fit_age))
        
        return res

class WiiFitParser:        
    def __init__(self, filename):
        self._f = open(filename, "r")
        self._players = {}
        # generate player_id -> player_name dictionary
        for i in range(0,8):
            try:
                p = self.player(i)
                self._players[p.id()] = p.name()
            except:
                pass

    def _raw_data(self, nr):
        self._f.seek(0x8 + 0x9281 * nr)
        return self._f.read(0x9281)
        
    def player(self, nr):
        try:
            p = Player(self._raw_data(nr))
            return p
        except:
            return None
            
    def highscore(self, game):
        self._f.seek(Shared.MAP[game.upper()][0])
        res = []

        if Shared.MAP[game.upper()] == (0x0, 0x0, 0x0):
            return res
        
        for s in range(0,11):
            # ID
            pid = self._f.read(0x4)
            
            if ord(pid[0]) == 0:
                continue
                
            # bytes -> hex-string
            pid = Util.hex_combine(pid)
            
            # read 0s
            self._f.read(0x3)
            
            score = ord(self._f.read(0x1))

            print game, pid, score
            print self._players
            res.append((self._players[pid], score))
        return res


from xml.dom.minidom import getDOMImplementation
class Printer:
    def body_tests(self, player):
        res = self.new_node("bodytests")
        
        bodytests = player.bodytests()
        for bodytest in bodytests:
            date, bmi, kg, right_bal, left_bal, wii_fit_age = bodytest
            year, month, day, hours, minutes = date
            
            node = self.new_node("bodytest")
            node.setAttribute("date", "%4i-%02i-%02i %02i:%02i"%(year, month, day, hours, minutes))
            node.setAttribute("bmi", str(bmi))
            node.setAttribute("kg", str(kg))
            node.setAttribute("right_balance", str(right_bal))
            node.setAttribute("left_balance", str(left_bal))
            node.setAttribute("wii_fit_age", str(wii_fit_age))
            res.appendChild(node)
        
        return res
    
    def level_tables(self, player, level_table):
        res = self.new_node("leveltable")
        
        for i in range(0,48):
            locked, last_played_level, date = level_table[i]

            if last_played_level == 0:
                continue
                
            year, month, day, hours, minutes = date
            name = Shared.game_name(i)
            points = player.points(name)
            stars = player.stars(name)

            node = self.new_node("game")
            node.setAttribute("id", str(i))
            node.setAttribute("name", name)
            node.setAttribute("last_played_level", str(last_played_level))
            node.setAttribute("stars", str(stars))
            node.setAttribute("points", str(points))
            node.setAttribute("date", "%i-%02i-%02i %02i:%02i"%(year, month, day, hours, minutes))
            res.appendChild(node)
        
        return res

    def play_tables(self, play_table):
        total_played = 0
        last_day_played = 0
        
        res = self.new_node("playtables")
        
        for play in play_table:
            date, balance_time, workout_time, yoga_time, aerobic_time = play

            last_day_played=balance_time + workout_time + yoga_time + aerobic_time
            total_played += balance_time + workout_time + yoga_time + aerobic_time
            node = self.new_node("playtable")
            node.setAttribute("date", str(date))
            node.setAttribute("balance_time", str(balance_time))
            node.setAttribute("workout_time", str(workout_time))
            node.setAttribute("yoga_time", str(yoga_time))
            node.setAttribute("aerobic_time", str(aerobic_time))
            res.appendChild(node)
            
        return res
        
    def played_info(self, play_table):
        total_played = 0
        last_day_played = 0
        
        for play in play_table:
            date, balance_time, workout_time, yoga_time, aerobic_time = play

            last_day_played=balance_time + workout_time + yoga_time + aerobic_time
            total_played += balance_time + workout_time + yoga_time + aerobic_time

        return (total_played, last_day_played)
    
    def new_node(self, name):
        return self._doc.createElement(name)
        
    def add_node(self, node):
        self._topnode.appendChild(node)
        
    def print_player(self, player):
        name = player.name()
        height = player.height()
        birthday = player.birthday()
        pid = player.id()
        last_played = player.last_played()
        last_played = hex(ord(last_played[0]))[2:] + hex(ord(last_played[1]))[2:]
        year, month, day = birthday
        
        if name == "":
            return

        total_played, last_day_played = self.played_info(player.play_table())
        node = self.new_node("player")
        node.setAttribute("name", name)
        node.setAttribute("height", str(height))
        node.setAttribute("birthday", "%i-%02i-%02i"%(year, month, day))
        node.setAttribute("id", pid)
        node.setAttribute("last_played", last_played)
        node.setAttribute("last_day_played", str(last_day_played))
        node.setAttribute("total_played", str(total_played))


        node.appendChild(self.body_tests(player))
        node.appendChild(self.level_tables(player, player.level_table()))
        node.appendChild(self.play_tables(player.play_table()))

        self.add_node(node)
            
    def print_highscore_table(self, parser):
        res = self.new_node("highscores")
        for i, name in Shared.MAP.iterkeys():
            if name == "":
                continue
                
            node = self.new_node("highscore")
            node.setAttribute("name", Shared.game_name(i))
            for pname, score in parser.highscore(name):
                n = self.new_node("score")
                n.setAttribute("score", str(score))
                n.setAttribute("player_name", str(pname))
                node.appendChild(n)
            res.appendChild(node)
            
        self.add_node(res)


    def __init__(self):
        self._xml = getDOMImplementation()
        self._doc = self._xml.createDocument(None, "wiifit", None)
        self._topnode = self._doc.documentElement
    
    def printout(self):
        print self._doc.toprettyxml()

if len(sys.argv) == 1:
    print "Run as ./wiifitparser.py somewhere/over/the/rainbow/RPWiiFit.dat"
    sys.exit()

parser = WiiFitParser(sys.argv[1])
printer = Printer()

for i in range(0,8):
    p = parser.player(i)
    if p != None:
        printer.print_player(p)

printer.print_highscore_table(parser)
printer.printout()


import scraperwiki

# Download Savegame
# The following will need to be decrypted locally and then have the individual files uploded:
# http://jacobjwalker.effectiveeducation.org/blog/wp-content/uploads/2013/05/data.bin


# Future Feature: Decrypting Savegame in Python
# Currently the Savegame decryption needs to occur locally, and then placed online someplace for the scraper
# Information at http://jansenprice.com/blog?id=9-Extracting-Data-from-Wii-Fit-Plus-Savegame-Files
# In the future, I might try porting Segher's Wii.git tools from C to Python, possibly using the following info to help with the porting
# http://pyinsci.blogspot.com/2010/03/converting-c-code-to-python.html


# Parsing Decrypted Savegame
# Based upon code from http://wiifit.googlecode.com/svn/trunk/wiifitparser.py
# Originally created by freeall and mathiasbuus, with additions by huanix, and now me (Jacob J. Walker)

import sys
class PairKeyDict(dict):
    # Super slow way to do a check for the single key. BUT it works :-)
    def __getitem__(self, single_key):
        for pair_key, value in super(PairKeyDict, self).iteritems():
            if single_key in pair_key:
                return value
        raise KeyError
    
    # A nice way to actually, still use the keys as a map
    def other_key(self, single_key):
        for k1, k2 in super(PairKeyDict, self).iterkeys():
            if single_key == k1:
                return k2
            if single_key == k2:
                return k1
        return None        
        
class Shared:
    MAP = PairKeyDict({
        # This map represents where the games are located in the memory
        # For the stars and points the address is relative to the players block
        # address.
        # For highscore, the address is absolute to the RPWiiFit.dat file
        
        # (index, name) : (highscore, stars, points)
        (0, "") : (0x0, 0x0, 0x0),
        (1, "") : (0x0, 0x0, 0x0),
        (2, "") : (0x0, 0x0, 0x0),
        (3, "TABLE TILT") : (0x0, 0x0, 0x0),
        (4, "") : (0x0, 0x0, 0x0),
        (5, "") : (0x0, 0x0, 0x0),
        (6, "") : (0x0, 0x0, 0x0),
        (7, "") : (0x0, 0x0, 0x0),
        (8, "") : (0x0, 0x0, 0x0),
        (9, "SINGLE LEG EXTENSION") : (0x0, 0x0, 0x0),
        (10, "") : (0x0, 0x0, 0x0),
        (11, "") : (0x0, 0x0, 0x0),
        (12, "") : (0x0, 0x0, 0x0),
        (13, "") : (0x0, 0x0, 0x0),
        (14, "") : (0x0, 0x0, 0x0),
        (15, "PRESS-UP AND SIDE STAND") : (0x0, 0x0, 0x0),
        (16, "") : (0x0, 0x0, 0x0),
        (17, "") : (0x0, 0x0, 0x0),
        (18, "") : (0x0, 0x0, 0x0),
        (19, "") : (0x0, 0x0, 0x0),
        (20, "") : (0x0, 0x0, 0x0),
        (21, "") : (0x0, 0x0, 0x0),
        (22, "") : (0x0, 0x0, 0x0),
        (23, "") : (0x0, 0x0, 0x0),
        (24, "DEEP BREATHING") : (0x4AA90, 0x360F, 0x377C),
        (25, "HALF-MOON") : (0x4AB80, 0x3612, 0x3788),
        (26, "WARRIOR") : (0x4AC70, 0x3615, 0x3794),
        (27, "TREE") : (0x0, 0x0, 0x0),
        (28, "") : (0x0, 0x0, 0x0),
        (29, "") : (0x0, 0x0, 0x0),
        (30, "") : (0x0, 0x0, 0x0),
        (31, "") : (0x0, 0x0, 0x0),
        (32, "") : (0x0, 0x0, 0x0),
        (33, "") : (0x0, 0x0, 0x0),
        (34, "") : (0x0, 0x0, 0x0),
        (35, "") : (0x0, 0x0, 0x0),
        (36, "") : (0x0, 0x0, 0x0),
        (37, "") : (0x0, 0x0, 0x0),
        (38, "") : (0x0, 0x0, 0x0),
        (39, "HULLA HOOP") : (0x0, 0x0, 0x0),
        (40, "STEPS BASICS") : (0x0, 0x0, 0x0),
        (41, "") : (0x0, 0x0, 0x0),
        (42, "") : (0x0, 0x0, 0x0),
        (43, "") : (0x0, 0x0, 0x0),
        (44, "") : (0x0, 0x0, 0x0),
        (45, "") : (0x0, 0x0, 0x0),
        (46, "") : (0x0, 0x0, 0x0),
        (47, "") : (0x0, 0x0, 0x0)})
    
    @staticmethod    
    def game_name(game_index):
        def beautify_str(s):
            res = s[0] if s != None and len(s) > 0 else ""
            for i in range(1, len(s)):
                if s[i-1] in (" ", "-"):
                    res += s[i].upper()
                else:
                    res += s[i].lower()
            return res
        return beautify_str(Shared.MAP.other_key(game_index))
    
class Util:
    @staticmethod
    def convert_date_bytes(date_bytes):
        def add_leading_chars(stringg, char, length):
            return char*(length - len(stringg)) + stringg

        # Convert hex to binary (and add leading 0's)
        bin0 = add_leading_chars(bin(ord(date_bytes[0]))[2:], "0", 8)
        bin1 = add_leading_chars(bin(ord(date_bytes[1]))[2:], "0", 8)
        bin2 = add_leading_chars(bin(ord(date_bytes[2]))[2:], "0", 8)
        bin3 = add_leading_chars(bin(ord(date_bytes[3]))[2:], "0", 8)
        bin_date = bin0 + bin1 + bin2 + bin3

        year = int(bin_date[0:12], 2)
        month = int(bin_date[12:16], 2)
        day = int(bin_date[16:21], 2)
        hours = int(bin_date[21:26], 2)
        minutes = int(bin_date[26:32], 2)
        
        return (year, month, day, hours, minutes)

    @staticmethod
    def hex_combine(bytes):
        res = ""
        for b in bytes:
            res += hex(ord(b))[2:]
        return res
        
class Player:
    def __init__(self, data):
        self.data = data
        name = self.data[:20]
        if ord(name[0]) == 0 and ord(name[1]) == 0:
            raise Exception()
        
    def level_table(self):
        data = self.data[0x87:0x267]
        res = []
        for i in range(0,48):
            block = data[10*i:10*(i+1)]
            locked = True if ord(block[0]) == 0 else False
            last_played_level = ord(block[5])
            date = Util.convert_date_bytes(block[6:10])
        
            res.append((locked, last_played_level, date))
        return res
        
    def play_table(self):
        data = self.data[0x267:]
        
        res=[]
        
        i=0
        while ord(data[i*12]) != 0:
            day_data = data[i*12 : (i+1)*12]

            date = Util.hex_combine(day_data[0x0:0x0+2])
            balance_time = int(Util.hex_combine(day_data[0x2:0x2+2]), 16)
            workout_time = int(Util.hex_combine(day_data[0x4:0x4+2]), 16)
            yoga_time = int(Util.hex_combine(day_data[0x6:0x6+2]), 16)
            aerobic_time = int(Util.hex_combine(day_data[0x8:0x8+2]), 16)

            res.append((date, balance_time, workout_time, yoga_time, aerobic_time))
            i+=1
        
        return res
    
    def last_played(self):
        return self.data[0x36:0x36+2]

    def name(self):
        name = self.data[:20]
        res = ""
        for c in name:
            if ord(c) != 0: res += c
        return res

    def height(self):
        return ord(self.data[0x17])
        
    def birthday(self):
        year = int(hex(ord(self.data[0x18]))[2:] + hex(ord(self.data[0x19]))[2:])
        month = int(hex(ord(self.data[0x1A]))[2:])
        day = int(hex(ord(self.data[0x1B]))[2:])
        return (year, month, day)
        
    def totalplayed(self):
        return self.data[0x26D]

    def id(self):
        return Util.hex_combine(self.data[0x2D:0x31])

    def stars(self, game):
        return ord(self.data[Shared.MAP[game.upper()][1]])

    def points(self, game):
        return ord(self.data[Shared.MAP[game.upper()][2]])
    
    def bodytests(self):
        bt_start = 0x3899
        res=[]

        test_nr=0
        while True:
            test_nr += 1
      
            # break after we read 1096 bodytests, since 
            # there is no more space/data for this player
            if test_nr > 1096:
              break
         
            bodytest = self.data[bt_start + 21*(test_nr-1):bt_start + 21*test_nr]
        
            if ord(bodytest[0]) == 0:
                break
            date = Util.convert_date_bytes(bodytest[0:4])

            kg = bodytest[0x4:0x4+2]
            kg = int(hex(ord(kg[0]))[2:] + hex(ord(kg[1]))[2:], 16)
            kg = float(kg) /10
      
            bmi = bodytest[0x6:0x6+2]
            bmi = float("%s.%s"%(ord(bmi[0]), ord(bmi[1])))
        
            right_bal = bodytest[0x8:0x8+2]
            right_bal = int(hex(ord(right_bal[0]))[2:] + hex(ord(right_bal[1]))[2:], 16) / 10.0
            left_bal = 100.0 - right_bal
        
            wii_fit_age = ord(bodytest[0xE])
            
            res.append((date, bmi, kg, right_bal, left_bal, wii_fit_age))
        
        return res

class WiiFitParser:        
    def __init__(self, filename):
        self._f = open(filename, "r")
        self._players = {}
        # generate player_id -> player_name dictionary
        for i in range(0,8):
            try:
                p = self.player(i)
                self._players[p.id()] = p.name()
            except:
                pass

    def _raw_data(self, nr):
        self._f.seek(0x8 + 0x9281 * nr)
        return self._f.read(0x9281)
        
    def player(self, nr):
        try:
            p = Player(self._raw_data(nr))
            return p
        except:
            return None
            
    def highscore(self, game):
        self._f.seek(Shared.MAP[game.upper()][0])
        res = []

        if Shared.MAP[game.upper()] == (0x0, 0x0, 0x0):
            return res
        
        for s in range(0,11):
            # ID
            pid = self._f.read(0x4)
            
            if ord(pid[0]) == 0:
                continue
                
            # bytes -> hex-string
            pid = Util.hex_combine(pid)
            
            # read 0s
            self._f.read(0x3)
            
            score = ord(self._f.read(0x1))

            print game, pid, score
            print self._players
            res.append((self._players[pid], score))
        return res


from xml.dom.minidom import getDOMImplementation
class Printer:
    def body_tests(self, player):
        res = self.new_node("bodytests")
        
        bodytests = player.bodytests()
        for bodytest in bodytests:
            date, bmi, kg, right_bal, left_bal, wii_fit_age = bodytest
            year, month, day, hours, minutes = date
            
            node = self.new_node("bodytest")
            node.setAttribute("date", "%4i-%02i-%02i %02i:%02i"%(year, month, day, hours, minutes))
            node.setAttribute("bmi", str(bmi))
            node.setAttribute("kg", str(kg))
            node.setAttribute("right_balance", str(right_bal))
            node.setAttribute("left_balance", str(left_bal))
            node.setAttribute("wii_fit_age", str(wii_fit_age))
            res.appendChild(node)
        
        return res
    
    def level_tables(self, player, level_table):
        res = self.new_node("leveltable")
        
        for i in range(0,48):
            locked, last_played_level, date = level_table[i]

            if last_played_level == 0:
                continue
                
            year, month, day, hours, minutes = date
            name = Shared.game_name(i)
            points = player.points(name)
            stars = player.stars(name)

            node = self.new_node("game")
            node.setAttribute("id", str(i))
            node.setAttribute("name", name)
            node.setAttribute("last_played_level", str(last_played_level))
            node.setAttribute("stars", str(stars))
            node.setAttribute("points", str(points))
            node.setAttribute("date", "%i-%02i-%02i %02i:%02i"%(year, month, day, hours, minutes))
            res.appendChild(node)
        
        return res

    def play_tables(self, play_table):
        total_played = 0
        last_day_played = 0
        
        res = self.new_node("playtables")
        
        for play in play_table:
            date, balance_time, workout_time, yoga_time, aerobic_time = play

            last_day_played=balance_time + workout_time + yoga_time + aerobic_time
            total_played += balance_time + workout_time + yoga_time + aerobic_time
            node = self.new_node("playtable")
            node.setAttribute("date", str(date))
            node.setAttribute("balance_time", str(balance_time))
            node.setAttribute("workout_time", str(workout_time))
            node.setAttribute("yoga_time", str(yoga_time))
            node.setAttribute("aerobic_time", str(aerobic_time))
            res.appendChild(node)
            
        return res
        
    def played_info(self, play_table):
        total_played = 0
        last_day_played = 0
        
        for play in play_table:
            date, balance_time, workout_time, yoga_time, aerobic_time = play

            last_day_played=balance_time + workout_time + yoga_time + aerobic_time
            total_played += balance_time + workout_time + yoga_time + aerobic_time

        return (total_played, last_day_played)
    
    def new_node(self, name):
        return self._doc.createElement(name)
        
    def add_node(self, node):
        self._topnode.appendChild(node)
        
    def print_player(self, player):
        name = player.name()
        height = player.height()
        birthday = player.birthday()
        pid = player.id()
        last_played = player.last_played()
        last_played = hex(ord(last_played[0]))[2:] + hex(ord(last_played[1]))[2:]
        year, month, day = birthday
        
        if name == "":
            return

        total_played, last_day_played = self.played_info(player.play_table())
        node = self.new_node("player")
        node.setAttribute("name", name)
        node.setAttribute("height", str(height))
        node.setAttribute("birthday", "%i-%02i-%02i"%(year, month, day))
        node.setAttribute("id", pid)
        node.setAttribute("last_played", last_played)
        node.setAttribute("last_day_played", str(last_day_played))
        node.setAttribute("total_played", str(total_played))


        node.appendChild(self.body_tests(player))
        node.appendChild(self.level_tables(player, player.level_table()))
        node.appendChild(self.play_tables(player.play_table()))

        self.add_node(node)
            
    def print_highscore_table(self, parser):
        res = self.new_node("highscores")
        for i, name in Shared.MAP.iterkeys():
            if name == "":
                continue
                
            node = self.new_node("highscore")
            node.setAttribute("name", Shared.game_name(i))
            for pname, score in parser.highscore(name):
                n = self.new_node("score")
                n.setAttribute("score", str(score))
                n.setAttribute("player_name", str(pname))
                node.appendChild(n)
            res.appendChild(node)
            
        self.add_node(res)


    def __init__(self):
        self._xml = getDOMImplementation()
        self._doc = self._xml.createDocument(None, "wiifit", None)
        self._topnode = self._doc.documentElement
    
    def printout(self):
        print self._doc.toprettyxml()

if len(sys.argv) == 1:
    print "Run as ./wiifitparser.py somewhere/over/the/rainbow/RPWiiFit.dat"
    sys.exit()

parser = WiiFitParser(sys.argv[1])
printer = Printer()

for i in range(0,8):
    p = parser.player(i)
    if p != None:
        printer.print_player(p)

printer.print_highscore_table(parser)
printer.printout()


import scraperwiki

# Download Savegame
# The following will need to be decrypted locally and then have the individual files uploded:
# http://jacobjwalker.effectiveeducation.org/blog/wp-content/uploads/2013/05/data.bin


# Future Feature: Decrypting Savegame in Python
# Currently the Savegame decryption needs to occur locally, and then placed online someplace for the scraper
# Information at http://jansenprice.com/blog?id=9-Extracting-Data-from-Wii-Fit-Plus-Savegame-Files
# In the future, I might try porting Segher's Wii.git tools from C to Python, possibly using the following info to help with the porting
# http://pyinsci.blogspot.com/2010/03/converting-c-code-to-python.html


# Parsing Decrypted Savegame
# Based upon code from http://wiifit.googlecode.com/svn/trunk/wiifitparser.py
# Originally created by freeall and mathiasbuus, with additions by huanix, and now me (Jacob J. Walker)

import sys
class PairKeyDict(dict):
    # Super slow way to do a check for the single key. BUT it works :-)
    def __getitem__(self, single_key):
        for pair_key, value in super(PairKeyDict, self).iteritems():
            if single_key in pair_key:
                return value
        raise KeyError
    
    # A nice way to actually, still use the keys as a map
    def other_key(self, single_key):
        for k1, k2 in super(PairKeyDict, self).iterkeys():
            if single_key == k1:
                return k2
            if single_key == k2:
                return k1
        return None        
        
class Shared:
    MAP = PairKeyDict({
        # This map represents where the games are located in the memory
        # For the stars and points the address is relative to the players block
        # address.
        # For highscore, the address is absolute to the RPWiiFit.dat file
        
        # (index, name) : (highscore, stars, points)
        (0, "") : (0x0, 0x0, 0x0),
        (1, "") : (0x0, 0x0, 0x0),
        (2, "") : (0x0, 0x0, 0x0),
        (3, "TABLE TILT") : (0x0, 0x0, 0x0),
        (4, "") : (0x0, 0x0, 0x0),
        (5, "") : (0x0, 0x0, 0x0),
        (6, "") : (0x0, 0x0, 0x0),
        (7, "") : (0x0, 0x0, 0x0),
        (8, "") : (0x0, 0x0, 0x0),
        (9, "SINGLE LEG EXTENSION") : (0x0, 0x0, 0x0),
        (10, "") : (0x0, 0x0, 0x0),
        (11, "") : (0x0, 0x0, 0x0),
        (12, "") : (0x0, 0x0, 0x0),
        (13, "") : (0x0, 0x0, 0x0),
        (14, "") : (0x0, 0x0, 0x0),
        (15, "PRESS-UP AND SIDE STAND") : (0x0, 0x0, 0x0),
        (16, "") : (0x0, 0x0, 0x0),
        (17, "") : (0x0, 0x0, 0x0),
        (18, "") : (0x0, 0x0, 0x0),
        (19, "") : (0x0, 0x0, 0x0),
        (20, "") : (0x0, 0x0, 0x0),
        (21, "") : (0x0, 0x0, 0x0),
        (22, "") : (0x0, 0x0, 0x0),
        (23, "") : (0x0, 0x0, 0x0),
        (24, "DEEP BREATHING") : (0x4AA90, 0x360F, 0x377C),
        (25, "HALF-MOON") : (0x4AB80, 0x3612, 0x3788),
        (26, "WARRIOR") : (0x4AC70, 0x3615, 0x3794),
        (27, "TREE") : (0x0, 0x0, 0x0),
        (28, "") : (0x0, 0x0, 0x0),
        (29, "") : (0x0, 0x0, 0x0),
        (30, "") : (0x0, 0x0, 0x0),
        (31, "") : (0x0, 0x0, 0x0),
        (32, "") : (0x0, 0x0, 0x0),
        (33, "") : (0x0, 0x0, 0x0),
        (34, "") : (0x0, 0x0, 0x0),
        (35, "") : (0x0, 0x0, 0x0),
        (36, "") : (0x0, 0x0, 0x0),
        (37, "") : (0x0, 0x0, 0x0),
        (38, "") : (0x0, 0x0, 0x0),
        (39, "HULLA HOOP") : (0x0, 0x0, 0x0),
        (40, "STEPS BASICS") : (0x0, 0x0, 0x0),
        (41, "") : (0x0, 0x0, 0x0),
        (42, "") : (0x0, 0x0, 0x0),
        (43, "") : (0x0, 0x0, 0x0),
        (44, "") : (0x0, 0x0, 0x0),
        (45, "") : (0x0, 0x0, 0x0),
        (46, "") : (0x0, 0x0, 0x0),
        (47, "") : (0x0, 0x0, 0x0)})
    
    @staticmethod    
    def game_name(game_index):
        def beautify_str(s):
            res = s[0] if s != None and len(s) > 0 else ""
            for i in range(1, len(s)):
                if s[i-1] in (" ", "-"):
                    res += s[i].upper()
                else:
                    res += s[i].lower()
            return res
        return beautify_str(Shared.MAP.other_key(game_index))
    
class Util:
    @staticmethod
    def convert_date_bytes(date_bytes):
        def add_leading_chars(stringg, char, length):
            return char*(length - len(stringg)) + stringg

        # Convert hex to binary (and add leading 0's)
        bin0 = add_leading_chars(bin(ord(date_bytes[0]))[2:], "0", 8)
        bin1 = add_leading_chars(bin(ord(date_bytes[1]))[2:], "0", 8)
        bin2 = add_leading_chars(bin(ord(date_bytes[2]))[2:], "0", 8)
        bin3 = add_leading_chars(bin(ord(date_bytes[3]))[2:], "0", 8)
        bin_date = bin0 + bin1 + bin2 + bin3

        year = int(bin_date[0:12], 2)
        month = int(bin_date[12:16], 2)
        day = int(bin_date[16:21], 2)
        hours = int(bin_date[21:26], 2)
        minutes = int(bin_date[26:32], 2)
        
        return (year, month, day, hours, minutes)

    @staticmethod
    def hex_combine(bytes):
        res = ""
        for b in bytes:
            res += hex(ord(b))[2:]
        return res
        
class Player:
    def __init__(self, data):
        self.data = data
        name = self.data[:20]
        if ord(name[0]) == 0 and ord(name[1]) == 0:
            raise Exception()
        
    def level_table(self):
        data = self.data[0x87:0x267]
        res = []
        for i in range(0,48):
            block = data[10*i:10*(i+1)]
            locked = True if ord(block[0]) == 0 else False
            last_played_level = ord(block[5])
            date = Util.convert_date_bytes(block[6:10])
        
            res.append((locked, last_played_level, date))
        return res
        
    def play_table(self):
        data = self.data[0x267:]
        
        res=[]
        
        i=0
        while ord(data[i*12]) != 0:
            day_data = data[i*12 : (i+1)*12]

            date = Util.hex_combine(day_data[0x0:0x0+2])
            balance_time = int(Util.hex_combine(day_data[0x2:0x2+2]), 16)
            workout_time = int(Util.hex_combine(day_data[0x4:0x4+2]), 16)
            yoga_time = int(Util.hex_combine(day_data[0x6:0x6+2]), 16)
            aerobic_time = int(Util.hex_combine(day_data[0x8:0x8+2]), 16)

            res.append((date, balance_time, workout_time, yoga_time, aerobic_time))
            i+=1
        
        return res
    
    def last_played(self):
        return self.data[0x36:0x36+2]

    def name(self):
        name = self.data[:20]
        res = ""
        for c in name:
            if ord(c) != 0: res += c
        return res

    def height(self):
        return ord(self.data[0x17])
        
    def birthday(self):
        year = int(hex(ord(self.data[0x18]))[2:] + hex(ord(self.data[0x19]))[2:])
        month = int(hex(ord(self.data[0x1A]))[2:])
        day = int(hex(ord(self.data[0x1B]))[2:])
        return (year, month, day)
        
    def totalplayed(self):
        return self.data[0x26D]

    def id(self):
        return Util.hex_combine(self.data[0x2D:0x31])

    def stars(self, game):
        return ord(self.data[Shared.MAP[game.upper()][1]])

    def points(self, game):
        return ord(self.data[Shared.MAP[game.upper()][2]])
    
    def bodytests(self):
        bt_start = 0x3899
        res=[]

        test_nr=0
        while True:
            test_nr += 1
      
            # break after we read 1096 bodytests, since 
            # there is no more space/data for this player
            if test_nr > 1096:
              break
         
            bodytest = self.data[bt_start + 21*(test_nr-1):bt_start + 21*test_nr]
        
            if ord(bodytest[0]) == 0:
                break
            date = Util.convert_date_bytes(bodytest[0:4])

            kg = bodytest[0x4:0x4+2]
            kg = int(hex(ord(kg[0]))[2:] + hex(ord(kg[1]))[2:], 16)
            kg = float(kg) /10
      
            bmi = bodytest[0x6:0x6+2]
            bmi = float("%s.%s"%(ord(bmi[0]), ord(bmi[1])))
        
            right_bal = bodytest[0x8:0x8+2]
            right_bal = int(hex(ord(right_bal[0]))[2:] + hex(ord(right_bal[1]))[2:], 16) / 10.0
            left_bal = 100.0 - right_bal
        
            wii_fit_age = ord(bodytest[0xE])
            
            res.append((date, bmi, kg, right_bal, left_bal, wii_fit_age))
        
        return res

class WiiFitParser:        
    def __init__(self, filename):
        self._f = open(filename, "r")
        self._players = {}
        # generate player_id -> player_name dictionary
        for i in range(0,8):
            try:
                p = self.player(i)
                self._players[p.id()] = p.name()
            except:
                pass

    def _raw_data(self, nr):
        self._f.seek(0x8 + 0x9281 * nr)
        return self._f.read(0x9281)
        
    def player(self, nr):
        try:
            p = Player(self._raw_data(nr))
            return p
        except:
            return None
            
    def highscore(self, game):
        self._f.seek(Shared.MAP[game.upper()][0])
        res = []

        if Shared.MAP[game.upper()] == (0x0, 0x0, 0x0):
            return res
        
        for s in range(0,11):
            # ID
            pid = self._f.read(0x4)
            
            if ord(pid[0]) == 0:
                continue
                
            # bytes -> hex-string
            pid = Util.hex_combine(pid)
            
            # read 0s
            self._f.read(0x3)
            
            score = ord(self._f.read(0x1))

            print game, pid, score
            print self._players
            res.append((self._players[pid], score))
        return res


from xml.dom.minidom import getDOMImplementation
class Printer:
    def body_tests(self, player):
        res = self.new_node("bodytests")
        
        bodytests = player.bodytests()
        for bodytest in bodytests:
            date, bmi, kg, right_bal, left_bal, wii_fit_age = bodytest
            year, month, day, hours, minutes = date
            
            node = self.new_node("bodytest")
            node.setAttribute("date", "%4i-%02i-%02i %02i:%02i"%(year, month, day, hours, minutes))
            node.setAttribute("bmi", str(bmi))
            node.setAttribute("kg", str(kg))
            node.setAttribute("right_balance", str(right_bal))
            node.setAttribute("left_balance", str(left_bal))
            node.setAttribute("wii_fit_age", str(wii_fit_age))
            res.appendChild(node)
        
        return res
    
    def level_tables(self, player, level_table):
        res = self.new_node("leveltable")
        
        for i in range(0,48):
            locked, last_played_level, date = level_table[i]

            if last_played_level == 0:
                continue
                
            year, month, day, hours, minutes = date
            name = Shared.game_name(i)
            points = player.points(name)
            stars = player.stars(name)

            node = self.new_node("game")
            node.setAttribute("id", str(i))
            node.setAttribute("name", name)
            node.setAttribute("last_played_level", str(last_played_level))
            node.setAttribute("stars", str(stars))
            node.setAttribute("points", str(points))
            node.setAttribute("date", "%i-%02i-%02i %02i:%02i"%(year, month, day, hours, minutes))
            res.appendChild(node)
        
        return res

    def play_tables(self, play_table):
        total_played = 0
        last_day_played = 0
        
        res = self.new_node("playtables")
        
        for play in play_table:
            date, balance_time, workout_time, yoga_time, aerobic_time = play

            last_day_played=balance_time + workout_time + yoga_time + aerobic_time
            total_played += balance_time + workout_time + yoga_time + aerobic_time
            node = self.new_node("playtable")
            node.setAttribute("date", str(date))
            node.setAttribute("balance_time", str(balance_time))
            node.setAttribute("workout_time", str(workout_time))
            node.setAttribute("yoga_time", str(yoga_time))
            node.setAttribute("aerobic_time", str(aerobic_time))
            res.appendChild(node)
            
        return res
        
    def played_info(self, play_table):
        total_played = 0
        last_day_played = 0
        
        for play in play_table:
            date, balance_time, workout_time, yoga_time, aerobic_time = play

            last_day_played=balance_time + workout_time + yoga_time + aerobic_time
            total_played += balance_time + workout_time + yoga_time + aerobic_time

        return (total_played, last_day_played)
    
    def new_node(self, name):
        return self._doc.createElement(name)
        
    def add_node(self, node):
        self._topnode.appendChild(node)
        
    def print_player(self, player):
        name = player.name()
        height = player.height()
        birthday = player.birthday()
        pid = player.id()
        last_played = player.last_played()
        last_played = hex(ord(last_played[0]))[2:] + hex(ord(last_played[1]))[2:]
        year, month, day = birthday
        
        if name == "":
            return

        total_played, last_day_played = self.played_info(player.play_table())
        node = self.new_node("player")
        node.setAttribute("name", name)
        node.setAttribute("height", str(height))
        node.setAttribute("birthday", "%i-%02i-%02i"%(year, month, day))
        node.setAttribute("id", pid)
        node.setAttribute("last_played", last_played)
        node.setAttribute("last_day_played", str(last_day_played))
        node.setAttribute("total_played", str(total_played))


        node.appendChild(self.body_tests(player))
        node.appendChild(self.level_tables(player, player.level_table()))
        node.appendChild(self.play_tables(player.play_table()))

        self.add_node(node)
            
    def print_highscore_table(self, parser):
        res = self.new_node("highscores")
        for i, name in Shared.MAP.iterkeys():
            if name == "":
                continue
                
            node = self.new_node("highscore")
            node.setAttribute("name", Shared.game_name(i))
            for pname, score in parser.highscore(name):
                n = self.new_node("score")
                n.setAttribute("score", str(score))
                n.setAttribute("player_name", str(pname))
                node.appendChild(n)
            res.appendChild(node)
            
        self.add_node(res)


    def __init__(self):
        self._xml = getDOMImplementation()
        self._doc = self._xml.createDocument(None, "wiifit", None)
        self._topnode = self._doc.documentElement
    
    def printout(self):
        print self._doc.toprettyxml()

if len(sys.argv) == 1:
    print "Run as ./wiifitparser.py somewhere/over/the/rainbow/RPWiiFit.dat"
    sys.exit()

parser = WiiFitParser(sys.argv[1])
printer = Printer()

for i in range(0,8):
    p = parser.player(i)
    if p != None:
        printer.print_player(p)

printer.print_highscore_table(parser)
printer.printout()


import scraperwiki

# Download Savegame
# The following will need to be decrypted locally and then have the individual files uploded:
# http://jacobjwalker.effectiveeducation.org/blog/wp-content/uploads/2013/05/data.bin


# Future Feature: Decrypting Savegame in Python
# Currently the Savegame decryption needs to occur locally, and then placed online someplace for the scraper
# Information at http://jansenprice.com/blog?id=9-Extracting-Data-from-Wii-Fit-Plus-Savegame-Files
# In the future, I might try porting Segher's Wii.git tools from C to Python, possibly using the following info to help with the porting
# http://pyinsci.blogspot.com/2010/03/converting-c-code-to-python.html


# Parsing Decrypted Savegame
# Based upon code from http://wiifit.googlecode.com/svn/trunk/wiifitparser.py
# Originally created by freeall and mathiasbuus, with additions by huanix, and now me (Jacob J. Walker)

import sys
class PairKeyDict(dict):
    # Super slow way to do a check for the single key. BUT it works :-)
    def __getitem__(self, single_key):
        for pair_key, value in super(PairKeyDict, self).iteritems():
            if single_key in pair_key:
                return value
        raise KeyError
    
    # A nice way to actually, still use the keys as a map
    def other_key(self, single_key):
        for k1, k2 in super(PairKeyDict, self).iterkeys():
            if single_key == k1:
                return k2
            if single_key == k2:
                return k1
        return None        
        
class Shared:
    MAP = PairKeyDict({
        # This map represents where the games are located in the memory
        # For the stars and points the address is relative to the players block
        # address.
        # For highscore, the address is absolute to the RPWiiFit.dat file
        
        # (index, name) : (highscore, stars, points)
        (0, "") : (0x0, 0x0, 0x0),
        (1, "") : (0x0, 0x0, 0x0),
        (2, "") : (0x0, 0x0, 0x0),
        (3, "TABLE TILT") : (0x0, 0x0, 0x0),
        (4, "") : (0x0, 0x0, 0x0),
        (5, "") : (0x0, 0x0, 0x0),
        (6, "") : (0x0, 0x0, 0x0),
        (7, "") : (0x0, 0x0, 0x0),
        (8, "") : (0x0, 0x0, 0x0),
        (9, "SINGLE LEG EXTENSION") : (0x0, 0x0, 0x0),
        (10, "") : (0x0, 0x0, 0x0),
        (11, "") : (0x0, 0x0, 0x0),
        (12, "") : (0x0, 0x0, 0x0),
        (13, "") : (0x0, 0x0, 0x0),
        (14, "") : (0x0, 0x0, 0x0),
        (15, "PRESS-UP AND SIDE STAND") : (0x0, 0x0, 0x0),
        (16, "") : (0x0, 0x0, 0x0),
        (17, "") : (0x0, 0x0, 0x0),
        (18, "") : (0x0, 0x0, 0x0),
        (19, "") : (0x0, 0x0, 0x0),
        (20, "") : (0x0, 0x0, 0x0),
        (21, "") : (0x0, 0x0, 0x0),
        (22, "") : (0x0, 0x0, 0x0),
        (23, "") : (0x0, 0x0, 0x0),
        (24, "DEEP BREATHING") : (0x4AA90, 0x360F, 0x377C),
        (25, "HALF-MOON") : (0x4AB80, 0x3612, 0x3788),
        (26, "WARRIOR") : (0x4AC70, 0x3615, 0x3794),
        (27, "TREE") : (0x0, 0x0, 0x0),
        (28, "") : (0x0, 0x0, 0x0),
        (29, "") : (0x0, 0x0, 0x0),
        (30, "") : (0x0, 0x0, 0x0),
        (31, "") : (0x0, 0x0, 0x0),
        (32, "") : (0x0, 0x0, 0x0),
        (33, "") : (0x0, 0x0, 0x0),
        (34, "") : (0x0, 0x0, 0x0),
        (35, "") : (0x0, 0x0, 0x0),
        (36, "") : (0x0, 0x0, 0x0),
        (37, "") : (0x0, 0x0, 0x0),
        (38, "") : (0x0, 0x0, 0x0),
        (39, "HULLA HOOP") : (0x0, 0x0, 0x0),
        (40, "STEPS BASICS") : (0x0, 0x0, 0x0),
        (41, "") : (0x0, 0x0, 0x0),
        (42, "") : (0x0, 0x0, 0x0),
        (43, "") : (0x0, 0x0, 0x0),
        (44, "") : (0x0, 0x0, 0x0),
        (45, "") : (0x0, 0x0, 0x0),
        (46, "") : (0x0, 0x0, 0x0),
        (47, "") : (0x0, 0x0, 0x0)})
    
    @staticmethod    
    def game_name(game_index):
        def beautify_str(s):
            res = s[0] if s != None and len(s) > 0 else ""
            for i in range(1, len(s)):
                if s[i-1] in (" ", "-"):
                    res += s[i].upper()
                else:
                    res += s[i].lower()
            return res
        return beautify_str(Shared.MAP.other_key(game_index))
    
class Util:
    @staticmethod
    def convert_date_bytes(date_bytes):
        def add_leading_chars(stringg, char, length):
            return char*(length - len(stringg)) + stringg

        # Convert hex to binary (and add leading 0's)
        bin0 = add_leading_chars(bin(ord(date_bytes[0]))[2:], "0", 8)
        bin1 = add_leading_chars(bin(ord(date_bytes[1]))[2:], "0", 8)
        bin2 = add_leading_chars(bin(ord(date_bytes[2]))[2:], "0", 8)
        bin3 = add_leading_chars(bin(ord(date_bytes[3]))[2:], "0", 8)
        bin_date = bin0 + bin1 + bin2 + bin3

        year = int(bin_date[0:12], 2)
        month = int(bin_date[12:16], 2)
        day = int(bin_date[16:21], 2)
        hours = int(bin_date[21:26], 2)
        minutes = int(bin_date[26:32], 2)
        
        return (year, month, day, hours, minutes)

    @staticmethod
    def hex_combine(bytes):
        res = ""
        for b in bytes:
            res += hex(ord(b))[2:]
        return res
        
class Player:
    def __init__(self, data):
        self.data = data
        name = self.data[:20]
        if ord(name[0]) == 0 and ord(name[1]) == 0:
            raise Exception()
        
    def level_table(self):
        data = self.data[0x87:0x267]
        res = []
        for i in range(0,48):
            block = data[10*i:10*(i+1)]
            locked = True if ord(block[0]) == 0 else False
            last_played_level = ord(block[5])
            date = Util.convert_date_bytes(block[6:10])
        
            res.append((locked, last_played_level, date))
        return res
        
    def play_table(self):
        data = self.data[0x267:]
        
        res=[]
        
        i=0
        while ord(data[i*12]) != 0:
            day_data = data[i*12 : (i+1)*12]

            date = Util.hex_combine(day_data[0x0:0x0+2])
            balance_time = int(Util.hex_combine(day_data[0x2:0x2+2]), 16)
            workout_time = int(Util.hex_combine(day_data[0x4:0x4+2]), 16)
            yoga_time = int(Util.hex_combine(day_data[0x6:0x6+2]), 16)
            aerobic_time = int(Util.hex_combine(day_data[0x8:0x8+2]), 16)

            res.append((date, balance_time, workout_time, yoga_time, aerobic_time))
            i+=1
        
        return res
    
    def last_played(self):
        return self.data[0x36:0x36+2]

    def name(self):
        name = self.data[:20]
        res = ""
        for c in name:
            if ord(c) != 0: res += c
        return res

    def height(self):
        return ord(self.data[0x17])
        
    def birthday(self):
        year = int(hex(ord(self.data[0x18]))[2:] + hex(ord(self.data[0x19]))[2:])
        month = int(hex(ord(self.data[0x1A]))[2:])
        day = int(hex(ord(self.data[0x1B]))[2:])
        return (year, month, day)
        
    def totalplayed(self):
        return self.data[0x26D]

    def id(self):
        return Util.hex_combine(self.data[0x2D:0x31])

    def stars(self, game):
        return ord(self.data[Shared.MAP[game.upper()][1]])

    def points(self, game):
        return ord(self.data[Shared.MAP[game.upper()][2]])
    
    def bodytests(self):
        bt_start = 0x3899
        res=[]

        test_nr=0
        while True:
            test_nr += 1
      
            # break after we read 1096 bodytests, since 
            # there is no more space/data for this player
            if test_nr > 1096:
              break
         
            bodytest = self.data[bt_start + 21*(test_nr-1):bt_start + 21*test_nr]
        
            if ord(bodytest[0]) == 0:
                break
            date = Util.convert_date_bytes(bodytest[0:4])

            kg = bodytest[0x4:0x4+2]
            kg = int(hex(ord(kg[0]))[2:] + hex(ord(kg[1]))[2:], 16)
            kg = float(kg) /10
      
            bmi = bodytest[0x6:0x6+2]
            bmi = float("%s.%s"%(ord(bmi[0]), ord(bmi[1])))
        
            right_bal = bodytest[0x8:0x8+2]
            right_bal = int(hex(ord(right_bal[0]))[2:] + hex(ord(right_bal[1]))[2:], 16) / 10.0
            left_bal = 100.0 - right_bal
        
            wii_fit_age = ord(bodytest[0xE])
            
            res.append((date, bmi, kg, right_bal, left_bal, wii_fit_age))
        
        return res

class WiiFitParser:        
    def __init__(self, filename):
        self._f = open(filename, "r")
        self._players = {}
        # generate player_id -> player_name dictionary
        for i in range(0,8):
            try:
                p = self.player(i)
                self._players[p.id()] = p.name()
            except:
                pass

    def _raw_data(self, nr):
        self._f.seek(0x8 + 0x9281 * nr)
        return self._f.read(0x9281)
        
    def player(self, nr):
        try:
            p = Player(self._raw_data(nr))
            return p
        except:
            return None
            
    def highscore(self, game):
        self._f.seek(Shared.MAP[game.upper()][0])
        res = []

        if Shared.MAP[game.upper()] == (0x0, 0x0, 0x0):
            return res
        
        for s in range(0,11):
            # ID
            pid = self._f.read(0x4)
            
            if ord(pid[0]) == 0:
                continue
                
            # bytes -> hex-string
            pid = Util.hex_combine(pid)
            
            # read 0s
            self._f.read(0x3)
            
            score = ord(self._f.read(0x1))

            print game, pid, score
            print self._players
            res.append((self._players[pid], score))
        return res


from xml.dom.minidom import getDOMImplementation
class Printer:
    def body_tests(self, player):
        res = self.new_node("bodytests")
        
        bodytests = player.bodytests()
        for bodytest in bodytests:
            date, bmi, kg, right_bal, left_bal, wii_fit_age = bodytest
            year, month, day, hours, minutes = date
            
            node = self.new_node("bodytest")
            node.setAttribute("date", "%4i-%02i-%02i %02i:%02i"%(year, month, day, hours, minutes))
            node.setAttribute("bmi", str(bmi))
            node.setAttribute("kg", str(kg))
            node.setAttribute("right_balance", str(right_bal))
            node.setAttribute("left_balance", str(left_bal))
            node.setAttribute("wii_fit_age", str(wii_fit_age))
            res.appendChild(node)
        
        return res
    
    def level_tables(self, player, level_table):
        res = self.new_node("leveltable")
        
        for i in range(0,48):
            locked, last_played_level, date = level_table[i]

            if last_played_level == 0:
                continue
                
            year, month, day, hours, minutes = date
            name = Shared.game_name(i)
            points = player.points(name)
            stars = player.stars(name)

            node = self.new_node("game")
            node.setAttribute("id", str(i))
            node.setAttribute("name", name)
            node.setAttribute("last_played_level", str(last_played_level))
            node.setAttribute("stars", str(stars))
            node.setAttribute("points", str(points))
            node.setAttribute("date", "%i-%02i-%02i %02i:%02i"%(year, month, day, hours, minutes))
            res.appendChild(node)
        
        return res

    def play_tables(self, play_table):
        total_played = 0
        last_day_played = 0
        
        res = self.new_node("playtables")
        
        for play in play_table:
            date, balance_time, workout_time, yoga_time, aerobic_time = play

            last_day_played=balance_time + workout_time + yoga_time + aerobic_time
            total_played += balance_time + workout_time + yoga_time + aerobic_time
            node = self.new_node("playtable")
            node.setAttribute("date", str(date))
            node.setAttribute("balance_time", str(balance_time))
            node.setAttribute("workout_time", str(workout_time))
            node.setAttribute("yoga_time", str(yoga_time))
            node.setAttribute("aerobic_time", str(aerobic_time))
            res.appendChild(node)
            
        return res
        
    def played_info(self, play_table):
        total_played = 0
        last_day_played = 0
        
        for play in play_table:
            date, balance_time, workout_time, yoga_time, aerobic_time = play

            last_day_played=balance_time + workout_time + yoga_time + aerobic_time
            total_played += balance_time + workout_time + yoga_time + aerobic_time

        return (total_played, last_day_played)
    
    def new_node(self, name):
        return self._doc.createElement(name)
        
    def add_node(self, node):
        self._topnode.appendChild(node)
        
    def print_player(self, player):
        name = player.name()
        height = player.height()
        birthday = player.birthday()
        pid = player.id()
        last_played = player.last_played()
        last_played = hex(ord(last_played[0]))[2:] + hex(ord(last_played[1]))[2:]
        year, month, day = birthday
        
        if name == "":
            return

        total_played, last_day_played = self.played_info(player.play_table())
        node = self.new_node("player")
        node.setAttribute("name", name)
        node.setAttribute("height", str(height))
        node.setAttribute("birthday", "%i-%02i-%02i"%(year, month, day))
        node.setAttribute("id", pid)
        node.setAttribute("last_played", last_played)
        node.setAttribute("last_day_played", str(last_day_played))
        node.setAttribute("total_played", str(total_played))


        node.appendChild(self.body_tests(player))
        node.appendChild(self.level_tables(player, player.level_table()))
        node.appendChild(self.play_tables(player.play_table()))

        self.add_node(node)
            
    def print_highscore_table(self, parser):
        res = self.new_node("highscores")
        for i, name in Shared.MAP.iterkeys():
            if name == "":
                continue
                
            node = self.new_node("highscore")
            node.setAttribute("name", Shared.game_name(i))
            for pname, score in parser.highscore(name):
                n = self.new_node("score")
                n.setAttribute("score", str(score))
                n.setAttribute("player_name", str(pname))
                node.appendChild(n)
            res.appendChild(node)
            
        self.add_node(res)


    def __init__(self):
        self._xml = getDOMImplementation()
        self._doc = self._xml.createDocument(None, "wiifit", None)
        self._topnode = self._doc.documentElement
    
    def printout(self):
        print self._doc.toprettyxml()

if len(sys.argv) == 1:
    print "Run as ./wiifitparser.py somewhere/over/the/rainbow/RPWiiFit.dat"
    sys.exit()

parser = WiiFitParser(sys.argv[1])
printer = Printer()

for i in range(0,8):
    p = parser.player(i)
    if p != None:
        printer.print_player(p)

printer.print_highscore_table(parser)
printer.printout()


