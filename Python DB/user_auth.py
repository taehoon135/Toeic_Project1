import sqlite3
import hashlib
import os
from wordbook import Wordbook
from quiz import Quiz

class UserAuth:
    """
    사용자 인증을 관리하는 클래스
    
    주요 기능:
    1. 회원가입: 새로운 사용자 등록
    2. 로그인: 사용자 인증
    3. ID 중복 확인: 회원가입 시 ID 중복 검사
    
    데이터베이스 테이블:
    - User: 사용자 정보 저장
    """
    
    def __init__(self):
        """
        UserAuth 클래스 초기화
        데이터베이스 연결을 설정합니다.
        """
        self.conn = sqlite3.connect("toeic_vocabulary.db")
        self.cursor = self.conn.cursor()
        self.current_user = None
        self.setup_database()

    def __del__(self):
        """
        객체가 소멸될 때 데이터베이스 연결을 종료합니다.
        """
        self.conn.close()

    def setup_database(self):
        """데이터베이스 초기 설정"""
        # User 테이블 생성
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
        ''')
        
        # 관리자 계정이 없으면 생성
        self.cursor.execute("SELECT * FROM User WHERE username = 'admin'")
        if not self.cursor.fetchone():
            admin_password = hashlib.sha256('admin123'.encode()).hexdigest()
            self.cursor.execute('''
            INSERT INTO User (username, password, name, is_admin)
            VALUES (?, ?, ?, ?)
            ''', ('admin', admin_password, '관리자', 1))
            self.conn.commit()
        
        self.conn.commit()

    def register(self):
        """사용자 회원가입"""
        print("\n=== 회원가입 ===")
        username = input("ID를 입력하세요: ")
        
        # ID 중복 확인
        self.cursor.execute("SELECT * FROM User WHERE username = ?", (username,))
        if self.cursor.fetchone():
            print("이미 사용 중인 ID입니다.")
            return False
        
        password = input("비밀번호를 입력하세요: ")
        name = input("이름을 입력하세요: ")
        
        # 비밀번호 해시화
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            self.cursor.execute('''
            INSERT INTO User (username, password, name, is_admin)
            VALUES (?, ?, ?, ?)
            ''', (username, hashed_password, name, 0))
            self.conn.commit()
            print("회원가입이 완료되었습니다.")
            return True
        except sqlite3.Error as e:
            print(f"회원가입 중 오류가 발생했습니다: {str(e)}")
            return False

    def login(self):
        """사용자 로그인"""
        print("\n=== 로그인 ===")
        username = input("ID를 입력하세요: ")
        password = input("비밀번호를 입력하세요: ")
        
        # 비밀번호 해시화
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        self.cursor.execute('''
        SELECT user_id, username, name, is_admin FROM User 
        WHERE username = ? AND password = ?
        ''', (username, hashed_password))
        
        user = self.cursor.fetchone()
        if user:
            self.current_user = {
                'user_id': user[0],
                'username': user[1],
                'name': user[2],
                'is_admin': bool(user[3])
            }
            print("로그인 성공")
            print(f"사용자 정보: [계정유형: {'관리자' if self.current_user['is_admin'] else '일반 사용자'}] ID: {self.current_user['username']}, 이름: {self.current_user['name']}")
            return True
        else:
            print("ID 또는 비밀번호가 올바르지 않습니다.")
            return False

    def show_main_menu(self):
        """메인 메뉴 표시"""
        print("\n=== TOEIC 단어장 시스템 ===")
        print(f"환영합니다, {self.current_user['name']}님!")
        print("1. 단어장")
        print("2. 퀴즈")
        print("3. 설정")
        print("4. 로그아웃")
        
        choice = input("\n원하는 작업을 선택하세요 (1-4): ")
        return choice

    def run(self):
        """시스템 실행"""
        while True:
            print("\n=== TOEIC 단어장 시스템 ===")
            print("1. 회원가입")
            print("2. 로그인")
            print("3. 종료")
            
            choice = input("\n원하는 작업을 선택하세요 (1-3): ")
            
            if choice == '1':
                self.register()
            elif choice == '2':
                if self.login():
                    self.main_loop()
            elif choice == '3':
                print("프로그램을 종료합니다.")
                break
            else:
                print("잘못된 선택입니다. 다시 시도하세요.")

    def main_loop(self):
        """로그인 후 메인 루프"""
        while True:
            choice = self.show_main_menu()
            
            if choice == '1':
                wordbook = Wordbook(self.current_user['user_id'])
                wordbook.show_wordbook_menu()
            elif choice == '2':
                quiz = Quiz(self.current_user['user_id'])
                quiz.show_quiz_menu()
            elif choice == '3':
                self.show_settings_menu()
            elif choice == '4':
                print("로그아웃되었습니다.")
                self.current_user = None
                break
            else:
                print("잘못된 선택입니다. 다시 시도하세요.")

    def show_settings_menu(self):
        """설정 메뉴 표시"""
        while True:
            print("\n=== 설정 ===")
            print("1. 회원 정보 수정")
            print("2. 비밀번호 변경")
            print("3. 계정 삭제")
            print("4. 돌아가기")
            
            choice = input("\n원하는 작업을 선택하세요 (1-4): ")
            
            if choice == '1':
                self.edit_profile()
            elif choice == '2':
                self.change_password()
            elif choice == '3':
                self.delete_account()
            elif choice == '4':
                break
            else:
                print("잘못된 선택입니다. 다시 시도하세요.")

    def edit_profile(self):
        """회원 정보 수정"""
        print("\n=== 회원 정보 수정 ===")
        new_name = input("새로운 이름을 입력하세요: ")
        
        try:
            self.cursor.execute('''
            UPDATE User SET name = ? WHERE user_id = ?
            ''', (new_name, self.current_user['user_id']))
            self.conn.commit()
            self.current_user['name'] = new_name
            print("회원 정보가 수정되었습니다.")
        except sqlite3.Error as e:
            print(f"회원 정보 수정 중 오류가 발생했습니다: {str(e)}")

    def change_password(self):
        """비밀번호 변경"""
        print("\n=== 비밀번호 변경 ===")
        current_password = input("현재 비밀번호를 입력하세요: ")
        hashed_current = hashlib.sha256(current_password.encode()).hexdigest()
        
        self.cursor.execute('''
        SELECT password FROM User WHERE user_id = ?
        ''', (self.current_user['user_id'],))
        stored_password = self.cursor.fetchone()[0]
        
        if hashed_current != stored_password:
            print("현재 비밀번호가 올바르지 않습니다.")
            return
        
        new_password = input("새로운 비밀번호를 입력하세요: ")
        confirm_password = input("새로운 비밀번호를 다시 입력하세요: ")
        
        if new_password != confirm_password:
            print("비밀번호가 일치하지 않습니다.")
            return
        
        hashed_new = hashlib.sha256(new_password.encode()).hexdigest()
        
        try:
            self.cursor.execute('''
            UPDATE User SET password = ? WHERE user_id = ?
            ''', (hashed_new, self.current_user['user_id']))
            self.conn.commit()
            print("비밀번호가 변경되었습니다.")
        except sqlite3.Error as e:
            print(f"비밀번호 변경 중 오류가 발생했습니다: {str(e)}")

    def delete_account(self):
        """계정 삭제"""
        print("\n=== 계정 삭제 ===")
        confirm = input("정말로 계정을 삭제하시겠습니까? (y/n): ")
        
        if confirm.lower() == 'y':
            try:
                self.cursor.execute('''
                DELETE FROM User WHERE user_id = ?
                ''', (self.current_user['user_id'],))
                self.conn.commit()
                print("계정이 삭제되었습니다.")
                self.current_user = None
                return True
            except sqlite3.Error as e:
                print(f"계정 삭제 중 오류가 발생했습니다: {str(e)}")
        return False

if __name__ == "__main__":
    auth = UserAuth()
    auth.run() 