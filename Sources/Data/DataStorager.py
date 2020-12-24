# Author: Gabriel Dinse
# File: ProductsDatabase
# Date: 20/03/2020
# Made with PyCharm


# Standard Library
import datetime
import io
from typing import List, Tuple

# Third party modules
from ftplib import FTP
import mysql.connector as mariadb
import numpy as np
import cv2

# Local application imports
from Miscellaneous.Errors import (DatabaseNotOpenedError,
                                  NotLoggedInToFTPServerError,
                                  ProductionNotStartedError)
from Miscellaneous.Helper import (Product, SegmentationInfo, ProductType,
                                  ProductTypeName, is_empty, full_filepath)


class TemplateFromBytes:
    def __init__(self):
        self.data = b""

    def __call__(self, data: bytes) -> None:
        self.data += data


class DataStorager:
    def __init__(self):
        self.started = False
        self.database_opened = False
        self.template_path = full_filepath("Templates")
        self.logged_in_to_ftp = False

    def open_database(self) -> None:
        if not self.database_opened:
            self.connection = mariadb.connect(
                host='localhost',
                user='root',
                password='123456',
                database='controle_producao'
            )
            self.cursor = self.connection.cursor()
            self.database_opened = True

    def login_to_ftp_server(self) -> None:
        self.ftp_client = FTP("127.0.0.1")
        self.ftp_client.login(user="admin", passwd="admin")
        self.ftp_client.cwd("/")
        self.logged_in_to_ftp = True

    def close_database(self) -> None:
        if self.database_opened:
            self.cursor.close()
            self.connection.close()

    def logout_from_ftp_server(self) -> None:
        self.ftp_client.close()

    def start_production(self, product_type_id: int,
                         production_id: int=None) -> None:
        if not self.database_opened:
            raise DatabaseNotOpenedError("Should open database first.")

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

    def stop_production(self) -> None:
        self.started = False

    def add_product_type(self, product_type: ProductType) -> int:
        if not self.database_opened:
            raise DatabaseNotOpenedError("Should open database first.")

        if not self.logged_in_to_ftp:
            raise NotLoggedInToFTPServerError(
                "Should log in to FTP server first.")

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

        success, buffer_array = cv2.imencode(".png", product_type.template)
        template_bytes = buffer_array.tobytes()
        self.ftp_client.storbinary(
            "STOR " + f"{product_type_id}.png", io.BytesIO(template_bytes))

        return product_type_id

    def edit_product_type(self, product_type_id: int,
                          product_type: ProductType,
                          edit_template=True) -> None:
        if not self.database_opened:
            raise DatabaseNotOpenedError("Should open database first.")

        segmentation_info = product_type.segmentation_info
        self.cursor.execute(f'''
            UPDATE tipo_produto
            SET
                NomeProduto = "{product_type.name}",
                LowerCanny = {segmentation_info.lower_canny},
                UpperCanny = {segmentation_info.upper_canny},
                FiltroGaussiano = {segmentation_info.gaussian_filter_size}
            WHERE
                Id = {product_type_id}
        ''')
        self.connection.commit()

        if edit_template:
            success, buffer_array = cv2.imencode(".png", product_type.template)
            template_bytes = buffer_array.tobytes()
            self.ftp_client.storbinary(
                "STOR " + f"{product_type_id}.png", io.BytesIO(template_bytes))

    def get_product_types_names(self) -> List[Tuple]:
        if not self.database_opened:
            raise DatabaseNotOpenedError("Should open database first.")

        self.cursor.execute(f'''
            SELECT Id, NomeProduto FROM tipo_produto
        ''')
        product_types_names = []
        for product_type_name in self.cursor:
            product_types_names.append(ProductTypeName(*product_type_name))
        return product_types_names


    def get_product_type(self, product_type_id: int) -> ProductType:
        if not self.database_opened:
            raise DatabaseNotOpenedError("Should open database first.")

        self.cursor.execute(f'''
            SELECT
                NomeProduto, LowerCanny, UpperCanny, FiltroGaussiano
            FROM tipo_produto
            WHERE
                Id = {product_type_id}
        ''')
        row = next(self.cursor)

        template_from_bytes = TemplateFromBytes()
        self.ftp_client.retrbinary(
            "RETR " + f"{product_type_id}.png", template_from_bytes)
        template = cv2.imdecode(
            np.frombuffer(
                template_from_bytes.data, dtype=np.uint8),
            cv2.IMREAD_GRAYSCALE)

        product_type = ProductType(
            row[0], SegmentationInfo(*row[1:]), template)
        return product_type

    def add_product(self, product: Product) -> int:
        if not self.database_opened:
            raise DatabaseNotOpenedError("Should open database first.")

        if not self.production_started:
            raise ProductionNotStartedError(
                "Production should be started first")

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
