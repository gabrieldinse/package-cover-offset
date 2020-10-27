# Author: Gabriel Dinse
# File: mariadb_acess
# Date: 20/03/2020
# Made with PyCharm

# Standard Library
import datetime
import time
import random

# Third party modules
import mysql.connector as mariadb


# Local application imports


def main():
    """
    
    :return:
    :rtype:
    """
    mariadb_connection = mariadb.connect(
        host='localhost',
        user='root',
        password='123456',
        database='classificador_laranjas'
    )
    cursor = mariadb_connection.cursor()
    random.seed(10)

    colors_name = [
        "Verde", "Amarelo Esverdeado", "Amarelo", "Laranja Claro", "Laranja"
    ]

    for harvest_number in range(10):  # Ten harvests
        harvest_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(f'''
            INSERT INTO colheita (IniciadaEm) VALUES ("{harvest_datetime}")
        ''')
        last_harvest_id = cursor.lastrowid

        for orange_number in range(5):  # Five oranges per harvest
            cci = random.uniform(-5.0, 5.0)
            diameter = random.uniform(0.0, 100.0)
            cursor.execute(f'''
                INSERT INTO laranja
                    (Iluminante, CCI, NomeCor, Diametro)
                VALUES
                    ("D65", {cci}, "{color_name}", {diameter})
            ''')
            last_orange_id = cursor.lastrowid

            cursor.execute(f'''
                INSERT INTO laranja_colheita
                    (IdColheita, IdLaranja)
                VALUES 
                    ({last_harvest_id}, {last_orange_id})
            ''')

        time.sleep(0.5)

    mariadb_connection.commit()
    mariadb_connection.close()


if __name__ == "__main__":
    main()
