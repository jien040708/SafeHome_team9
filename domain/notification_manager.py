import os
from datetime import datetime

class NotificationManager:
    def __init__(self):
        self.log_dir = "notifications"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def send_sms(self, message):
        """SMS 발송 시뮬레이션 (파일 생성)"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"{self.log_dir}/sms_log.txt"
        
        log_msg = f"[{timestamp}] [SMS SENT] To: 010-1234-5678 | Msg: {message}\n"
        
        # 로그 파일에 추가 (append 모드)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(log_msg)
            
        print(f"📱 [Notification] SMS Sent: {message}")

    def make_call(self, message):
        """전화 걸기 시뮬레이션"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"{self.log_dir}/call_log.txt"
        
        log_msg = f"[{timestamp}] [CALL MADE] To: 112 | Msg: {message}\n"
        
        with open(filename, "a", encoding="utf-8") as f:
            f.write(log_msg)
            
        print(f"📞 [Notification] Emergency Call Made: {message}")