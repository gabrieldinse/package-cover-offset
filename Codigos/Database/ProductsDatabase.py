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


class ProductsDatabase:
    def __init__(self):
        self.connection = mariadb.connect(
            host='localhost',
            user='root',
            password='123456',
            database='controle_producao'
        )
        self.cursor = self.connection.cursor()
        self.production_started = False

    def start_production(self, product_type_id, production_id=None):
        if production_id is None:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(f'''
                INSERT INTO producao (IniciadaEm) VALUES ("{now}")
            ''')
            self.production_id = self.cursor.lastrowid
        else:
            self.production_id = production_id

        self.product_type_id = product_type_id
        self.cursor.execute(f'''
            INSERT INTO producao_tipo_produto
                (IdTipoProduto, IdProducao)
            VALUES 
                ({self.product_type_id}, {self.production_id})
        ''')
        self.connection.commit()
        self.production_started = True


    def register_product_type(self, name):
        self.cursor.execute(f'''
            INSERT INTO tipo_produto
                (NomeProduto)
            VALUES
                ("{name}")
        ''')
        self.connection.commit()

    def get_product_types(self):
        self.cursor.execute(f'''
            SELECT Id, NomeProduto FROM tipo_produto
        ''')
        return self.cursor.__iter__()

    def add_product(self, offset, has_cover):
        if self.production_started:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(f'''
                INSERT INTO produto
                    (Offset, TemTampa, ProduzidoEm)
                VALUES
                    ({offset}, {int(has_cover)}, "{now}")
            ''')
            self.last_product_id = self.cursor.lastrowid

            self.cursor.execute(f'''
                INSERT INTO produto_producao
                    (IdProducao, IdProduto)
                VALUES 
                    ({self.production_id}, {self.last_product_id})
            ''')
            self.connection.commit()
        else:
            raise RuntimeError("Produção não foi iniciada ainda")

    def stop_production(self):
        self.production_started = False

    def close_connection(self):
        self.cursor.close()
        self.connection.close()


connection = ProductsDatabase()
connection.register_product_type("Produto Teste")
product_types = connection.get_product_types()
print(type(product_types))
for (id, name) in product_types:
    print(f"ID: {id}, Nome: {name}")
