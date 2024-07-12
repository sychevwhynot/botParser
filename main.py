import subprocess

def run_all_scripts(scripts):
    processes = []
    try:
        for script in scripts:
            process = subprocess.Popen(['python', script])
            processes.append(process)
        
        # Ожидание завершения всех процессов
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        print("Завершаем все скрипты...")
        for process in processes:
            process.terminate()
        for process in processes:
            process.wait()

if __name__ == '__main__':
    scripts = ['2gis.py', 'doctu.py', 'konsult.py', 'napopravku.py', 'prodoc.py', 'yandex.py']  # Добавьте сюда имена ваших скриптов
    run_all_scripts(scripts)