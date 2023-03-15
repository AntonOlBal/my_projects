try:
    number_friends = int(input("Введите количество друзей "))
    friends_balans_list = []
    for friend in range(1, number_friends + 1):
        friends_balans_list.append("0")
    number_reciepts = int(input("Введите количество долговых расписок "))
    for transactions in range(number_reciepts):
        data_from_user = input("Введите последовательно через пробел:\nНомер друга взявшего в долг Номер друга давшего "
                               "в долг Сумма\nПример: 1 3 150\n")
        data_from_user_list = data_from_user.split()
        friend_who_took = int("".join(data_from_user_list[0]))
        friend_who_gave = int("".join(data_from_user_list[1]))
        transaction_amount = int("".join(data_from_user_list[2]))
        if friend_who_took == friend_who_gave:
            print("Человек не может занять сам у себя, попробуйте еще раз")
            break
        friends_balans_list[friend_who_took-1] = str(int("".join(friends_balans_list[friend_who_took-1])) -
                                                     transaction_amount)
        friends_balans_list[friend_who_gave-1] = str(int("".join(friends_balans_list[friend_who_gave-1])) +
                                                     transaction_amount)
    for index, total_amount in enumerate(friends_balans_list, 1):
        if friend_who_took == friend_who_gave:
            break
        else:
            print(f"Друг № {index} : {total_amount}")
except (ValueError, NameError, IndexError):
    print('Ошибка: вы ввели не число или ошиблись при вводе')