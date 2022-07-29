import configparser

# для того, чтобы не писать конфиг-файл вручную, можно воспользоваться этим модулем.
# если есть необходимость создания интерфейса для выставления настроек, то этот модуль нужно использовать.
# создание конфига проходит с помощью библиотеки configparser -> https://docs.python.org/3/library/configparser.html

config = configparser.ConfigParser()

config["A"] = {
    'width': 50,
    'alignment': {
        'horizontal': 'center'
    },
    'type': 'column'
}
config["B"] = {
    'width': 100,
    'alignment': {
        'horizontal': 'right'
    },
    'font': {
        'name': 'Calibri',
        'sz': 10,
        'italic': True
    },
    'type': 'column'
}
config["1"] = {
    'height': 20,
    'alignment': {
        'horizontal': 'center'
    },
    'font': {
        'bold': True
    },
    'type': 'row'
}

with open('config.ini', 'w') as configfile:
    config.write(configfile)
