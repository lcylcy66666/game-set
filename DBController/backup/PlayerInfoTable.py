from DBConnection import DBConnection

import datetime

class playerInfoTable:
    def insert_a_player(self, name):
        command = "INSERT INTO player_info (name, play_date) VALUES  ('{}','{}');".format(name, datetime.date.today())
            
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def select_all_player(self):
        command = "SELECT * FROM player_info;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()
        
        result = dict()
        for row in record_from_db:
            result[row['pl_id']] = row['name']

        return result

    def select_a_player(self, name):
        command = "SELECT * FROM player_info WHERE name='{}';".format(name)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        return [row['pl_id'] for row in record_from_db]

    def delete_a_player(self, pl_id):
        command = "DELETE FROM player_info WHERE pl_id='{}';".format(pl_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()
