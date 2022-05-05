import math

def core_pct(enrage=0, streak=0):
    if((streak-1)>math.floor(enrage/5)):
        raise Exception(f'cannot have streak of {streak} at {enrage} enrage')
    numerator = (1000+10*enrage+25*streak)
    denominator = 1000000
    unique = numerator/denominator
    uniqueInverse = 1/unique
    return uniqueInverse * 5
    
def hp(enrage=0, num_of_arms=0, num_of_minions=0):
    glacor = 370000+3700*math.floor(enrage/5)
    factor = 1
    arms = 32500 if enrage <= 2500 else 32500+325*math.floor((enrage-2500)/3.33)
    glacytes = 13500 if enrage <= 2500 else 13500+135*math.floor((enrage-2500)/2.5)
    bolstered = 0 if enrage < 250 else (27000 if enrage <= 2500 else 27000+270*math.floor(enrage-2500)/2.5)
    return glacor+(arms+glacytes+bolstered)*factor

def do_math(enrage=400, kills=20, is_streak:bool=True, avg_dpm=250):
    total_time = 0
    total_prob = 0
    for i in range(0,kills):
        streak = i if is_streak else 0
        avg_enrage_increase=11.5
        new_enrage=enrage+(avg_enrage_increase)*streak
        new_enrage = 4000 if new_enrage > 4000 else new_enrage
        hp_glacor = hp(new_enrage)
        mins = hp_glacor / (avg_dpm*1000)
        denom = core_pct(new_enrage,streak)
        total_time = total_time + mins
        prob_not_getting = 1-total_prob
        new_chance = prob_not_getting*(1/denom)
        total_prob = total_prob + new_chance
    return total_prob*100, total_time

def test():
    kills = 13
    enrage = 1040
    is_streak=True
    total_pct, total_time = do_math(enrage, kills, is_streak)
    print(f'{total_pct}% chance to get it after {kills} kills (took {total_time} mins at {enrage} enrage is_streak={is_streak})')
test()
def find_kills(enrage, is_streak=False, time=120):
    kills = 0
    total_time=0
    total_pct = 0
    while(total_time<time):
        kills = kills + 1
        total_pct, total_time = do_math(enrage, kills, is_streak)
    return total_pct, total_time, kills

increment = 20
total_mins=120

enrage = 0
best_pct = 0
best_kills = 0
best_enr = 0
is_streak = None
for i in range(0, int(4000/increment)+1):
    enrage = i*increment
    total_pct_streak, total_time_streak, kills_streak = find_kills(enrage, True, total_mins)
    total_pct_no_streak, total_time_no_streak, kills_no_streak = find_kills(enrage, False, total_mins)
    if(total_pct_streak > best_pct):
        best_pct = total_pct_streak
        best_kills = kills_streak
        is_streak = True
        best_enr = enrage
    if(total_pct_no_streak > best_pct):
        best_pct = total_pct_no_streak
        best_kills = kills_no_streak
        is_streak = False
        best_enr = enrage


print(best_pct, best_enr, best_kills, is_streak)
