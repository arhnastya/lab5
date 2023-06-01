ALPHABET = "qwertyuiopasdfghjklzxcvbnm1234567890_"


# класс хранит номер студента отдельно
class Row():
    id = 0

    def __init__(self, id: int):
        self.id = id

    def get_id(self):
        return self.id

    def set_id(self, val):
        self.id = val


# класс хранит все данные списка
class RowModel(Row):
    id = 0
    name = ""
    email = ""
    group = ""

    def __init__(self, id: int, name: str, email: str, group: str):
        super().__init__(id)
        self.name = name
        self.email = email
        self.group = group

    # вызывается при команде print элемента списка
    def __str__(self):
        return f"№{self.id}\nФИО: {self.name}\nemail: {self.email}\nГруппа: {self.group}\n"

    def __repr__(self):
        return f"RowModel(id={self.id},name={self.name},email={self.email},group={self.group})"

    def __setattr__(self, __name, __value):
        self.__dict__[__name] = __value


class Data():
    file_path = ""
    data = []
    pointer = 0

    def __init__(self, path: str):
        self.file_path = path
        self.data = self.parse(self.file_path)

    def __str__(self):
        d_str = '\n'.join([str(rm) for rm in self.data])
        return f"Контейнер хранит в себе следующее:\n{d_str}"

    def __repr__(self):
        return f"Data({[repr(rm) for rm in self.data]})"

    def __iter__(self):
        return self

    def __next__(self):
        if self.pointer >= len(self.data):
            self.pointer = 0
            raise StopIteration
        else:
            self.pointer += 1
            return self.data[self.pointer - 1]

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError("Индекс должен быть целым числом.")

        if 0 <= item < len(self.data):
            return self.data[item]
        else:
            raise IndexError("Неверный индекс.")

    def as_generator(self):
        self.pointer = 0

        while self.pointer < len(self.data):
            yield self.data[self.pointer]
            self.pointer += 1

    def sorted_by_name(self) -> list:
        return sorted(self.data, key=lambda f: f.name)

    def sorted_by_number(self) -> list:
        return sorted(self.data, key=lambda f: f.id)

    def select_rows_with_likes_count_more_than(self, value) -> list:
        return [rm for rm in self.data if rm.group >= value]

    def add_new(self, id, name, email, group):
        self.data.append(RowModel(id, name, email, group))
        self.save(self.file_path, self.data)

    @staticmethod
    def parse(path: str) -> list:
        parsed = []

        with open(path, "r") as raw_csv:
            for line in raw_csv:
                (id, name, email, group) = line.replace("\n", "").split(",")
                parsed.append(RowModel(int(id), name, email, group))

        return parsed

    @staticmethod
    def save(path, new_data):
        with open(path, "w") as f:
            for rm in new_data:
                f.write(f"{rm.id},{rm.name},{rm.email},{rm.group}\n")


if __name__ == "__main__":

    #init класса d, использующий методы RowModel, наследующийся от класса Row
    d = Data("data-1.csv")

    print("Используем итератор:\n")

    for item in iter(d):
        print(item)

    print("-" * 64)

    print("Используем генератор:\n")

    for item in d.as_generator():
        print(item)

    print("=" * 64)

    print("Сортировка по ФИО:\n")

    for item in d.sorted_by_name():
        print(item)

    print("-" * 64)

    print("Сортировка по id студента:\n")

    for item in d.sorted_by_number():
        print(item)

    print("-" * 64)

    print("Выборка студентов, находящихся в группе ИВТАПбд22:\n")

    for item in d.select_rows_with_likes_count_more_than("IVTAP22"):
        print(item)

    print("=" * 64)

    # Добавим элемент (addnew и save)
    print("Добавление данных:")
    d.add_new(input("Номер Студента: "), input("ФИО: "), input("email: "), input("Группа: "))
    print()

    for item in iter(d):
        print(item)

    print("=" * 64)

    # Вводишь индекс списка - получаешь его элемент (значение), вызваается в getitem
    print("Выборка по индексу:")
    id = int(input("Индекс: "))
    print(f"\n{d[id]}")
