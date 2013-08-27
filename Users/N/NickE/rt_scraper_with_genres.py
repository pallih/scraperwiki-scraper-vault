import scraperwiki
import lxml
import urllib
import simplejson
import time

titles = ["Beneath the Darkness","The Devil Inside","Contraband","Beauty and the Beast 3D","The Divide","Joyful Noise","Coriolanus","Haywire","Red Tails","Underworld: Awakening","W.E.","The Grey","Man on a Ledge","One for the Money","Big Miracle","Chronicle","The Woman in Black","Journey 2: The Mysterious Island","Rampart","Safe House","Star Wars Episode I: The Phantom Menace 3D","The Vow","Ghost Rider: Spirit of Vengeance","This Means War","Act of Valor","Gone","Good Deeds","Wanderlust","This Is Not a Film","Being Flynn","Dr. Seuss' The Lorax","Project X","Tim and Eric's Billion Dollar Movie","Attenberg","The Ballad of Genesis and Lady Jaye","Footnote","Friends with Kids","Jiro Dreams of Sushi","John Carter","Salmon Fishing in the Yemen","Silent House","A Thousand Words","Gerhard Richter Painting","21 Jump Street","Casa de Mi Padre","Jeff, Who Lives at Home","The Hunger Games","October Baby","The Raid: Redemption","A Royal Affair","Goon","Mirror Mirror","Wrath of the Titans","Titanic 3D","American Reunion","Comic-Con Episode IV: A Fan's Hope","Damsels in Distress","Keyhole","Surviving Progress","We Have a Pope","The Cabin in the Woods","Lockout","Monsieur Lazhar","The Three Stooges","Chimpanzee","Darling Companion","Fightville","Jesus Henry Christ","The Lucky One","Marley","Think Like a Man","The Avengers","Payback","The Five-Year Engagement","Headhunters","The Pirates! In an Adventure with Scientists","The Raven","Safe","Sound of My Voice","First Position","Dark Shadows","Under African Skies","Where Do We Go Now?","The Dictator","Rust and Bone","Battleship","Beyond the Black Rainbow","Crooked Arrows","Fury","Virginia","What to Expect When You're Expecting","Chernobyl Diaries","Men in Black 3","Moonrise Kingdom","Oslo, August 31st","Piranha 3DD","Snow White and the Huntsman","Lola Versus","Madagascar 3: Europe's Most Wanted","Prometheus","Safety Not Guaranteed","Rock of Ages","That's My Boy","The Woman in the Fifth","Your Sister's Sister","Kumare","Abraham Lincoln: Vampire Hunter","Brave","The Invisible War","To Rome with Love","Seeking a Friend for the End of the World","Beasts of the Southern Wild","Madea's Witness Protection","Magic Mike","Neil Young Journeys","People Like Us","Take This Waltz","Ted","The Amazing Spider-Man","Katy Perry: Part of Me 3D","Collaborator","Savages","Farewell, My Queen","Ice Age: Continental Drift","The Imposter","Union Square","Shut Up and Play the Hits","The Dark Knight Rises","The Queen of Versailles","Iron Sky","Ruby Sparks","Ai Weiwei: Never Sorry","Killer Joe","Searching for Sugar Man","Step Up Revolution","The Watch","360","Celeste and Jesse Forever","Diary of a Wimpy Kid: Dog Days","Total Recall","Hope Springs","2 Days in New York","The Bourne Legacy","The Campaign","Ek Tha Tiger","The Odd Life of Timothy Green","Compliance","Cosmopolis","The Expendables 2","ParaNorman","Robot & Frank","Sparkle","Hit and Run","The Apparition","Premium Rush","The Ambassador","Lawless","The Oogieloves in the Big Balloon Adventure","For a Good Time, Call...","The Possession","Anna Karenina","Bachelorette","The Cold Light of Day","Detropia","Raaz 3D","Raiders of the Lost Ark: The IMAX Experience","The Words","Arbitrage","Barfi!","Finding Nemo 3D","The Master","Resident Evil: Retribution","Stolen","Amour","Diana Vreeland: The Eye Has to Travel","Dredd","End of Watch","Head Games","House at the End of the Street","The Perks of Being a Wallflower","Trouble with the Curve","Magical Mystery Tour","Hotel Transylvania","Looper","The Waiting Room","Won't Back Down","Frankenweenie","It's Such a Beautiful Day","The Oranges","The Paperboy","Pitch Perfect","Taken 2","3,2,1... Frankie Go Boom","Argo","Here Comes the Boom","Nobody Walks","Seven Psychopaths","Sinister","Smashed","Holy Motors","Alex Cross","Paranormal Activity 4","The Sessions","Chasing Mavericks","Cloud Atlas","Fun Size","Pusher","Silent Hill: Revelation 3D","Skyfall","Flight","A Late Quartet","A Liar's Autobiography","The Man with the Iron Fists","Wreck-It Ralph","Lincoln","In Their Skin","Jab Tak Hai Jaan","Chasing Ice","Silver Linings Playbook","The Twilight Saga: Breaking Dawn – Part 2","Life of Pi","Nativity 2: Danger in the Manger","Red Dawn","Rise of the Guardians","Hitchcock","The Collection","Killing Them Softly","Talaash","Deadfall","Dino Time","Heleno","Hyde Park on Hudson","Playing for Keeps","The Hobbit: An Unexpected Journey","The Guilt Trip","Monsters, Inc. 3D","Zero Dark Thirty","Cirque du Soleil: Worlds Away","The Impossible","Jack Reacher","Not Fade Away","This Is 40","Django Unchained","Les Misérables","Parental Guidance","Quartet","Tabu","Promised Land","A Dark Truth","Table No. 21","Texas Chainsaw 3D","The Grandmaster","A Haunted House","Gangster Squad","Matru Ki Bijlee Ka Mandola","Hansel and Gretel: Witch Hunters","Broken City","LUV","Mama","Officer Down","The Last Stand","John Dies at the End","Knife Fight","Movie 43","Parker","Race 2","Television","Bullet to the Head","Sound City","Stand Up Guys","The Haunting in Connecticut 2: Ghosts of Georgia","Warm Bodies","A Glimpse Inside the Mind of Charles Swan III","I Give It a Year","Identity Thief","Side Effects","Special 26","Top Gun 3D","Journey to the West: Conquering the Demons","A Good Day to Die Hard","Beautiful Creatures","Murder 3","Safe Haven","Escape from Planet Earth","Bless Me, Ultima","Dark Skies","Kai Po Che!","Snitch","To the Wonder","21 & Over","I, Me Aur Main","Jack the Giant Slayer","Phantom","Stoker","The Attacks of 26/11","The Last Exorcism Part II","Dead Man Down","Emperor","I'm So Excited","Oz the Great and Powerful","Goddess","Spring Breakers","The Call","The Incredible Burt Wonderstone","Welcome to the Punch","Admission","Inappropriate Comedy","Love and Honor","Olympus Has Fallen","The Croods","G.I. Joe: Retaliation","Trance","Himmatwala","Temptation: Confessions of a Marriage Counselor","The Host","The Place Beyond the Pines","Wrong","Evil Dead","Jurassic Park 3D","Settai","The Brass Teapot","Upstream Color","Fist of Legend","Oblivion","42","Disconnect","It's a Disaster","Scary Movie 5","Java Heat","Home Run","The Lords of Salem","At Any Price","Iron Man 3","Arthur Newman","Mud","Pain & Gain","The Big Wedding","Bombay Talkies","Greetings from Tim Buckley","Kiss of the Damned","Shootout at Wadala","The Iceman","What Maisie Knew","Star Trek Into Darkness","Aftershock","Go Goa Gone","He's Way More Famous Than You","No One Lives","The Great Gatsby","Tyler Perry Presents Peeples","Aurangzeb","Black Rock","Fast & Furious 6","Frances Ha","The English Teacher","The Hangover Part III","Before Midnight","Epic","After Earth","Byzantium","Now You See Me","The East","The Kings of Summer","The Purge","Yeh Jawaani Hai Deewani","Much Ado About Nothing","The Internship","Tiger Eyes","Violet & Daisy","This Is the End","Man of Steel","The Bling Ring","My Little Pony: Equestria Girls","Monsters University","World War Z","The Heat","White House Down"]

titles2 = ["Like Someone in Love","Narenji Poush"]


for s in range(scraperwiki.sqlite.get_var('upto'), len(titles)):
    titleNice = urllib.quote_plus(titles[s])
    title = simplejson.loads(scraperwiki.scrape('http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=bwt5wn89d4xjv93b8y86b93w&q=' + titleNice))
    try:
        movieTitle = title['movies'][0]['title']
        criticScore = title['movies'][0]['ratings']['critics_score']
        userScore = title['movies'][0]['ratings']['audience_score']
        url = title['movies'][0]['links']['alternate']
        id = title['movies'][0]['id']    
        linkURL = title['movies'][0]['links']['self']
        mpaa_rating = title['movies'][0]['mpaa_rating']
    
        try:
            lead_actor1 = title['movies'][0]['abridged_cast'][0]['name']
        except:
            lead_actor1 = 'na'
        try:
            lead_actor2 = title['movies'][0]['abridged_cast'][1]['name']    
        except:
            lead_actor2 = 'na'    
    
        if movieTitle == titles[s]:
            matching = 'yes'
        else:
            matching = 'no'
    
        try:
            moreDetail = simplejson.loads(scraperwiki.scrape(linkURL + '?apikey=bwt5wn89d4xjv93b8y86b93w'))
            try:
                genres = moreDetail['genres']
            except:
                genres = 'na'
            try:
                studio = moreDetail['studio'] 
            except:
                studio = 'na'
            try:
                director = moreDetail['abridged_directors'][0]['name']
            except:
                director = 'na'
        except:
            genres = 'na'
            studio = 'na'
            director = 'na'

        print matching
        print movieTitle
        print criticScore
        print userScore
        print url
        print id
        print genres
        print mpaa_rating
        print lead_actor1
        print lead_actor2
        print studio
        print director
    
        data = {}
        data['title'] = movieTitle
        data['critic_score'] = criticScore
        data['user_score'] = userScore
        data['url'] = url
        data['id'] = id
        data['genres'] = genres
        data['mpaa_rating'] = mpaa_rating
        data['lead_actor1'] = lead_actor1
        data['lead_actor2'] = lead_actor2
        data['studio'] = studio
        data['titles_match'] = matching
        data['old_title'] = titles[s]
        data['direcotr'] = director   
        scraperwiki.sqlite.save(unique_keys=["id"], data=data)
        scraperwiki.sqlite.save_var('upto', s)
    except:
        print 'Nah, no movie called ' + titles[s]
    time.sleep(2)



import scraperwiki
import lxml
import urllib
import simplejson
import time

titles = ["Beneath the Darkness","The Devil Inside","Contraband","Beauty and the Beast 3D","The Divide","Joyful Noise","Coriolanus","Haywire","Red Tails","Underworld: Awakening","W.E.","The Grey","Man on a Ledge","One for the Money","Big Miracle","Chronicle","The Woman in Black","Journey 2: The Mysterious Island","Rampart","Safe House","Star Wars Episode I: The Phantom Menace 3D","The Vow","Ghost Rider: Spirit of Vengeance","This Means War","Act of Valor","Gone","Good Deeds","Wanderlust","This Is Not a Film","Being Flynn","Dr. Seuss' The Lorax","Project X","Tim and Eric's Billion Dollar Movie","Attenberg","The Ballad of Genesis and Lady Jaye","Footnote","Friends with Kids","Jiro Dreams of Sushi","John Carter","Salmon Fishing in the Yemen","Silent House","A Thousand Words","Gerhard Richter Painting","21 Jump Street","Casa de Mi Padre","Jeff, Who Lives at Home","The Hunger Games","October Baby","The Raid: Redemption","A Royal Affair","Goon","Mirror Mirror","Wrath of the Titans","Titanic 3D","American Reunion","Comic-Con Episode IV: A Fan's Hope","Damsels in Distress","Keyhole","Surviving Progress","We Have a Pope","The Cabin in the Woods","Lockout","Monsieur Lazhar","The Three Stooges","Chimpanzee","Darling Companion","Fightville","Jesus Henry Christ","The Lucky One","Marley","Think Like a Man","The Avengers","Payback","The Five-Year Engagement","Headhunters","The Pirates! In an Adventure with Scientists","The Raven","Safe","Sound of My Voice","First Position","Dark Shadows","Under African Skies","Where Do We Go Now?","The Dictator","Rust and Bone","Battleship","Beyond the Black Rainbow","Crooked Arrows","Fury","Virginia","What to Expect When You're Expecting","Chernobyl Diaries","Men in Black 3","Moonrise Kingdom","Oslo, August 31st","Piranha 3DD","Snow White and the Huntsman","Lola Versus","Madagascar 3: Europe's Most Wanted","Prometheus","Safety Not Guaranteed","Rock of Ages","That's My Boy","The Woman in the Fifth","Your Sister's Sister","Kumare","Abraham Lincoln: Vampire Hunter","Brave","The Invisible War","To Rome with Love","Seeking a Friend for the End of the World","Beasts of the Southern Wild","Madea's Witness Protection","Magic Mike","Neil Young Journeys","People Like Us","Take This Waltz","Ted","The Amazing Spider-Man","Katy Perry: Part of Me 3D","Collaborator","Savages","Farewell, My Queen","Ice Age: Continental Drift","The Imposter","Union Square","Shut Up and Play the Hits","The Dark Knight Rises","The Queen of Versailles","Iron Sky","Ruby Sparks","Ai Weiwei: Never Sorry","Killer Joe","Searching for Sugar Man","Step Up Revolution","The Watch","360","Celeste and Jesse Forever","Diary of a Wimpy Kid: Dog Days","Total Recall","Hope Springs","2 Days in New York","The Bourne Legacy","The Campaign","Ek Tha Tiger","The Odd Life of Timothy Green","Compliance","Cosmopolis","The Expendables 2","ParaNorman","Robot & Frank","Sparkle","Hit and Run","The Apparition","Premium Rush","The Ambassador","Lawless","The Oogieloves in the Big Balloon Adventure","For a Good Time, Call...","The Possession","Anna Karenina","Bachelorette","The Cold Light of Day","Detropia","Raaz 3D","Raiders of the Lost Ark: The IMAX Experience","The Words","Arbitrage","Barfi!","Finding Nemo 3D","The Master","Resident Evil: Retribution","Stolen","Amour","Diana Vreeland: The Eye Has to Travel","Dredd","End of Watch","Head Games","House at the End of the Street","The Perks of Being a Wallflower","Trouble with the Curve","Magical Mystery Tour","Hotel Transylvania","Looper","The Waiting Room","Won't Back Down","Frankenweenie","It's Such a Beautiful Day","The Oranges","The Paperboy","Pitch Perfect","Taken 2","3,2,1... Frankie Go Boom","Argo","Here Comes the Boom","Nobody Walks","Seven Psychopaths","Sinister","Smashed","Holy Motors","Alex Cross","Paranormal Activity 4","The Sessions","Chasing Mavericks","Cloud Atlas","Fun Size","Pusher","Silent Hill: Revelation 3D","Skyfall","Flight","A Late Quartet","A Liar's Autobiography","The Man with the Iron Fists","Wreck-It Ralph","Lincoln","In Their Skin","Jab Tak Hai Jaan","Chasing Ice","Silver Linings Playbook","The Twilight Saga: Breaking Dawn – Part 2","Life of Pi","Nativity 2: Danger in the Manger","Red Dawn","Rise of the Guardians","Hitchcock","The Collection","Killing Them Softly","Talaash","Deadfall","Dino Time","Heleno","Hyde Park on Hudson","Playing for Keeps","The Hobbit: An Unexpected Journey","The Guilt Trip","Monsters, Inc. 3D","Zero Dark Thirty","Cirque du Soleil: Worlds Away","The Impossible","Jack Reacher","Not Fade Away","This Is 40","Django Unchained","Les Misérables","Parental Guidance","Quartet","Tabu","Promised Land","A Dark Truth","Table No. 21","Texas Chainsaw 3D","The Grandmaster","A Haunted House","Gangster Squad","Matru Ki Bijlee Ka Mandola","Hansel and Gretel: Witch Hunters","Broken City","LUV","Mama","Officer Down","The Last Stand","John Dies at the End","Knife Fight","Movie 43","Parker","Race 2","Television","Bullet to the Head","Sound City","Stand Up Guys","The Haunting in Connecticut 2: Ghosts of Georgia","Warm Bodies","A Glimpse Inside the Mind of Charles Swan III","I Give It a Year","Identity Thief","Side Effects","Special 26","Top Gun 3D","Journey to the West: Conquering the Demons","A Good Day to Die Hard","Beautiful Creatures","Murder 3","Safe Haven","Escape from Planet Earth","Bless Me, Ultima","Dark Skies","Kai Po Che!","Snitch","To the Wonder","21 & Over","I, Me Aur Main","Jack the Giant Slayer","Phantom","Stoker","The Attacks of 26/11","The Last Exorcism Part II","Dead Man Down","Emperor","I'm So Excited","Oz the Great and Powerful","Goddess","Spring Breakers","The Call","The Incredible Burt Wonderstone","Welcome to the Punch","Admission","Inappropriate Comedy","Love and Honor","Olympus Has Fallen","The Croods","G.I. Joe: Retaliation","Trance","Himmatwala","Temptation: Confessions of a Marriage Counselor","The Host","The Place Beyond the Pines","Wrong","Evil Dead","Jurassic Park 3D","Settai","The Brass Teapot","Upstream Color","Fist of Legend","Oblivion","42","Disconnect","It's a Disaster","Scary Movie 5","Java Heat","Home Run","The Lords of Salem","At Any Price","Iron Man 3","Arthur Newman","Mud","Pain & Gain","The Big Wedding","Bombay Talkies","Greetings from Tim Buckley","Kiss of the Damned","Shootout at Wadala","The Iceman","What Maisie Knew","Star Trek Into Darkness","Aftershock","Go Goa Gone","He's Way More Famous Than You","No One Lives","The Great Gatsby","Tyler Perry Presents Peeples","Aurangzeb","Black Rock","Fast & Furious 6","Frances Ha","The English Teacher","The Hangover Part III","Before Midnight","Epic","After Earth","Byzantium","Now You See Me","The East","The Kings of Summer","The Purge","Yeh Jawaani Hai Deewani","Much Ado About Nothing","The Internship","Tiger Eyes","Violet & Daisy","This Is the End","Man of Steel","The Bling Ring","My Little Pony: Equestria Girls","Monsters University","World War Z","The Heat","White House Down"]

titles2 = ["Like Someone in Love","Narenji Poush"]


for s in range(scraperwiki.sqlite.get_var('upto'), len(titles)):
    titleNice = urllib.quote_plus(titles[s])
    title = simplejson.loads(scraperwiki.scrape('http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=bwt5wn89d4xjv93b8y86b93w&q=' + titleNice))
    try:
        movieTitle = title['movies'][0]['title']
        criticScore = title['movies'][0]['ratings']['critics_score']
        userScore = title['movies'][0]['ratings']['audience_score']
        url = title['movies'][0]['links']['alternate']
        id = title['movies'][0]['id']    
        linkURL = title['movies'][0]['links']['self']
        mpaa_rating = title['movies'][0]['mpaa_rating']
    
        try:
            lead_actor1 = title['movies'][0]['abridged_cast'][0]['name']
        except:
            lead_actor1 = 'na'
        try:
            lead_actor2 = title['movies'][0]['abridged_cast'][1]['name']    
        except:
            lead_actor2 = 'na'    
    
        if movieTitle == titles[s]:
            matching = 'yes'
        else:
            matching = 'no'
    
        try:
            moreDetail = simplejson.loads(scraperwiki.scrape(linkURL + '?apikey=bwt5wn89d4xjv93b8y86b93w'))
            try:
                genres = moreDetail['genres']
            except:
                genres = 'na'
            try:
                studio = moreDetail['studio'] 
            except:
                studio = 'na'
            try:
                director = moreDetail['abridged_directors'][0]['name']
            except:
                director = 'na'
        except:
            genres = 'na'
            studio = 'na'
            director = 'na'

        print matching
        print movieTitle
        print criticScore
        print userScore
        print url
        print id
        print genres
        print mpaa_rating
        print lead_actor1
        print lead_actor2
        print studio
        print director
    
        data = {}
        data['title'] = movieTitle
        data['critic_score'] = criticScore
        data['user_score'] = userScore
        data['url'] = url
        data['id'] = id
        data['genres'] = genres
        data['mpaa_rating'] = mpaa_rating
        data['lead_actor1'] = lead_actor1
        data['lead_actor2'] = lead_actor2
        data['studio'] = studio
        data['titles_match'] = matching
        data['old_title'] = titles[s]
        data['direcotr'] = director   
        scraperwiki.sqlite.save(unique_keys=["id"], data=data)
        scraperwiki.sqlite.save_var('upto', s)
    except:
        print 'Nah, no movie called ' + titles[s]
    time.sleep(2)



import scraperwiki
import lxml
import urllib
import simplejson
import time

titles = ["Beneath the Darkness","The Devil Inside","Contraband","Beauty and the Beast 3D","The Divide","Joyful Noise","Coriolanus","Haywire","Red Tails","Underworld: Awakening","W.E.","The Grey","Man on a Ledge","One for the Money","Big Miracle","Chronicle","The Woman in Black","Journey 2: The Mysterious Island","Rampart","Safe House","Star Wars Episode I: The Phantom Menace 3D","The Vow","Ghost Rider: Spirit of Vengeance","This Means War","Act of Valor","Gone","Good Deeds","Wanderlust","This Is Not a Film","Being Flynn","Dr. Seuss' The Lorax","Project X","Tim and Eric's Billion Dollar Movie","Attenberg","The Ballad of Genesis and Lady Jaye","Footnote","Friends with Kids","Jiro Dreams of Sushi","John Carter","Salmon Fishing in the Yemen","Silent House","A Thousand Words","Gerhard Richter Painting","21 Jump Street","Casa de Mi Padre","Jeff, Who Lives at Home","The Hunger Games","October Baby","The Raid: Redemption","A Royal Affair","Goon","Mirror Mirror","Wrath of the Titans","Titanic 3D","American Reunion","Comic-Con Episode IV: A Fan's Hope","Damsels in Distress","Keyhole","Surviving Progress","We Have a Pope","The Cabin in the Woods","Lockout","Monsieur Lazhar","The Three Stooges","Chimpanzee","Darling Companion","Fightville","Jesus Henry Christ","The Lucky One","Marley","Think Like a Man","The Avengers","Payback","The Five-Year Engagement","Headhunters","The Pirates! In an Adventure with Scientists","The Raven","Safe","Sound of My Voice","First Position","Dark Shadows","Under African Skies","Where Do We Go Now?","The Dictator","Rust and Bone","Battleship","Beyond the Black Rainbow","Crooked Arrows","Fury","Virginia","What to Expect When You're Expecting","Chernobyl Diaries","Men in Black 3","Moonrise Kingdom","Oslo, August 31st","Piranha 3DD","Snow White and the Huntsman","Lola Versus","Madagascar 3: Europe's Most Wanted","Prometheus","Safety Not Guaranteed","Rock of Ages","That's My Boy","The Woman in the Fifth","Your Sister's Sister","Kumare","Abraham Lincoln: Vampire Hunter","Brave","The Invisible War","To Rome with Love","Seeking a Friend for the End of the World","Beasts of the Southern Wild","Madea's Witness Protection","Magic Mike","Neil Young Journeys","People Like Us","Take This Waltz","Ted","The Amazing Spider-Man","Katy Perry: Part of Me 3D","Collaborator","Savages","Farewell, My Queen","Ice Age: Continental Drift","The Imposter","Union Square","Shut Up and Play the Hits","The Dark Knight Rises","The Queen of Versailles","Iron Sky","Ruby Sparks","Ai Weiwei: Never Sorry","Killer Joe","Searching for Sugar Man","Step Up Revolution","The Watch","360","Celeste and Jesse Forever","Diary of a Wimpy Kid: Dog Days","Total Recall","Hope Springs","2 Days in New York","The Bourne Legacy","The Campaign","Ek Tha Tiger","The Odd Life of Timothy Green","Compliance","Cosmopolis","The Expendables 2","ParaNorman","Robot & Frank","Sparkle","Hit and Run","The Apparition","Premium Rush","The Ambassador","Lawless","The Oogieloves in the Big Balloon Adventure","For a Good Time, Call...","The Possession","Anna Karenina","Bachelorette","The Cold Light of Day","Detropia","Raaz 3D","Raiders of the Lost Ark: The IMAX Experience","The Words","Arbitrage","Barfi!","Finding Nemo 3D","The Master","Resident Evil: Retribution","Stolen","Amour","Diana Vreeland: The Eye Has to Travel","Dredd","End of Watch","Head Games","House at the End of the Street","The Perks of Being a Wallflower","Trouble with the Curve","Magical Mystery Tour","Hotel Transylvania","Looper","The Waiting Room","Won't Back Down","Frankenweenie","It's Such a Beautiful Day","The Oranges","The Paperboy","Pitch Perfect","Taken 2","3,2,1... Frankie Go Boom","Argo","Here Comes the Boom","Nobody Walks","Seven Psychopaths","Sinister","Smashed","Holy Motors","Alex Cross","Paranormal Activity 4","The Sessions","Chasing Mavericks","Cloud Atlas","Fun Size","Pusher","Silent Hill: Revelation 3D","Skyfall","Flight","A Late Quartet","A Liar's Autobiography","The Man with the Iron Fists","Wreck-It Ralph","Lincoln","In Their Skin","Jab Tak Hai Jaan","Chasing Ice","Silver Linings Playbook","The Twilight Saga: Breaking Dawn – Part 2","Life of Pi","Nativity 2: Danger in the Manger","Red Dawn","Rise of the Guardians","Hitchcock","The Collection","Killing Them Softly","Talaash","Deadfall","Dino Time","Heleno","Hyde Park on Hudson","Playing for Keeps","The Hobbit: An Unexpected Journey","The Guilt Trip","Monsters, Inc. 3D","Zero Dark Thirty","Cirque du Soleil: Worlds Away","The Impossible","Jack Reacher","Not Fade Away","This Is 40","Django Unchained","Les Misérables","Parental Guidance","Quartet","Tabu","Promised Land","A Dark Truth","Table No. 21","Texas Chainsaw 3D","The Grandmaster","A Haunted House","Gangster Squad","Matru Ki Bijlee Ka Mandola","Hansel and Gretel: Witch Hunters","Broken City","LUV","Mama","Officer Down","The Last Stand","John Dies at the End","Knife Fight","Movie 43","Parker","Race 2","Television","Bullet to the Head","Sound City","Stand Up Guys","The Haunting in Connecticut 2: Ghosts of Georgia","Warm Bodies","A Glimpse Inside the Mind of Charles Swan III","I Give It a Year","Identity Thief","Side Effects","Special 26","Top Gun 3D","Journey to the West: Conquering the Demons","A Good Day to Die Hard","Beautiful Creatures","Murder 3","Safe Haven","Escape from Planet Earth","Bless Me, Ultima","Dark Skies","Kai Po Che!","Snitch","To the Wonder","21 & Over","I, Me Aur Main","Jack the Giant Slayer","Phantom","Stoker","The Attacks of 26/11","The Last Exorcism Part II","Dead Man Down","Emperor","I'm So Excited","Oz the Great and Powerful","Goddess","Spring Breakers","The Call","The Incredible Burt Wonderstone","Welcome to the Punch","Admission","Inappropriate Comedy","Love and Honor","Olympus Has Fallen","The Croods","G.I. Joe: Retaliation","Trance","Himmatwala","Temptation: Confessions of a Marriage Counselor","The Host","The Place Beyond the Pines","Wrong","Evil Dead","Jurassic Park 3D","Settai","The Brass Teapot","Upstream Color","Fist of Legend","Oblivion","42","Disconnect","It's a Disaster","Scary Movie 5","Java Heat","Home Run","The Lords of Salem","At Any Price","Iron Man 3","Arthur Newman","Mud","Pain & Gain","The Big Wedding","Bombay Talkies","Greetings from Tim Buckley","Kiss of the Damned","Shootout at Wadala","The Iceman","What Maisie Knew","Star Trek Into Darkness","Aftershock","Go Goa Gone","He's Way More Famous Than You","No One Lives","The Great Gatsby","Tyler Perry Presents Peeples","Aurangzeb","Black Rock","Fast & Furious 6","Frances Ha","The English Teacher","The Hangover Part III","Before Midnight","Epic","After Earth","Byzantium","Now You See Me","The East","The Kings of Summer","The Purge","Yeh Jawaani Hai Deewani","Much Ado About Nothing","The Internship","Tiger Eyes","Violet & Daisy","This Is the End","Man of Steel","The Bling Ring","My Little Pony: Equestria Girls","Monsters University","World War Z","The Heat","White House Down"]

titles2 = ["Like Someone in Love","Narenji Poush"]


for s in range(scraperwiki.sqlite.get_var('upto'), len(titles)):
    titleNice = urllib.quote_plus(titles[s])
    title = simplejson.loads(scraperwiki.scrape('http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=bwt5wn89d4xjv93b8y86b93w&q=' + titleNice))
    try:
        movieTitle = title['movies'][0]['title']
        criticScore = title['movies'][0]['ratings']['critics_score']
        userScore = title['movies'][0]['ratings']['audience_score']
        url = title['movies'][0]['links']['alternate']
        id = title['movies'][0]['id']    
        linkURL = title['movies'][0]['links']['self']
        mpaa_rating = title['movies'][0]['mpaa_rating']
    
        try:
            lead_actor1 = title['movies'][0]['abridged_cast'][0]['name']
        except:
            lead_actor1 = 'na'
        try:
            lead_actor2 = title['movies'][0]['abridged_cast'][1]['name']    
        except:
            lead_actor2 = 'na'    
    
        if movieTitle == titles[s]:
            matching = 'yes'
        else:
            matching = 'no'
    
        try:
            moreDetail = simplejson.loads(scraperwiki.scrape(linkURL + '?apikey=bwt5wn89d4xjv93b8y86b93w'))
            try:
                genres = moreDetail['genres']
            except:
                genres = 'na'
            try:
                studio = moreDetail['studio'] 
            except:
                studio = 'na'
            try:
                director = moreDetail['abridged_directors'][0]['name']
            except:
                director = 'na'
        except:
            genres = 'na'
            studio = 'na'
            director = 'na'

        print matching
        print movieTitle
        print criticScore
        print userScore
        print url
        print id
        print genres
        print mpaa_rating
        print lead_actor1
        print lead_actor2
        print studio
        print director
    
        data = {}
        data['title'] = movieTitle
        data['critic_score'] = criticScore
        data['user_score'] = userScore
        data['url'] = url
        data['id'] = id
        data['genres'] = genres
        data['mpaa_rating'] = mpaa_rating
        data['lead_actor1'] = lead_actor1
        data['lead_actor2'] = lead_actor2
        data['studio'] = studio
        data['titles_match'] = matching
        data['old_title'] = titles[s]
        data['direcotr'] = director   
        scraperwiki.sqlite.save(unique_keys=["id"], data=data)
        scraperwiki.sqlite.save_var('upto', s)
    except:
        print 'Nah, no movie called ' + titles[s]
    time.sleep(2)



