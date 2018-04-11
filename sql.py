import MySQLdb
import main

conn = MySQLdb.connect(host='sql139.main-hosting.eu',
                       port=3306,
                       user='u356390377_admin',
                       passwd='rootroot1',
                       db='u356390377_vibor')

cursor = conn.cursor()

conn.set_character_set('utf8')
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')


def take_data_from_db(chat_id, message):
    row = ['', '', '', '', '', '', '']
    conn = MySQLdb.connect(host='sql139.main-hosting.eu',
                           port=3306,
                           user='u356390377_admin',
                           passwd='rootroot1',
                           db='u356390377_vibor')
    cursor = conn.cursor()
    conn.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    main.login = False
    login = message
    if(login[:-10] == '+7'):
        login = '8'+login[2:]
    print(login)
    cursor.execute('SELECT * FROM u356390377_vibor.usersdb WHERE Number = \'{}\''.format(login))
    row = cursor.fetchone()
    if row == None:
        print("In except")
        main.send_message(chat_id, "Неправильный логин!")
        main.open_sing_in_payers(chat_id)
    else:
        print(row)
        list_of_pays = [
            ('50-50', row[3]),
            ('Aktay', row[3]),
            ('Atyray', row[3]),
            ('Semya', row[3])
        ]
        for i in list_of_pays:
            cursor.execute("SELECT * FROM `{}` WHERE Name = '{}';".format(i[0], i[1]))
            data = cursor.fetchone()
            if data is None:
                continue
            print(data)
            cursor.execute("SELECT COUNT(Name) FROM {}".format(i[0]))
            count = cursor.fetchall()
            count_of_payers = str(count[0][0])
            send = "Здравствуйте, {}! Сейчас пайщиков в кооперативе: {}. ".format(data[0], count_of_payers)
            #print(data)
            if data[3] == -1:
                send += "Вы получили недвижимость на сумму {} тенге. " \
                        "Ваш ежемесячный паевый взнос состовляет {} тенге. "\
                    .format(data[1], data[2])
            else:
                send += "Ваша запрашиваемая сумма недвижимости состовляет {} тенге. " \
                        "Ваш паевый взнос состовляет {} тенге." \
                        "Ваше место в очереди: {}".format(data[1], data[2], data[3])
            main.send_message(chat_id, send)
            break
    conn.close()

