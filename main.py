from src.srv import DataClassUnpack, OnlinerTask, get_tasks


# tasks_url = "https://s.onliner.by/api/tasks?page=1&sections%5B%5D=service"

if __name__ == "__main__":
    tasks = []
    for i in range(1, 20):
        tasks_url = f"https://s.onliner.by/api/tasks?page={i}&sections%5B%5D=service"
        tasks.extend(get_tasks(tasks_url))
    # for task in tasks:
    print(len(tasks))

    oTasks: list[OnlinerTask] = []
    for _task in tasks:
        oTasks.append(DataClassUnpack.instantiate(OnlinerTask, _task))

    for otask in oTasks:
        s = otask.title.lower() + otask.description.lower()

        if "грм" in s and "вольво" in s:
            # and (
            #     # "volvo" in (otask.title.lower() + otask.description.lower())
            #     # or "вольво" in (otask.title.lower() + otask.description.lower())
            #     # or "b4164t" in otask.title.lower() + otask.description.lower()
            # )
            print(otask)
            print(otask.title.lower(), otask.description.lower())
