***
Проект: Таймер, работающий {duration_munutes} мунут, и воспроивздящий сообщение об оставшемся времени с интервалом {elapse_playback_interval_minutes}. Так же нужно задать имя клиента в переменную {clients_name}
***
Работаю с воспроизведением звука, из текста.

Рабочий исполняемый файл: app/timer.py

Это для того, что бы написать голосовой таймер, что бы он каждые , допустим, 5 минут, говорил сколько осталось времени до окончания сеанса.

Для генерации голоса используется gtts

Для воспроизведения - pygame

Промежуточный результат сохраняется в файл.