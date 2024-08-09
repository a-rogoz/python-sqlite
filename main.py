import sqlite3


class Task:
    def __init__(self):
        self.conn = sqlite3.connect("main.db")
        self.c = self.conn.cursor()
        self.create_task_table()

    def create_task_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                       id INTEGER PRIMARY KEY,
                       name TEXT NOT NULL,
                       priority INTEGER NOT NULL
                       );''')
        
    def find_task(self, name):
        tasks = self.c.execute('SELECT * FROM tasks')
        for task in tasks:
            if task[1] == name:
                print("Found!")
                return task
        return None

    def read_tasks(self):
        # Less efficient:
        # rows = self.c.fetchall()

        # One:
        # row = self.c.fetchone()

        for row in self.c.execute('SELECT * FROM tasks'):
            print(row)

    def add_task(self):
        name = input('Enter the task name: ')
        priority = int(input('Enter the task priority: '))
        
        if name == "":
            raise ValueError("The name cannot be an empty string!")
        
        if priority < 1:
            raise ValueError("The priority cannot be less than 1!")
        
        self.c.execute('INSERT INTO tasks (name, priority) VALUES (?,?)', (name, priority))
        self.conn.commit()

    def update_task(self, id, priority):
        self.c.execute('UPDATE tasks SET priority = ? WHERE id = ?', (priority, id))
        self.conn.commit()

    def delete_task(self, id):
        self.c.execute('DELETE FROM tasks WHERE id = ?', (id,))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
        
app = Task()
        
option = 0
while option != 5:
    print("\033[93m" + "1. Show Tasks" + "\033[0m")
    print("\033[93m" + "2. Add Task" + "\033[0m")
    print("\033[93m" + "3. Change Priority" + "\033[0m")
    print("\033[93m" + "4. Delete Task" + "\033[0m")
    print("\033[93m" + "5. Exit" + "\033[0m")
    try:
        option = int(input("Select action: "))
    except ValueError:
        print("Incorrect value. Try again!")
    
    match option:
        case 1:
            app.read_tasks()
        case 2:
            app.add_task()
        case 3:
            try:
                id = int(input("Enter the task ID to update: "))
                priority = int(input("Enter the task new priority: "))
            except ValueError:
                print("Incorrect values provided!")
                exit()

            app.update_task(id, priority)
        case 4:
            try:
                id = int(input("Enter the task ID to delete: "))
            except ValueError:
                print("Incorrect ID value!")
                exit()

            app.delete_task(id)
        case 5:
            print("Exiting...")
            app.close_connection()
            exit()
