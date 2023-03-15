import random


class House:
    money = 100
    food_for_human = 50
    food_for_cat = 30
    dirty = 0
    fur_coat = 0
    earned = 0
    food_eaten = 0
    cat_ate = 0

    def __init__(self, family_list):
        self.family = family_list

    @staticmethod
    def pollution():
        if House.dirty >= 0:
            House.dirty += 5
        else:
            House.dirty = 0

    def life(self):
        for i_resident in self.family:
            if House.dirty >= 90 and not isinstance(i_resident, Cat):
                i_resident.happiness_level -= 10

            if isinstance(i_resident, Cat) and House.food_for_cat >= 20 \
                    and i_resident.satiety <= 20:
                i_resident.eat()
                print(f'\n{i_resident.name} поел')
                House.cat_ate += 10
            elif isinstance(i_resident, Cat):
                if random.randint(1, 2) == 1:
                    i_resident.make_chaos()
                    print(f'\n{i_resident.name} сделал chaos')
                else:
                    i_resident.sleep()
                    print(f'\n{i_resident.name} спит')
            elif House.food_for_human >= 60 and i_resident.satiety <= 30:
                i_resident.eat()
                print(f'\n{i_resident.name} ПОКУШАВА')
                House.food_eaten += 30
            elif isinstance(i_resident, Husband):
                if House.money <= 150:
                    i_resident.work()
                    print('\nЭкстренная работа')
                    House.earned += 150
                elif i_resident.happiness_level <= 50:
                    i_resident.play()
                    print('\nРАсслабляется')
                elif i_resident.happiness_level <= 70:
                    i_resident.stroke()
                    print(f'{i_resident.name} гладит кота')
                else:
                    i_resident.work()
                    print('\nОбычная работа')
                    House.earned += 150
            elif isinstance(i_resident, Wife):
                if House.food_for_human <= 60:
                    if House.money <= 100:
                        print(f'\n{i_resident.name} Требует деньги на еду! \nВозможна голодная смерть')
                    else:
                        i_resident.by_prod_for_human()
                        print(f'\n{i_resident.name} купила еды домой')
                elif House.food_for_cat <= 20:
                    if House.money <= 50:
                        print(f'\n{i_resident.name} Требует деньги на еду коту! \nВозможна голодная смерть')
                    else:
                        i_resident.by_prod_for_cat()
                        print(f'\n{i_resident.name} купила еды коту')
                elif House.dirty >= 50:
                    i_resident.clean()
                    if House.dirty <= 0:
                        House.dirty = 0
                        print('\nПрибралась в МИНУС')
                    else:
                        print('\nПрибралася')
                elif i_resident.happiness_level <= 70:
                    i_resident.stroke()
                    print('\nЖена гладит кота')
                elif House.money >= 450:
                    i_resident.by_fur_coat()
                    print('\nКупила ШУБУ')
                    House.fur_coat += 1
                else:
                    i_resident.stroke()
                    print('\nЖена гладит кота')
            elif isinstance(i_resident, Children):
                if random.randint(1, 3) == 1:
                    i_resident.cray()
                    print(f'\n{i_resident.name} ОРЕТ')
                elif i_resident.happiness_level <= 40:
                    i_resident.play_parents()
                    print(f'\n{i_resident.name} играет с родителями')
                else:
                    i_resident.make_pope()
                    print(f'\n{i_resident.name} НАКАКАЛ')

            print(f'\nПоказатели {i_resident.name}')
            print(f'Сытость: {i_resident.satiety}')
            if not isinstance(i_resident, Cat):
                print(f'Уровень счастья: {i_resident.happiness_level}')


class Residents:
    def __init__(self, name=None, satiety=None, happiness_level=None):
        self.satiety = satiety
        self.name = name
        self.happiness_level = happiness_level

    def eat(self):
        self.satiety += 30
        House.food_for_human -= 30

    def stroke(self):
        self.satiety -= 10
        self.happiness_level += 5


class Husband(Residents):

    def __init__(self, name, satiety=30, happiness_level=100):
        super().__init__(name, satiety, happiness_level)

    def play(self):
        self.satiety -= 10
        self.happiness_level += 20

    def work(self):
        self.satiety -= 10
        House.money += 150


class Wife(Residents):

    def __init__(self, name, satiety=30, happiness_level=100):
        super().__init__(name, satiety, happiness_level)

    def by_prod_for_human(self):
        self.satiety -= 10
        House.food_for_human += 100
        House.money -= 100

    def by_prod_for_cat(self):
        self.satiety -= 10
        House.food_for_cat += 50
        House.money -= 50

    def clean(self):
        self.satiety -= 10
        House.dirty -= 100

    def by_fur_coat(self):
        self.satiety -= 10
        House.money -= 350
        self.happiness_level += 60


class Children(Residents):

    def __init__(self, name, satiety=15, happiness_level=100):
        super().__init__(name, satiety, happiness_level)

    def cray(self):
        self.happiness_level -= 20
        self.satiety -= 10

    def play_parents(self):
        self.happiness_level += 40
        self.satiety -= 10

    def make_pope(self):
        House.dirty += 25
        self.satiety -= 10
        self.happiness_level += 10


class Cat(Residents):

    def __init__(self, name, satiety=30):
        super().__init__(name, satiety)

    def eat(self):
        self.satiety += 20
        House.food_for_cat -= 10

    def sleep(self):
        self.satiety -= 10

    def make_chaos(self):
        self.satiety -= 10
        House.dirty += 5


def life_death(family_list):
    for i_elem in family_list:
        if i_elem.satiety <= 0:
            print(f'{i_elem.name} Умер от голода')
            return True
        elif not isinstance(i_elem, Cat):
            if i_elem.happiness_level <= 0:
                print(f'{i_elem.name} Умер от дипрессии')
                return True


husband = Husband('Anton')
wife = Wife('Darya')
cat = Cat('Benedict')
husband2 = Husband('Dimanchik', 15, 50)
wife2 = Wife('Masha', 5, 35)
cat2 = Cat('Barsik', 10)
cat3 = Cat('Daemon', 10)
cat4 = Cat('Gomuncul', 10)
cat5 = Cat('Vasya', 10)
husband3 = Husband('Tolya', 15, 50)
wife3 = Wife('Lena', 5, 35)
children = Children('Sonya')
my_family_list1 = [husband, wife, cat]
my_family_list2 = [husband2, wife2, cat2]
long_family = [husband3, wife3, cat, cat2, cat3, cat4, cat5, children]
family_with_children = [husband, wife, cat, children]
house = House(my_family_list1)
house2 = House(my_family_list2)
house3 = House(long_family)
house4 = House(family_with_children)

for i_day in range(1, 366):
    print(f'День {i_day}')
    House.pollution()
    if life_death(family_with_children):
        print('ЭКСПЕРЕМЕНТ НЕ УДАЛСЯ')
        break
    else:
        house4.life()
        print(f'\nОсталось еды человечей:{House.food_for_human}'
              f'\nОсталось сухарей:{House.food_for_cat}'
              f'\nОсталось денег:{House.money}'
              f'\nГрязи:{House.dirty}\n')

print('\nЗа год:'
      f'\nКуплено шуб:{House.fur_coat}'
      f'\nЗаработано:{House.earned}'
      f'\nСъедено людьми:{House.food_eaten}'
      f'\nСъедено котом:{House.cat_ate}')
