class Countable:
    def __init__(self, amount=0, avg=0, cmax=float('-inf')):
        self.amount = amount
        self.avg = avg
        self.max = cmax

    def add(self, num):
        self.avg = self.avg * self.amount + num
        self.amount += 1
        self.max = num if self.max < num else self.max
        self.avg = self.avg / self.amount

    def split(self, name):
        return f"{name}_avg", self.avg, f"{name}_amount", self.amount, f"{name}_max", self.max

    @staticmethod
    def overview_types(name):
        return f"""{name}_amount integer,
        {name}_avg double,
        {name}_max double
        """

    @staticmethod
    def this_type(name):
        return f"{name} integer"

    @staticmethod
    def recreate(name, cursor, table, where):
        amount = cursor.execute(f"SELECT {name}_amount FROM {table} WHERE {where}").fetchall()[0][0]
        avg = cursor.execute(f"SELECT {name}_avg FROM {table} WHERE {where}").fetchall()[0][0]
        max = cursor.execute(f"SELECT {name}_max FROM {table} WHERE {where}").fetchall()[0][0]

        return Countable(amount, avg, max)


class Boolean:
    def __init__(self, amount=0, avg=0, last=0):
        self.amount = amount
        self.avg = avg * 100
        self.last = last

    def add(self, num):
        self.avg = self.avg * self.amount + num * 100
        self.amount += 1
        self.last = num
        self.avg = self.avg / self.amount

    def split(self, name):
        return f"{name}_avg", self.avg, f"{name}_amount", self.amount, f"{name}_last", self.last

    @staticmethod
    def overview_types(name):
        return f"""{name}_amount integer,
            {name}_avg double,
            {name}_last double
            """

    @staticmethod
    def this_type(name):
        return f"{name} boolean"

    @staticmethod
    def recreate(name, cursor, table, where):
        amount = cursor.execute(f"SELECT {name}_amount FROM {table} WHERE {where}").fetchall()[0][0]
        avg = cursor.execute(f"SELECT {name}_avg FROM {table} WHERE {where}").fetchall()[0][0]
        last = cursor.execute(f"SELECT {name}_last FROM {table} WHERE {where}").fetchall()[0][0]
        return Boolean(amount, avg, last)

# class MetaData:
#    def __init__(self, team, win=0, amount=0, comments=[], game_list=[]):
#        self.team = team
#        self.win = win
#        self.amount = amount
#        self.comments = comments
#        self.game_list = game_list
#
#     def add(self, win, comment, game):
#         self.win = self.win * self.amount + win
#         self.amount += 1
#         self.win = self.win / self.amount
#         if comment:
#             self.comments.append(comment)
#         if game:
#             self.game_list.append(game)
#
#     def split(self):
#         return self.team, self.amount, self.amount, self.comments, self.game_list
