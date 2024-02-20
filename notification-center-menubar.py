import sqlite3
import os
import rumps


class NotificationCounter(rumps.App):

    def __init__(self):
        super().__init__("NotificationCounter", title="Counting", icon=None)

    def get_notification_count(self):
        user_dir = os.popen("getconf DARWIN_USER_DIR").read().strip()

        file_path = os.path.join(user_dir, "com.apple.notificationcenter/db2/db")
        if not os.path.exists(file_path):
            return 0

        with sqlite3.connect(f'file:{file_path}?mode=ro', uri=True) as db:
            cursor = db.cursor()
            cursor.execute("SELECT count(1) FROM record")
            count = cursor.fetchone()[0]
        return count


    @rumps.timer(5)
    def a(self, _sender_):
        notification_count = self.get_notification_count()
        circled_zero = ord("⓿")
        circled_one = ord("❶")
        if notification_count == 0:
            circled_number = chr(circled_zero + notification_count)
        else:
            circled_number = chr(circled_one + notification_count - 1)
        self.title = circled_number


if __name__ == "__main__":
    NotificationCounter().run()
