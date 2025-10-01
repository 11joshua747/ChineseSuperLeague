# database_setup.py - 数据库表结构创建
import pymysql
import sys

def create_database_and_tables():
    """创建数据库和表结构"""
    try:
        sys.path.append('E:/miniconda/ChineseSuperLeague')
        from config import db_config

        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = connection.cursor()

        # 1. 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS csl_prediction CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ 数据库创建/验证完成")

        # 2. 使用数据库
        cursor.execute("USE csl_prediction")

        # 3. 创建球队表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teams (
                team_id INT AUTO_INCREMENT PRIMARY KEY,
                team_name VARCHAR(50) NOT NULL UNIQUE,
                team_name_short VARCHAR(20),
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ 球队表创建/验证完成")

        # 4. 创建比赛表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                match_id INT AUTO_INCREMENT PRIMARY KEY,
                season VARCHAR(10) NOT NULL,
                round_name VARCHAR(20) NOT NULL,
                match_date DATE NOT NULL,
                match_time TIME,
                home_team_id INT NOT NULL,
                away_team_id INT NOT NULL,
                home_score INT,
                away_score INT,
                home_half_score INT,
                away_half_score INT,
                result VARCHAR(5),
                created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
                FOREIGN KEY (away_team_id) REFERENCES teams(team_id),
                UNIQUE KEY unique_match (season, round_name, home_team_id, away_team_id)
            )
        """)
        print("✅ 比赛表创建/验证完成")

        connection.commit()
        cursor.close()
        connection.close()
        print("🎉 数据库和表结构创建成功！")
        return True
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return False

if __name__ == "__main__":
    create_database_and_tables()