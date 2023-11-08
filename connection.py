from datetime import date

import pymysql  # type: ignore


class conn:
    def __init__(self) -> None:
        self.con = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            db="secure_id",
            port=3306,
        )
        self.cu = self.con.cursor()

    def nonreturn(self, a: str) -> int | None:  # ins  upd  del
        self.cu.execute(a)
        id = self.cu.lastrowid
        self.con.commit()
        return id

    def selectone(self, a: str) -> tuple[int | str | None, ...]:  # one row
        self.cu.execute(a)
        self.res = self.cu.fetchone()
        return self.res

    def selectall(
        self, a: str
    ) -> tuple[tuple[int | str | None, ...], ...]:  # multiple row
        self.cu.execute(a)
        self.res = self.cu.fetchall()
        return self.res

    def jsonsel(self, a: str) -> list[dict[str, int | str | date]]:
        self.cu.execute(a)
        self.res = self.cu.fetchall()
        row_headers = [x[0] for x in self.cu.description]
        json_data = []
        for result in self.res:
            json_data.append(dict(zip(row_headers, result)))
        return json_data
