import sqlite3
import datetime
import openpyxl
import pandas as pd


class DatabaseAccess:

    def __init__(self) -> None:
        self.conn = sqlite3.connect(r"digiHome.db")
        self.cur = self.conn.cursor()

    def store_temp_humidity(self, data):
        try:
            datetime = self.get_date_time()
            self.cur.execute("INSERT INTO tbl_Temp_Humidity(Date, Time, Temp, Humidity) VALUES(?,?,?,?)", (datetime["Date"], datetime["Time"], data["temperature"], data["humidity"]))
            self.conn.commit()
        except Exception as e:
            print(f"database lock : {e}")

    def get_date_time(self) -> str:
        """
        returns current DateTime 
        """
        t = datetime.datetime.now()
        date = t.strftime("%d-%m-%Y")
        time = t.strftime("%H:%M:%S")
        return {"Date":date, "Time":time}


    def read_all_data(self):
        self.cur.execute("SELECT * FROM tbl_Temp_Humidity")
        data = self.cur.fetchall()
        return data
    
    def export_to_excel(self):
        data = self.read_all_data()
        df = pd.DataFrame(data)
        print(df)
        df.to_excel(r"D:\projects_Flask\digihomeapp\output.xlsx", index=False)

# db = DatabaseAccess()
# db.export_to_excel()