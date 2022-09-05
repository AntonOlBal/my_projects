class Stack:
    def __init__(self):
        self.stack = []

    def __str__(self):
        return '; '.join(self.stack)

    def append_elem(self, elem):
        self.stack.append(elem)

    def delete_elem(self):
        if len(self.stack) == 0:
            return None
        return self.stack.pop()


class TaskManager:
    def __init__(self):
        self.task = {}

    def __str__(self):
        display = []
        if self.task:
            for i_priority in sorted(self.task.keys()):
                display.append(f'{str(i_priority)} {self.task[i_priority]}\n')

        return ''.join(display)

    def new_task(self, task, priority):
        if priority not in self.task:
            self.task[priority] = Stack()
        self.task[priority].append_elem(task)


manager = TaskManager()
manager.new_task("сделать уборку", 4)
manager.new_task("помыть посуду", 4)
manager.new_task("отдохнуть", 1)
manager.new_task("поесть", 2)
manager.new_task("сдать дз", 2)
print(manager)