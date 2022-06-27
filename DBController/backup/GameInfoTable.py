from DBConnection import DBConnection


class gameInfoTable:
    def insert_a_game(self, pl_id, game, score):
        command = "INSERT INTO game_info (pl_id, game, score) VALUES  ('{}', '{}', '{}');".format(pl_id, game, score)
            
        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def select_student_game(self, pl_id):
        command = "SELECT * FROM game_info WHERE pl_id='{}';".format(pl_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            record_from_db = cursor.fetchall()
        result = dict()
        for row in record_from_db:
            result[row['game']] = row['score']

        return result

    def delete_student_games(self, pl_id):
        command = "DELETE FROM game_info WHERE pl_id='{}';".format(pl_id)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()

    def update_a_game(self, pl_id, game, score):
        command = "UPDATE game_info SET score='{}' WHERE pl_id='{}' AND game='{}';".format(score, pl_id, game)

        with DBConnection() as connection:
            cursor = connection.cursor()
            cursor.execute(command)
            connection.commit()
       