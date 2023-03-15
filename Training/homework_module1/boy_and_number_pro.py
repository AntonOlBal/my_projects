start = 1
stop = 100
y = 1
while True:
    general = (start + stop)//2
    x = input(f"Попытка № {y} \nТвое число...  \n 1 - равно \n 2 - больше \n 3 - меньше \n чем {general}? \n Ответ...")
    if x in "1":
        print("Ваше число " + str(general))
        break
    elif x in "2":
        start = general + 1
        y += 1
    else:
        stop = general - 1
        y += 1