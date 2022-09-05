class Stack_book:
    def __init__(self):
        self.stack = []

    def addition(self, value):
        self.stack.append(value)

    def remove(self):
        removed = self.stack.pop()
        return removed


class TaskManager:
    def __init__(self):
        self.task_list = {}

    def new_task(self,task,priority):
        if priority in self.task_list:
            self.task_list[priority] += "; " + task
        else:
            self.task_list[priority] = task

    def remove(self,priority):
        removed = self.task_list.pop(priority)
        return removed

    def __str__(self):
        list_priority = list(self.task_list.keys())
        list_priority.sort()
        result = str()
        for keys in list_priority:
            result += str(f"{keys} {self.task_list[keys]}\n")
        return result


first_stack = Stack_book()



first_stack.addition(6)
first_stack.addition(2)
first_stack.addition(3)
first_stack.remove()
print(first_stack.stack)


manager = TaskManager()


manager.new_task("сделать уборку", 4)
manager.new_task("помыть посуду", 4)
manager.new_task("отдохнуть", 1)
manager.new_task("поесть", 2)
manager.new_task("сдать дз", 2)
manager.remove(2)
print(manager)

