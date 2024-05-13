import MakeScreen

flags = [False] * 2 
start_flag = False
while True:
    f = open('./source/connection.json')
    a = f.readline()
    if flags[1] == False and a == "my_throw\n":
        cubs = f.readline().split()
        new_user_comb = f.readline().split()
        MakeScreen.roll_dice(cubs)
        MakeScreen.change_user_comb(new_user_comb)
        flags = [False] * 2
        flags[1] = True
        continue