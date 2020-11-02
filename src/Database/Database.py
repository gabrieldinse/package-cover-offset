# Author: Gabriel Dinse
# File: ProductsDatabase
# Date: 20/03/2020
# Made with PyCharm

# Standard Library
import datetime
import time
import random

# Third party modules
import mysql.connector as mariadb

# Local application imports
from Helper import ProductInfo


class Database:
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
            start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute(f'''
                INSERT INTO producao (IniciadaEm) VALUES ("{start_time}")
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


    def register_product_type(self, name, hmin, hmax, smin, smax, vmin, vmax):
        self.cursor.execute(f'''
            INSERT INTO tipo_produto
                (NomeProduto, HueMin, HueMax, SaturationMin, SaturationMax,
                 ValueMin, ValueMax)
            VALUES
                ("{name}", {hmin}, {hmax}, {smin}, {smax}, {vmin}, {vmax})
        ''')
        self.connection.commit()

    def get_product_types(self):
        self.cursor.execute(f'''
            SELECT Id, NomeProduto FROM tipo_produto
        ''')
        return self.cursor.__iter__()

    def add_product(self, product_info : ProductInfo):
        if self.production_started:
            self.cursor.execute(f'''
                INSERT INTO produto
                    (Offset, TemTampa, ProduzidoEm)
                VALUES
                    ({product_info.offset},
                     {int(product_info.has_cover)},
                     "{product_info.datetime_produced}")
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
