# database_manager.py
import pymysql
import sys

class DatabaseManager:
    """封装所有数据库操作：连接、插入、查询等"""

    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        """连接 MySQL"""
        try:
            sys.path.append('E:/miniconda/ChineseSuperLeague')
            from config import db_config
            self.connection = pymysql.connect(
                **db_config,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("✅ 数据库连接成功")
            return True
        except pymysql.Error as e:
            print(f"❌ 数据库连接失败: {e}")
            return False

    def get_or_create_team(self, team_name):
        """根据球队名返回 team_id，不存在则创建"""
        if not self.connection:
            return None
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT team_id FROM teams WHERE team_name = %s", (team_name,))
            result = cursor.fetchone()
            if result:
                print(f"✅ 球队已存在: {team_name} (ID: {result['team_id']})")
                return result['team_id']
            else:
                cursor.execute("INSERT INTO teams (team_name) VALUES (%s)", (team_name,))
                self.connection.commit()
                team_id = cursor.lastrowid
                print(f"✅ 新球队创建成功: {team_name} (ID: {team_id})")
                return team_id
        except pymysql.Error as e:
            print(f"❌ 处理球队失败: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def insert_matches(self, matches):
        """批量插入比赛"""
        if not self.connection:
            return
        cursor = self.connection.cursor()
        try:
            sql = """INSERT INTO matches (season, round_name, match_date, home_team_id, away_team_id, home_score, away_score, result)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.executemany(sql, matches)
            self.connection.commit()
            print(f"✅ 批量插入比赛完成：{len(matches)} 条")
        except pymysql.Error as e:
            print(f"❌ 批量插入比赛失败: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def close(self):
        if self.connection:
            self.connection.close()
            print("✅ 数据库连接已关闭")