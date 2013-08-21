#!/usr/bin/env python
#coding: utf8 

import scraperwiki
import lxml
import urllib
import simplejson
import time

titles = ["The Amazing Spider-Man 2","The Shawshank Redemption","The Godfather","Star Wars: Episode IV - A New Hope","Back to the Future","The Breakfast Club","The Goonies","The Silence of the Lambs","Jurassic Park","The Lion King","Pulp Fiction","Se7en","Toy Story","The Big Lebowski","Saving Private Ryan","Fight Club","The Matrix","Star Wars: Episode I - The Phantom Menace","Gladiator","X-Men","Harry Potter and the Philosopher's Stone","The Lord of the Rings: The Fellowship of the Ring","The Lord of the Rings: The Two Towers","xXx","Finding Nemo","The Lord of the Rings: The Return of the King","Anchorman: The Legend of Ron Burgundy","Mean Girls","Sin City","Star Wars: Episode III - Revenge of the Sith","Batman Begins","The Departed","The Prestige","V for Vendetta","Casino Royale","Transformers","The Dark Knight","Iron Man","Quantum of Solace","Tropic Thunder","G.I. Joe: The Rise of Cobra","The Hangover","Inglourious Basterds","Star Trek","Taken","Up","X-Men Origins: Wolverine","Zombieland","2012","Avatar","Despicable Me","Grown Ups","How to Train Your Dragon","Inception","Iron Man 2","Kick-Ass","Red","Shutter Island","TRON: Legacy","Toy Story 3","Drive","Fast & Furious 5","Harry Potter and the Deathly Hallows: Part 2","Limitless","Pirates of the Caribbean: On Stranger Tides","X-Men: First Class","The Girl with the Dragon Tattoo","The Help","In Time","21 Jump Street","The Amazing Spider-Man","American Reunion","The Avengers","Battleship","The Bourne Legacy","Brave","The Cabin in the Woods","The Campaign","Cloud Atlas","The Dark Knight Rises","Dark Shadows","Django Unchained","Dredd","End of Watch","The Expendables 2","Flight","The Guilt Trip","Here Comes the Boom","The Hobbit: An Unexpected Journey","Hotel Transylvania","Jack Reacher","John Carter","Killing Them Softly","Lawless","Life of Pi","Looper","Magic Mike","Man on a Ledge","The Man with the Iron Fists","The Master","Men in Black 3","Parental Guidance","Project X","Prometheus","Red Dawn","Rise of the Guardians","Savages","Seven Psychopaths","Sinister","Skyfall","Snow White and the Huntsman","Taken 2","Ted","That's My Boy","This Is 40","Total Recall","Promised Land","Wreck-It Ralph","Jack the Giant Slayer","Oz the Great and Powerful","A Good Day to Die Hard","Trance","Side Effects","Spring Breakers","The Incredible Burt Wonderstone","Disconnect","Mud","The Company You Keep","Olympus Has Fallen","The Place Beyond the Pines","G.I. Joe: Retaliation","The Croods","A Haunted House","World War Z","Oblivion","Ender's Game","The Hobbit: The Desolation of Smaug","Man of Steel","Pacific Rim","The Hunger Games: Catching Fire","The Lone Ranger","The Wolverine","Elysium","After Earth","Iron Man 3","This Is the End","R.I.P.D.","Thor: The Dark World","Star Trek Into Darkness","Now You See Me","The Hangover Part III","Kick-Ass 2","The Lords of Salem","Iron Sky","The Impossible","Filly Brown","Antiviral","Anna Karenina","The Cloth","What Richard Did","Stand Up Guys","Tomorrow You're Gone","Not Fade Away","Any Day Now","Under the Bed","Outback","The Boondock Saints","The Evil Dead","42","Evil Dead","Scary MoVie","Broken City","Gangster Squad","Furious 6","Pain & Gain","The Numbers Station","Mama","Pawn","300: Rise of an Empire","Temptation: Confessions of a Marriage Counselor","The Way, Way Back","Grown Ups 2","Dark Skies","Assassins Run","Percy Jackson: Sea of Monsters","The Bling Ring","Identity Thief","The Big Wedding","Welcome to the Punch","Only God Forgives","Devils of War","Movie 43","The Haunting in Connecticut 2: Ghosts of Georgia","The Call","Crush","Hansel & Gretel: Witch Hunters","The Purge","Snitch","A Clockwork Orange","Willy Wonka & the Chocolate Factory","The Godfather: Part II","One Flew Over the Cuckoo's Nest","Star Wars: Episode V - The Empire Strikes Back","Raiders of the Lost Ark","Apocalypse Now","Alien","Blade Runner","E.T. the Extra-Terrestrial","The Outsiders","Scarface","Star Wars: Episode VI - Return of the Jedi","Ghostbusters","Red Dawn","The Terminator","Full Metal Jacket","Die Hard","Leon: The Professional","The Usual Suspects","Heat","Independence Day","Good Will Hunting","Armageddon","The Truman Show","American Beauty","Big Daddy","The Green Mile","The Mummy","Office Space","The Sixth Sense","Toy Story 2","American Psycho","Scary Movie","Snatch.","Monsters, Inc.","Men in Black II","Red Dragon","Spider-Man","Spirited Away","Star Wars: Episode II - Attack of the Clones","The Italian Job","The Matrix Reloaded","Pirates of the Caribbean: The Curse of the Black Pearl","Big Fish","Kill Bill: Vol. 1","Dodgeball: A True Underdog Story","EuroTrip","Harry Potter and the Prisoner of Azkaban","The Incredibles","Napoleon Dynamite","Shaun of the Dead","Crash","The Chronicles of Narnia: The Lion, the Witch and the Wardrobe","Harry Potter and the Goblet of Fire","Cars","Pan's Labyrinth","Superman Returns","Talladega Nights: The Ballad of Ricky Bobby","X-Men: The Last Stand","The Bourne Ultimatum","Die Hard 4.0","No Country for Old Men","Ratatouille","Superbad","There Will Be Blood","Jumper","Gran Torino","The Incredible Hulk","Pineapple Express","RocknRolla","Role Models","Step Brothers","Wanted","District 9","Harry Potter and the Half-Blood Prince","Law Abiding Citizen","Terminator Salvation","Transformers: Revenge of the Fallen","Watchmen","Sherlock Holmes","The A-Team","Alice in Wonderland","Black Swan","The Book of Eli","Clash of the Titans","Due Date","The Expendables","Get Him to the Greek","Harry Potter and the Deathly Hallows: Part 1","The Other Guys","Percy Jackson & the Olympians: The Lightning Thief","Robin Hood","Salt","The Town","Bad Teacher","World Invasion: Battle LA","Cars 2","The Change-Up","Cowboys & Aliens","Green Lantern","The Hangover Part II","Horrible Bosses","I Am Number Four","Paul","Rio","Rise of the Planet of the Apes","Scream 4","Source Code","Sucker Punch","50/50","Contagion","The Descendants","The Ides of March","Immortals","Real Steel","Sherlock Holmes: A Game of Shadows","Tinker Tailor Soldier Spy","We Bought a Zoo","Abraham Lincoln: Vampire Hunter","Alex Cross","Chasing Mavericks","Chernobyl Diaries","Chronicle","The Collection","Contraband","The Dictator","Fun Size","The Grey","Haywire","House at the End of the Street","Ice Age: Continental Drift","Lockout","The Lorax","Madagascar 3: Europe's Most Wanted","The Odd Life of Timothy Green","ParaNorman","Premium Rush","The Raven","Resident Evil: Retribution","Safe House","Silent Hill: Revelation 3D","Wanderlust","The Watch","Wrath of the Titans","The Last Stand","Snowpiercer","Stoker","Monsters University","Carrie","Despicable Me 2","Anchorman: The Legend Continues","White House Down","Riddick","Oldboy","The Story of Luke","Stolen","Beasts of the Southern Wild","Deadfall","On the Road","The Paperboy","The Tall Man","John Dies at the End","Great Expectations","The Awakening","Shame","The Best Exotic Marigold Hotel","Moon","Fast & Furious","The Hurt Locker","Memento","Donnie Darko","Coffee and Cigarettes","American History X","Trainspotting","Reservoir Dogs","Dazed and Confused","The Shining","Noah","Guardians of the Galaxy","Teenage Mutant Ninja Turtles","Jurassic Park IV","The Expendables 3","Java Heat","Dead Man Down","Sin City: A Dame to Kill For","21 & Over","Parker","Till We Meet Again","Escape from Planet Earth","A Resurrection","The Internship","Epic","Revelation Road: The Beginning of the End","Jaws","The Man with the Golden Gun","Taxi Driver","Aliens","Platoon","Stand by Me","Predator","Back to the Future Part II","Dead Poets Society","Indiana Jones and the Last Crusade","Rain Man","Who Framed Roger Rabbit","Home Alone","Total Recall","Unforgiven","Army of Darkness","The Sandlot Kids","The Crow","Dumb & Dumber","Twelve Monkeys","Fargo","The Rock","Boogie Nights","The Fifth Element","L.A. Confidential","Liar Liar","The Lost World: Jurassic Park","Men in Black","Fear and Loathing in Las Vegas","Stepmom","Magnolia","Almost Famous","O Brother, Where Art Thou?","The Fast and the Furious","Jurassic Park III","Ocean's Eleven","Scary Movie 2","Shrek","Training Day","8 Mile","The Bourne Identity","Harry Potter and the Chamber of Secrets","Minority Report","28 Days Later...","Lost in Translation","Old School","School of Rock","X2","Cheaper by the Dozen","The Matrix Revolutions","Mystic River","Scary Movie 3","The Bourne Supremacy","The Butterfly Effect","Collateral","I, Robot","Kill Bill: Vol. 2","Million Dollar Baby","Spider-Man 2","Van Helsing","Madagascar","The Sisterhood of the Travelling Pants","Charlie and the Chocolate Factory","The Dukes of Hazzard","Fantastic Four","The Island","Serenity","War of the Worlds","The Fast and the Furious: Tokyo Drift","Inside Man","Pirates of the Caribbean: Dead Man's Chest","Scary Movie 4","Silent Hill","Blood Diamond","Harry Potter and the Order of the Phoenix","Hitman","Hot Fuzz","I Am Legend","The Mist","Pirates of the Caribbean: At World's End","Spider-Man 3","Zodiac","Hancock","Kung Fu Panda","Seven Pounds","Angels & Demons","Knowing","Couples Retreat","The Lovely Bones","The Karate Kid","Knight and Day","The Last Airbender","Megamind","Predators","Shrek Forever After","Unstoppable","Drive Angry","The Green Hornet","Hanna","Insidious","Kung Fu Panda 2","Red Riding Hood","Unknown","Your Highness","Colombiana","Extremely Loud & Incredibly Close","Killer Elite","The Muppets","Puss in Boots","Tower Heist","War Horse","Act of Valor","The Cold Light of Day","Frankenweenie","Gone","Journey 2: The Mysterious Island","The Lucky One","Mirror Mirror","Paranormal Activity 4","The Possession","The Raid","Trouble with the Curve","Underworld: Awakening","The Woman in Black","American Mary","The World's End","The Expatriate","Lay the Favorite","Robot & Frank","Would You Rather","Bullet to the Head","Gambit","Red Lights","Arbitrage","The Baytown Outlaws","The Tree of Life","Killer Joe","Winter's Bone","The Road","In Bruges","Sunshine","Children of Men","The Machinist","Like Minds","Equilibrium","Lock, Stock and Two Smoking Barrels","Interstellar","Godzilla","Before Midnight","The Heat","The Conjuring","The Rocky Horror Picture Show","Monty Python and the Holy Grail","The Exorcist","Rocky","Superman","The Thing","Terms of Endearment","Indiana Jones and the Temple of Doom","The NeverEnding Story","The Lost Boys","Spaceballs","Beetlejuice","Batman","The Godfather: Part III","Basic Instinct","A Few Good Men","The Secret Garden","True Romance","What's Eating Gilbert Grape","True Lies","Die Hard: With a Vengeance","Friday","Hackers","From Dusk Till Dawn","The Neverending Story III","A Time to Kill"]

titles2 = ["Like Someone in Love","Narenji Poush"]


for s in range(0, len(titles)):
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
        data['title'] = str(movieTitle)
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
        data['director'] = director   
        scraperwiki.sqlite.save(unique_keys=["id"], data=data)
        scraperwiki.sqlite.save_var('upto', s)
    except:
        print 'Nah, no movie called ' + titles[s]
    time.sleep(2)



