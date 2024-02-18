import sqlite3
import os
import rumps

class NotificationCounter(rumps.App):
    def __init__(self):
        super(NotificationCounter, self).__init__("NotificationCounter", title="Counting", icon=None)

    def get_notification_count(self):
        user_dir = os.popen("getconf DARWIN_USER_DIR").read().strip()
        file = user_dir + "com.apple.notificationcenter/db2/db"
        db = sqlite3.connect(f'file:{file}?mode=ro', uri=True)
        count = db.execute("SELECT count(1) FROM record").fetchone()[0]
        return count

    @rumps.timer(5)
    def a(self, sender):
        notification_count = self.get_notification_count()
        circled_zero = ord("⓿")
        circled_one = ord("❶")
        if (notification_count == 0):
            circled_number = chr(circled_zero + notification_count)
        else:
            circled_number = chr(circled_one + notification_count - 1)
        self.title = circled_number

if __name__ == "__main__":
    NotificationCounter().run()