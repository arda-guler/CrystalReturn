import string
import random

poem1 = ["",
         "AT THE SHORES OF PAST",
         "BEHIND THE CRYSTAL WINDOW",
         "IT IS SO FAR AWAY",
         "IT IS SO FAMILIAR",
         "IN THE AFTERMATH",
         "WHERE ALL COMES TOGETHER",
         "THE CLOUD IS NO MORE",
         "ALL IS CRYSTAL CLEAR"]

poem2 = ["",
         "MOONLIGHT IN SILENCE",
         "MISTY PATH",
         "ENCOUNTER",
         "BEAUTIFUL INCIDENT",
         "COMPASSION",
         "THE SHADOW OF LOVE"]

poem3 = ["",
         "THE LANTERN, MY COMPANY, SUDDENLY MET ITS DOOM",
         "IN AN INSTANT I AM LEFT IN A QUITE COLD GLOOM",
         "RAIN POURING DOWN DEEP INTO THE LATE NIGHT",
         "PASSING RIGHT AHEAD IS A SINGLE FAINT LIGHT",
         "IF, WANDER AWAY NOW, IT IS GOING TO NOT",
         "FOLLOW CLOSELY I SHALL, STAYING A BIT BEHIND",
         "BUT, ON THE PATHWAY, I SEEM TO BE ALREADY",
         "AT MY DESTINATION, WHO KNOWS, I MIGHT VERY WELL BE",
         "JUST ACROSS THE ROAD, HE WOULD OF COURSE KNOW ME",
         "HE WOULD APPRECIATE VERY MUCH THIS TIMELY VISIT TO THEE",
         "LETS SEE WHETHER THE ROOM IS LIT BRIGHT STILL",
         "OR RESTING HE MAY BE, PERHAPS FALLEN ILL"]

poem4 = ["",
         "THE CHILL OF A SEPTEMBER MORNING",
         "THE CHILL OF THE LEAVES",
         "I FILL INTO MY CHEST",
         "THE SERENITY AND THE QUIET",
         "MERGES INTO ONE",
         "THE BATHING DOVES",
         "THE SOUND OF A DISTANT TRAIN",
         "THE URGE TO START OVER",
         "ENVELOPS MY HEART",
         "EACH TIME I WAKE UP"]

poem5 = ["",
         "WHEN IT IS TIME TO WEIGH THE ANCHORS",
         "A SHIP DEPARTS FROM HERE TO THE UNKNOWNS",
         "IT SAILS AS IF THERE IS NO ONE ABOARD",
         "NONE WAVES A HAND, IT MOVES ONWARD",
         "THOSE LEFT ON THE SHORE ARE DEEPLY IN SORROW",
         "STARING AT THE HORIZON WITH A SILENT DARK GLOW",
         "POOR SOULS, FOR THIS IS NOT THE LAST SHIP",
         "THERE WILL SOON BE MORE SAILING TOWARDS THE DEEP",
         "LOVERS AWAIT THEIR BELOVED, LOOKING AT ITS STERN",
         "FUTILE, FOR THOSE WHO LEFT ARE NEVER GOING TO RETURN",
         "TRAVELLERS SEEM PLEASED WITH THEIR DESTINATION",
         "MANY YEARS HAVE PASSED, RETURNS ARE ON STAGNATION"]

poem6 = ["",
         "WHILE YOU LIVE, SHINE",
         "HAVE NO GRIEF AT ALL",
         "LIFE IS ONLY FOR A SHORT WHILE",
         "AND TIME WILL TAKE ITS TOLL"]

poem7 = ["",
          "SOMEWHERE AFTER MIDNIGHT",
          "IN MY WILDEST FANTASY",
          "SOMEONE JUST BEYOND MY REACH",
          "THERE'S SOMEONE REACHING BACK FOR ME"]

poem8 = ["",
          "FLY ME TO THE MOON",
          "AND LET ME PLAY AMONG THE STARS",
          "LET ME SEE WHAT SPRING IS LIKE",
          "ON JUPITER AND MARS",
          "IN OTHER WORDS",
          "HOLD MY HAND",
          "IN OTHER WORDS",
          "DARLING KISS ME",
          "FILL MY HEART WITH SONG",
          "AND LET ME SING FOREVERMORE",
          "YOU ARE ALL I LONG FOR",
          "ALL I WORSHIP AND ADORE",
          "IN OTHER WORDS",
          "PLEASE BE TRUE",
          "IN OTHER WORDS",
          "I LOVE YOU"]

poem9 = ["",
          "STANDING IN THE RAIN OF TEARS",
          "I ENGRAVE THE SEAL OF A SWEET DREAM",
          "SO AS NOT TO DISAPPEAR",
          "WHY DOES IT SMELL SO NICE",
          "A SIN-COLORED DROP DRIPS DOWN"]

poem10 = ["",
          "MAYBE, OUT OF THE BLUE",
          "WHEN I CAME BY YOU",
          "WHATEVER I SAID WERE",
          "MEANINGLESS TO YOU",
          "BUT THERE WAS NO TIME",
          "ALAS, YOU WERE RIGHT",
          "THESE KINDS OF THINGS",
          "COULDN'T HAVE BEEN RUSHED",
          "EVEN THOUGH IT WAS A LIE",
          "HOW BEAUTIFUL WAS YOUR SMILE",
          "THAT NIGHT..."]

poem11 = ["",
          "HERE IS THE PUNISHMENT",
          "BOUND TO ME FOR ETERNITY",
          "THEY ARE BUT ONLY DREAMS",
          "THE END OF THE DAY HIDES IN SHADOWS",
          "ALL ALONE I WANT TO CRY",
          "ONLY FEAR IS IN MY EYES",
          "HERE IS THE PUNISHMENT",
          "BOUND TO THIS WORLD FOR ETERNITY",
          "ALL THESE ARE JUST THE WIND",
          "I STOP FOR A MOMENT",
          "JUST A MOMENT TO CRY"]

poem12 = ["",
          "AS I IN HOARY WINTER'S NIGHT",
          "STOOD SHIVERING IN THE SNOW",
          "SURPRISED I WAS WITH SUDDEN HEAT",
          "WHICH MADE MY HEART TO GLOW",
          "AND LIFTING UP A FEARFUL EYE",
          "TO VIEW WHAT FIRE WAS NEAR",
          "A PRETTY BABE ALL BURNING BRIGHT",
          "DID IN THE AIR APPEAR",
          "WHO, SCORCHED WITH EXCESSIVE HEAT",
          "SUCH FLOOD OF TEARS DID SHED"]

poem12 = ["",
          "FLOWERS BLOOM WHEN YOU LAUGH",
          "THE BIRDS SING ABOUT YOU",
          "AND WE WOULD LISTEN",
          "THE SPRING ARRIVES WHEN YOU DO",
          "THE RIVERS CALL OUT FOR YOU",
          "AND WE WOULD SMILE",
          "WITH THE RAINS IN FALL",
          "YOU LEFT US, ONE DAY",
          "AND WE COULDN'T BELIEVE",
          "OUR HOMES SILENT",
          "OUR HOMES WITHOUT YOU",
          "IT COULDN'T BE"]

poem13 = ["",
          "FLOAT ALONG LITTLE GLASS BOTTLE",
          "CARRY MY MESSAGE, MY LAST WISH",
          "ON THE OTHER SIDE OF THE HORIZON",
          "MAYBE THIS WON'T APPEAR SO SELFISH"]

poem14 = ["",
          "WHEN YOU AWAKEN IN THE MORNING'S HUSH",
          "I AM THE SWIFT UPLIFTING RUSH",
          "OF QUIET BIRDS IN CIRCLED FLIGHT",
          "I AM THE SOFT STARS THAT SHINE AT NIGHT",
          "DO NOT STAND AT MY GRAVE AND CRY",
          "I AM NOT THERE - I DID NOT DIE"]

poem15 = ["",
          "SWEET DREAMS OF INNOCENT TIMES",
          "SEEING THROUGH THICK CLOUDS OF LIES",
          "REACHING OUT TO THE PUREST HEARTS",
          "CONNECTING THEM LIKE BINARY STARS",
          "THEN TIME COMES INTO ACTION",
          "STARS FLY AWAY IN REACTION",
          "A DIM LIGHT YET STILL VISIBLE",
          "LOVERS FAR AWAY BUT IMPARTIBLE",
          "BUT STARS ALSO DIE OUT",
          "WITH NOTHING TO ORBIT ABOUT",
          "HOWEVER THEN STARTS THE STORY",
          "OF BILLIONS ON A PLANET SO PRETTY"]

poem_list = [poem1, poem2, poem3, poem4, poem5, poem6, poem7,
             poem8, poem9, poem10, poem11, poem12, poem13, poem14,
             poem15]

death_msgs = []
death_msgs.append("TIME TAKES ITS TOLL")
death_msgs.append("ANOTHER ONE BITES THE DUST")
death_msgs.append("SO LONG AND THANKS FOR ALL THE FISH")
death_msgs.append("AND ON MARS THERE WILL BE APPLE BLOSSOMS")
death_msgs.append("CLUBBED TO DEATH")
death_msgs.append("FLY ME TO THE MOON")
death_msgs.append("ALWAYS WATCHING")
death_msgs.append("FAREWELL")
death_msgs.append("YOU HAVE PLAYED THIS GAME TOO LONG, MORTAL.")
death_msgs.append("IDDQD")
death_msgs.append("XYZZY")
death_msgs.append("AND STANLEY WAS HAPPY")
death_msgs.append("EYES ON THE ROAD")
death_msgs.append("FOR WHOM THE BELL TOLLS")
death_msgs.append("THE SOUL WOULD HAVE NO RAINBOW HAD THE EYES NO TEARS")
death_msgs.append("RAILROAD CROSSING AHEAD")
death_msgs.append("TOO LOW, TERRAIN!")
death_msgs.append("OUCH")
death_msgs.append("PERCUSSION TIME")
death_msgs.append("NON-EUCLIDIAN")
death_msgs.append("MICE ON VENUS")
death_msgs.append("dQw4w9WgXcQ")
death_msgs.append("WAVE FUNCTION COLLAPSE")
death_msgs.append("FLY SAFE")
death_msgs.append("aeiou")
death_msgs.append("MEIN LEBEN!")
death_msgs.append("ROLLED A 1.")
death_msgs.append("TRYING IS THE FIRST STEP TOWARDS FAILURE.")
death_msgs.append("Cocuklar, Mahmut Hoca burada, gelmeyin!")
death_msgs.append("LOREM IPSUM DOLOR SIT AMET")
death_msgs.append("MY BATTERY IS LOW AND IT'S GETTING DARK")
death_msgs.append("<player> WAS INCINERATED BY AN ARCHVILE")
death_msgs.append("<player> WAS SMITTEN BY A CACODEMON")
death_msgs.append("<player> EXPERIENCED KINETIC ENERGY")
death_msgs.append("<player> HIT THE GROUND TOO HARD")
death_msgs.append("<player> WAS KILLED BY MAGIC")

random_filename = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5,9)))
random_line = str(random.randint(17, 257))
random_codeline = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + " ", k=random.randint(16,75)))
death_msgs.append("An exception has occurred.\n While running game code:\n  File \"" + random_filename + ".py\", line " + random_line + ", in script\n    " + random_codeline + "\n  Exception: Never gonna give you up.")

death_msgs.append("AFTER ALL, IT'S MY HOUSE.")
death_msgs.append("DAISY, DAISY")
death_msgs.append("RESISTANCE IS FUTILE")
death_msgs.append("STRANDED? CALL THE FUEL RATS!")
death_msgs.append("ALL OTHER OBJECTIVES SECONDARY")
death_msgs.append("I HAVE BEEN, AND ALWAYS SHALL BE, YOUR FRIEND")
death_msgs.append("DON'T RUN WITH SCISSORS")
death_msgs.append("The marabou stork (Leptoptilos crumenifer) is a large species of wading bird in the stork family, Ciconiidae. Breeding in sub-Saharan Africa, it eats mainly carrion, scraps and faeces, but will opportunistically eat almost any animal matter it can swallow. It occasionally eats other birds including Quelea nestlings, pigeons and doves, pelican and cormorant chicks, and even flamingos. During the breeding season, adults scale back on carrion and take mostly small, live prey since nestlings need this kind of food to survive. Common prey at this time may consist of fish, frogs, insects, eggs, small mammals and reptiles such as crocodile hatchlings and eggs. Though known to eat putrid and seemingly inedible foods, these storks may sometimes wash food in water to remove soil. Increasingly, marabous have become dependent on human garbage and hundreds of the birds can be found around African dumps or waiting for a handout in urban areas. Those eating garbage have been seen to devour virtually anything that they can swallow, including shoes and pieces of metal, and those conditioned to eating from human sources have been known to lash out when refused food.")
death_msgs.append("The missile knows where it is at all times. It knows this because it knows where it isn't. By subtracting where it is from where it isn't, or where it isn't from where it is (whichever is greater), it obtains a difference, or deviation. The guidance subsystem uses deviations to generate corrective commands to drive the missile from a position where it is to a position where it isn't, and arriving at a position where it wasn't, it now is. Consequently, the position where it is, is now the position that it wasn't, and it follows that the position that it was, is now the position that it isn't. In the event that the position that it is in is not the position that it wasn't, the system has acquired a variation, the variation being the difference between where the missile is, and where it wasn't. If variation is considered to be a significant factor, it too may be corrected by the GEA. However, the missile must also know where it was. The missile guidance computer scenario works as follows. Because a variation has modified some of the information the missile has obtained, it is not sure just where it is. However, it is sure where it isn't, within reason, and it knows where it was. It now subtracts where it should be from where it wasn't, or vice-versa, and by differentiating this from the algebraic sum of where it shouldn't be, and where it was, it is able to obtain the deviation and its variation, which is called error.")
