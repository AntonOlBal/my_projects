# TODO ты должен был сделать класс Человек (Human) и наследовать методы от него. Схема такая:

class Human():
    def __init__(self, name, degree_satiety, degree_happines):  # TODO его начальные атрибуты (имя, уровень сытости, уровень счастья)
        self.name = name
        self.degree_satiety = degree_satiety
        self.degree_happines = degree_happines

    def eat(self):
        pass

    def petting_cat(self):
        pass

    def chek_degree_satiety(self):
        degree_satirty_now = self.degree_satiety
    
    def chek_degree_happines(self):
        degree_happines_now = self.degree_happines
    
    

    def __str__(self):
        about_me = f'Я - {self.name}, сытость - {self.degree_satiety}, уровень счастья - {self.degree_happines}'
        return about_me

    


    # TODO так же добавь методы класса на проверку грязи, еды, денег и метод действия, в зависимости от условия


class Husband(Human):
    def play(self):
        pass

    def job(self):
        pass


class Wife(Human):
    def buy_product(self):
        pass

    def buy_fur_coat(self):
        pass
    
    def cleaning_house(self):
        pass


class Cat:
    pass


class Home:
    pass


# TODO сделай функцию для вывода итогов дня, например print_info
# TODO сделай лог каждого дня по типу ниже

# День  365
# Антон работает...
# Даша ест...
# Беня спит...
# ---------- Итоги дня ----------
# Я - Антон, сытость - 20, степень счастья - 55
# Я - Даша, сытость - 50, степень счастья - 100
# Я - Беня, сытость - 10
#
# В доме осталось:
# 4382 еды
# 5129 еды для кота
# 25128 денег
# 30 грязи
#
# --------Итоги за год--------
# Денег заработано -  41100
# Еды съедено -  5430
# Шуб куплено -  0

# TODO все условия действия запиши в метод action у экземпляров
#  условно сама программа должна выглядеть таким образом,
#  все переменные объявляй после классов и функций и обрати внимание на свою орфографию:

# сначала все классы
# далее функции
# далее уже создаешь объекты

# home = Home()
# husband = Husband(name='Антон')
# wife = Wife(name='Даша')
# cat = Cat(name='Беня')

# print(husband)
# print(wife)
# print(cat)
#
# for day in range(1, 366):
#     print()
#     print('День ', day)
#     husband.action()
#     wife.action()
#     cat.action()
#     print_info()
#     if day == 365:
#         print('\n--------Итоги за год--------')
#         print('Денег заработано - ', home.total_earned)
#         print('Еды съедено - ', home.all_eaten)
#         print('Шуб куплено - ', wife.cnt_fur_coat)
#
#     if not husband.check_alive() or not wife.check_alive() or not cat.check_alive():
#         break

# TODO Твоя реализация не особо ооп и явно люди не должны быть объекты класса дом.
#  Удачи в написании хорошего и красивого кода

class House:
    def __init__(self, name):
        self.name = name

    money = 100
    food = 50
    food_cat = 30
    amount_dirt = 0


my_home = House("Home")


class Husbend(House):
    degree_satiety_husbend = 30
    degree_happines_husbend = 100
    amount_money = 0
    amount_eat_husbend = 0

    def job(self):
        House.money += 150
        Husbend.degree_satiety_husbend -= 10
        Husbend.amount_money += 150

    def eat_husbent(self):
        House.food -= 30
        Husbend.degree_satiety_husbend += 30
        Husbend.amount_eat_husbend += 30

    def play(self):
        Husbend.degree_satiety_husbend -= 10
        Husbend.degree_happines_husbend += 20

    def petting_cat(self):
        Husbend.degree_happines_husbend += 5
        Husbend.degree_satiety_husbend -= 10


husbend = Husbend("Anton")


class Wife(House):

    degree_happines_wife = 100
    degree_satiety_wife = 30
    amount_fur_coat = 0
    amount_eat_wife = 0

    def eat_wife(self):
        House.food -= 30
        Wife.degree_satiety_wife += 30
        Wife.amount_eat_wife += 30

    def buy_product(self):
        Wife.degree_satiety_wife -= 10
        House.food += 60
        House.food_cat += 5
        House.money -= 65

    def buy_fur_coat(self):
        House.money -= 350
        Wife.degree_satiety_wife -= 10
        Wife.degree_happines_wife += 60
        Wife.amount_fur_coat += 1

    def cleaning_house(self):
        Wife.degree_satiety_wife -= 10
        House.amount_dirt -= 100

    def petting_cat(self):
        Wife.degree_happines_wife += 5
        Wife.degree_satiety_wife -= 10


wife = Wife("Darya")


class Cat(House):
    degree_satiety_cat = 30
    amount_eat_cat = 0

    def eat_cat(self):
        House.food_cat -= 10
        Cat.degree_satiety_cat += 20
        Cat.amount_eat_cat += 10

    def sleep(self):
        Cat.degree_satiety_cat -= 10

    def tear_up_wallpaper(self):
        Cat.degree_satiety_cat -= 10
        House.amount_dirt += 5


cat = Cat("Benedikt")

# TODO это плохая реализация
for days in range(1, 366):
    House.amount_dirt += 5
    if Husbend.degree_satiety_husbend < 20:
        husbend.eat_husbent()
    elif Husbend.degree_satiety_husbend > 10 and Husbend.degree_happines_husbend > 20:
        husbend.job()
    elif Husbend.degree_happines_husbend < 30:
        husbend.play()
    if Wife.degree_satiety_wife < 20:
        wife.eat_wife()
    elif House.food < 70 and Wife.degree_happines_wife > 20:
        wife.buy_product()
    elif House.amount_dirt > 100:
        wife.cleaning_house()
    elif Wife.degree_happines_wife < 30 and House.money > 410:
        wife.buy_fur_coat()
    elif Wife.degree_happines_wife < 20:
        wife.petting_cat()
    if Cat.degree_satiety_cat < 20:
        cat.eat_cat()
    else:
        cat.sleep()
    if Husbend.degree_satiety_husbend == 0 or Wife.degree_satiety_wife == 0 or Cat.degree_satiety_cat == 0:
        print("Один из членов семьи погиб от голода :(")
        break
    if House.amount_dirt > 90:
        Wife.degree_happines_wife -= 10
        Husbend.degree_happines_husbend -= 10
    if Husbend.degree_happines_husbend < 10 or Wife.degree_happines_wife < 10:
        print("Один из членов семьи погиб от дипрессии :(")
        break
else:
    print(f"Итоги года: \n{Husbend.amount_money} рублей было заработанно\n{Wife.amount_fur_coat} шуб куплено\n"
          f"{(Husbend.amount_eat_husbend + Wife.amount_eat_wife + Cat.amount_eat_cat)} единиц еды съедено\nВсе остались живы, ура!")



