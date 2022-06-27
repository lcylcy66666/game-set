from DBController.DBConnection import DBConnection

import datetime

class RankingInfoTable:
    def insert_a_data(self, name, game, score):

        nowTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        command = "INSERT INTO ranking_info (play_date, name, game, score) VALUES  ('{}','{}','{}','{}');".format(nowTime, name, game, score)
            
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def select_all_data(self):
        command = "SELECT * FROM ranking_info;"

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()
        
        result_list = list()
        for row in record_from_db:
            data = {
                'Id': row['pl_id'],
                'Date':row['play_date'],
                'Name':row['name'],
                'Game':row['game'],
                'Score': row['score']
            }
            result_list.append(data)
        
        # Doing Sort
        for i in range(len(result_list)):
            for j in range(len(result_list)-1):
                if(result_list[i]['Score'] > result_list[j]['Score']):
                    temp = result_list[i]
                    result_list[i] = result_list[j]
                    result_list[j] = temp

        return result_list

    def select_a_name_data(self, name):
        command = "SELECT * FROM ranking_info WHERE name='{}';".format(name)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        result_list = list()
        for row in record_from_db:
            data = {
                'Id': row['pl_id'],
                'Date':row['play_date'],
                'Name':row['name'],
                'Game':row['game'],
                'Score': row['score']
            }
            result_list.append(data)
        
        # Doing Sort
        for i in range(len(result_list)):
            for j in range(len(result_list)-1):
                if(result_list[i]['Score'] > result_list[j]['Score']):
                    temp = result_list[i]
                    result_list[i] = result_list[j]
                    result_list[j] = temp

        return result_list
    
    def select_a_game_data(self, game):
        command = "SELECT * FROM ranking_info WHERE game='{}';".format(game)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        result_list = list()
        for row in record_from_db:
            data = {
                'Id': row['pl_id'],
                'Date':row['play_date'],
                'Name':row['name'],
                'Game':row['game'],
                'Score': row['score']
            }
            result_list.append(data)

        # Doing Sort
        for i in range(len(result_list)):
            for j in range(len(result_list)-1):
                if(result_list[i]['Score'] > result_list[j]['Score']):
                    temp = result_list[i]
                    result_list[i] = result_list[j]
                    result_list[j] = temp

        return result_list
    
    def get_a_game_hiscore(self, game):
        command = "SELECT * FROM ranking_info WHERE game='{}';".format(game)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()

        result_list = list()
        for row in record_from_db:
            data = {
                'Id': row['pl_id'],
                'Date':row['play_date'],
                'Name':row['name'],
                'Game':row['game'],
                'Score': row['score']
            }
            result_list.append(data)

        # Doing Sort
        for i in range(len(result_list)):
            for j in range(len(result_list)-1):
                if(result_list[i]['Score'] > result_list[j]['Score']):
                    temp = result_list[i]
                    result_list[i] = result_list[j]
                    result_list[j] = temp

        return result_list[0]['Score']

    def delete_a_data(self, pl_id):
        command = "DELETE FROM ranking_info WHERE pl_id='{}';".format(pl_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()
