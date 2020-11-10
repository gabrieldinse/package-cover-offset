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
import cv2

# Local application imports
from Helper import ProductInfo, SegmentationInfo, ProductType, ProductTypeName


class DataStorager:
    def __init__(self):
        self.connection = mariadb.connect(
            host='localhost',
            user='root',
            password='123456',
            database='controle_producao'
        )
        self.cursor = self.connection.cursor()
        self.started = False

    def start(self, product_type_id, production_id=None):
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

    def add_product_type(self, product_type : ProductType):
        segmentation_info = product_type.segmentation_info
        self.cursor.execute(f'''
            INSERT INTO tipo_produto
                (NomeProduto, HueMin, HueMax, SaturationMin, SaturationMax,
                 ValueMin, ValueMax, FiltroGaussiano, FiltroAbertura)
            VALUES
                ("{product_type.name}", {segmentation_info.min_h},
                 {segmentation_info.max_h}, {segmentation_info.min_s},
                 {segmentation_info.max_s}, {segmentation_info.min_v},
                 {segmentation_info.max_v},
                 {segmentation_info.gaussian_filter_size},
                 {segmentation_info.openning_filter_size})
        ''')
        self.connection.commit()
        product_type_id = self.cursor.lastrowid
        cv2.imwrite(f"Data/template/{product_type_id}.png",
                    product_type.template)
        return product_type_id

    def get_product_types_names(self):
        self.cursor.execute(f'''
            SELECT Id, NomeProduto FROM tipo_produto
        ''')
        product_types_names = []
        for product_type_name in self.cursor:
            product_types_names.append(ProductTypeName(*product_type_name))
        return product_types_names

    def get_product_type(self, product_type_id):
        self.cursor.execute(f'''
            SELECT
                (NomeProduto, HueMin, HueMax, SaturationMin, SaturationMax,
                 ValueMin, ValueMax, FiltroGaussiano, FiltroAbertura) 
            FROM tipo_produto
            WHERE
                Id == {product_type_id}
        ''')
        row = list(self.cursor.__iter__())[0]
        product_type_id = row[0]
        template = cv2.imread(f"Data/template/{product_type_id}.png")
        product_type = ProductType(
            row[0], SegmentationInfo(*row[1:-1]), template)
        return product_type

    def add_product(self, product_info : ProductInfo):
        if self.started:
            self.cursor.execute(f'''
                INSERT INTO produto
                    (Offset, TemTampa, ProduzidoEm)
                VALUES
                    ({product_info.offset},
                     {int(product_info.has_cover)},
                     "{product_info.datetime_produced}")
            ''')
            product_id = self.cursor.lastrowid

            self.cursor.execute(f'''
                INSERT INTO produto_producao
                    (IdProducao, IdProduto)
                VALUES 
                    ({self.production_id}, {self.last_product_id})
            ''')
            self.connection.commit()
            return product_id
        else:
            raise RuntimeError("Produção não foi iniciada ainda")

    def stop(self):
        self.started = False

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
