x = input("Твое число...  \n 1 - равно \n 2- больше \n 3 - меньше \n" "чем " + "50" + "?" "\n Ответ...")
if x in "1":
    print("Вы загадали 50")
if x in "3":
    for i in reversed(range(50)):
        i = str(i)
        x = input("Твое число...  \n 1 - равно \n 2- больше \n 3 - меньше \n" "чем " + i + "?" "\n Ответ...")
        if x in "1":
            print("Вы загадали " + i)
            break
if x in "2":
    for i in range(51,101):
        i = str(i)
        x = input("Твое число...  \n 1 - равно \n 2- больше \n 3 - меньше \n" "чем " + i + "?" "\n Ответ...")
        if x in "1":
            print("Вы загадали " + i)
            break
