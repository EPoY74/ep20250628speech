import queue
import threading

task_queue = queue.Queue()


def worker():
    while True:
        task = task_queue.get()
        if task is None:
            break
        # Обработка задачи
        print(f"Обрабатываю задачу: {task}")
        task_queue.task_done()  # Уведомляет, что задача выполнена


# Создаем несколько потоков-воркеров
num_threads = 3
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=worker)
    thread.daemon = True  # Поток завершается при выходе из основной программы
    threads.append(thread)
    thread.start()

# Добавляем задачи в очередь
for i in range(5):
    task_queue.put(f"Задача {i}")

# Блокировка до завершения всех задач
task_queue.join()

# Отправляем "None" в очередь для завершения потоков
for _ in range(num_threads):
    task_queue.put(None)

for thread in threads:
    thread.join()  # Ожидаем завершения потоков

print("Все задачи выполнены")
