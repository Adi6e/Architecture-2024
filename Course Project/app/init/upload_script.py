from postgres_connector import PostgresConnector
from faker import Faker
from typing import Sequence, Mapping
import hashlib
import psycopg2.extras
from pymongo import MongoClient
from faker import Faker


class DBWorker:
    def create_new_db(self, db_name: str) -> None:
        connector: PostgresConnector = PostgresConnector()
        cursor = connector.get_cursor()
        cursor.connection.autocommit = True
        drop_command = f"DROP DATABASE IF EXISTS {db_name};"
        creation_command = f"CREATE DATABASE {db_name};"
        cursor.execute(drop_command)
        cursor.execute(creation_command)
        connector.close_connection()

    def create_tables(self, db_name: str) -> None:
        connector: PostgresConnector = PostgresConnector(db_name=db_name)
        cursor = connector.get_cursor()
        with open("./sql_script.sql", "r") as tables_creation_cript:
            cursor.execute(tables_creation_cript.read())
        cursor.connection.commit()
        connector.close_connection()

    def insert_data_to_table(self, db_name: str, table_name: str, data: Sequence[Mapping]) -> None:
        connector = PostgresConnector(db_name=db_name)
        cursor = connector.get_cursor()
        columns = data[0].keys()
        columns_str = ", ".join(columns)
        sql = f"INSERT INTO {table_name} ({columns_str}) VALUES %s"
        data_to_insert = [[i[column] for column in columns] for i in data]
        psycopg2.extras.execute_values(cursor, sql, data_to_insert)
        cursor.connection.commit()
        connector.close_connection()


class CreaterData:
    def get_fake_users(self, count: int) -> Sequence[Mapping]:
        fake: Faker = Faker()
        users: Sequence[Mapping] = []
        for _ in range(count):
            user = self.create_fake_user(fake)
            users.append(user)
        return users

    def create_fake_user(self, fake: Faker) -> Mapping:
        user: dict = {}
        user_login: str = fake.unique.user_name()
        full_name: Sequence[str] = fake.unique.name().split()[:2]
        user_name: str = full_name[0]
        user_surname: str = full_name[1]
        password: str = fake.unique.password()
        user_password: str = hashlib.sha256(password.encode()).hexdigest()
        user["user_login"] = user_login
        user["user_name"] = user_name
        user["user_surname"] = user_surname
        user["user_password"] = user_password
        return user

    def generate_fake_service(self, fake, count_of_users):
        services = []
        count = fake.unique.random_int(min=100, max=1000)
        for _ in range(count):
            title = fake.unique.sentence()
            description = fake.unique.paragraph()
            creator_id = fake.random_int(min=1, max=count_of_users)
            services.append(
                {
                    "title": title,
                    "description": description,
                    "creator_id": creator_id
                }
            )
        return services

    def generate_fake_order(self, db, count_of_users):
        fake = Faker()
        count_of_confs: int = fake.random_int(min=20, max=30)
        confs = []
        for _ in range(count_of_confs):
            name = fake.unique.company()
            service_ids = db["services"].insert_many(
                self.generate_fake_service(fake=fake, count_of_users=count_of_users)).inserted_ids
            description = fake.unique.paragraph()
            confs.append(
                {
                    "name": name,
                    "description": description,
                    "services": service_ids
                }
            )
        result = db["orders"].insert_many(confs)
        print(result)


class Uploader:
    def upload_data(self):
        print("Start initializing")
        cursor = PostgresConnector().get_cursor()
        sql = "SELECT datname FROM pg_database WHERE datname = 'service_order_db'"
        cursor.execute(sql)
        data = cursor.fetchall()
        if data:
            print(data)
            print("Database already exist")
            cursor.close()
            return
        cursor.close()
        db_worker = DBWorker()
        db_name = "service_order_db"
        creater_data = CreaterData()
        db_worker.create_new_db(db_name)
        db_worker.create_tables(db_name)
        count_of_users = 100
        fake_users: Sequence[Mapping] = creater_data.get_fake_users(
            count_of_users)
        db_worker.insert_data_to_table(
            db_name=db_name, table_name="users", data=fake_users)
        username = "root"
        password = "example"
        mongo_uri = f"mongodb://{username}:{password}@mongo:27017/"
        client = MongoClient(mongo_uri)
        db = client["arch"]
        creater_data.generate_fake_order(
            db=db, count_of_users=count_of_users)
        print("Database was created and filled")


if __name__ == "__main__":
    Uploader().upload_data()
