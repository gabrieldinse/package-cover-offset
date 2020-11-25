# Author: Gabriel Dinse
# File: ProductsDatabase
# Date: 20/03/2020
# Made with PyCharm

# Standard Library
import datetime
import os

# Third party modules
import mysql.connector as mariadb
import cv2

# Local application imports
from Miscellaneous.Helper import (Product, SegmentationInfo, ProductType,
                                  ProductTypeName)
from Miscellaneous.Errors import TemplateReadingError, TemplateWritingError

class DataStorager:
    def __init__(self, ):
        self.started = False
        self.database_opened = False
        self.template_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "templates")

    def open_database(self):
        if not self.database_opened:
            self.connection = mariadb.connect(
                host='localhost',
                user='root',
                password='123456',
                database='controle_producao'
            )
            self.cursor = self.connection.cursor()
            self.database_opened = True
        else:
            pass

    def close_database(self):
        if self.database_opened:
            self.cursor.close()
            self.connection.close()
        else:
            pass

    def start_production(self, product_type_id, production_id=None):
        if self.database_opened:
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
        else:
            pass

    def stop_production(self):
        self.started = False

    def add_product_type(self, product_type : ProductType):
        if self.database_opened:
            segmentation_info = product_type.segmentation_info
            self.cursor.execute(f'''
                INSERT INTO tipo_produto
                    (NomeProduto, LowerCanny, UpperCanny, FiltroGaussiano)
                VALUES
                    ("{product_type.name}", {segmentation_info.lower_canny},
                      {segmentation_info.upper_canny},
                      {segmentation_info.gaussian_filter_size})
            ''')
            self.connection.commit()
            product_type_id = self.cursor.lastrowid
            if not cv2.imwrite(
                    os.path.join(self.template_path, f"{product_type_id}.png"),
                        product_type.template):
                raise FileWritingError("Error when saving template file")
            return product_type_id
        else:
            pass

    def get_product_types_names(self):
        if self.database_opened:
            self.cursor.execute(f'''
                SELECT Id, NomeProduto FROM tipo_produto
            ''')
            product_types_names = []
            for product_type_name in self.cursor:
                product_types_names.append(ProductTypeName(*product_type_name))
            return product_types_names
        else:
            pass

    def get_product_type(self, product_type_id):
        if self.database_opened:
            self.cursor.execute(f'''
                SELECT
                    NomeProduto, LowerCanny, UpperCanny, FiltroGaussiano
                FROM tipo_produto
                WHERE
                    Id = {product_type_id}
            ''')
            row = next(self.cursor)
            template = cv2.imread(
                os.path.join(self.template_path, f"{product_type_id}.png"), 0)
            if template is None:
                raise TemplateReadingError("Error when opening template file")
            product_type = ProductType(
                row[0], SegmentationInfo(*row[1:]), template)
            return product_type
        else:
            pass

    def add_product(self, product : Product):
        if self.database_opened:
            if self.production_started:
                self.cursor.execute(f'''
                    INSERT INTO produto
                        (Offset, TemTampa, ProduzidoEm)
                    VALUES
                        ({product.offset},
                         {int(product.has_cover)},
                         "{product.datetime_produced}")
                ''')
                product_id = self.cursor.lastrowid

                self.cursor.execute(f'''
                    INSERT INTO produto_producao
                        (IdProducao, IdProduto)
                    VALUES
                        ({self.production_id}, {product_id})
                ''')
                self.connection.commit()
                return product_id
            else:
                raise RuntimeError("Produção não foi iniciada ainda")
        else:
            pass
