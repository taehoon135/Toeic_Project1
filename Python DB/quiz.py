import sqlite3
import random

class Quiz:
    """
    퀴즈 기능을 관리하는 클래스
    
    주요 기능:
    1. 퀴즈 시작
    2. 퀴즈 결과 확인
    3. 오답 노트
    4. 퀴즈 통계
    """
    
    def __init__(self, user_id):
        """
        퀴즈 클래스를 초기화합니다.
        
        Args:
            user_id (int): 사용자 ID
        """
        self.conn = sqlite3.connect('toeic_vocabulary.db')
        self.cursor = self.conn.cursor()
        self.user_id = user_id
        self.setup_database()
    
    def setup_database(self):
        """데이터베이스 초기 설정"""
        # QuizResult 테이블 생성
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS QuizResult (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER,
            total_questions INTEGER,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES User(user_id)
        )
        ''')
        
        # WrongAnswer 테이블 생성
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS WrongAnswer (
            wrong_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            word_id INTEGER,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES User(user_id),
            FOREIGN KEY (word_id) REFERENCES Word(word_id)
        )
        ''')
        
        self.conn.commit()
    
    def show_quiz_menu(self):
        """퀴즈 메뉴를 표시합니다."""
        while True:
            print("\n=== 퀴즈 ===")
            print("1. 퀴즈 시작")
            print("2. 퀴즈 결과 확인")
            print("3. 오답 노트")
            print("4. 퀴즈 통계")
            print("5. 돌아가기")
            
            choice = input("\n원하는 작업을 선택하세요 (1-5): ")
            
            if choice == '1':
                self.start_quiz()
            elif choice == '2':
                self.show_quiz_results()
            elif choice == '3':
                self.show_wrong_answers()
            elif choice == '4':
                self.show_quiz_statistics()
            elif choice == '5':
                print("퀴즈를 종료합니다.")
                break
            else:
                print("잘못된 선택입니다. 다시 시도하세요.")
    
    def start_quiz(self):
        """퀴즈를 시작합니다."""
        print("\n=== 퀴즈 시작 ===")
        print("퀴즈 기능은 아직 구현되지 않았습니다.")
    
    def show_quiz_results(self):
        """퀴즈 결과를 표시합니다."""
        print("\n=== 퀴즈 결과 ===")
        print("퀴즈 결과 기능은 아직 구현되지 않았습니다.")
    
    def show_wrong_answers(self):
        """오답 노트를 표시합니다."""
        print("\n=== 오답 노트 ===")
        print("오답 노트 기능은 아직 구현되지 않았습니다.")
    
    def show_quiz_statistics(self):
        """퀴즈 통계를 표시합니다."""
        print("\n=== 퀴즈 통계 ===")
        print("퀴즈 통계 기능은 아직 구현되지 않았습니다.") 