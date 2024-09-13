import PySimpleGUI as sg
import subprocess
import sys
import os
import threading
import queue
import re
import io
import time

class EncodingSetup:
    @staticmethod
    def setup():
        try:
            if sys.stdout.encoding.lower() != 'utf-8':
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
            if sys.stderr.encoding.lower() != 'utf-8':
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
        except Exception as e:
            print(f"Error setting up encoding: {e}")

class ColorHandler:
    COLORS = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
    }

    @staticmethod
    def color_text(text, color):
        return f"{ColorHandler.COLORS[color]}{text}{ColorHandler.COLORS['reset']}"

    @staticmethod
    def parse_ansi_colors(text):
        ansi_to_sg = {
            '\033[91m': 'red',
            '\033[92m': 'green',
            '\033[93m': 'yellow',
            '\033[94m': 'blue',
            '\033[95m': 'magenta',
            '\033[96m': 'cyan',
        }
        parts = []
        current_color = None
        for part in re.split('(\033\\[\\d+m)', text):
            if part in ansi_to_sg:
                current_color = ansi_to_sg[part]
            elif part == '\033[0m':
                current_color = None
            elif part:
                parts.append((part, current_color))
        return parts

class SafeThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._return = None
        self._exception = None

    def run(self):
        try:
            if self._target:
                self._return = self._target(*self._args, **self._kwargs)
        except Exception as e:
            self._exception = e

    def join(self, timeout=None):
        super().join(timeout)
        if self._exception:
            raise self._exception
        return self._return

def run_with_timeout(func, args=(), kwargs={}, timeout=300):
    result_queue = queue.Queue()
    def wrapper():
        try:
            result = func(*args, **kwargs)
            result_queue.put(("result", result))
        except Exception as e:
            result_queue.put(("exception", e))

    thread = SafeThread(target=wrapper)
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive():
        raise TimeoutError(f"Function {func.__name__} timed out after {timeout} seconds")
    
    result_type, result_value = result_queue.get()
    if result_type == "exception":
        raise result_value
    return result_value

class AiderRunner:
    @staticmethod
    def find_python():
        return sys.executable

    @staticmethod
    def get_base_command(python_cmd):
        return [
            python_cmd,
            "-m",
            "aider",
            "--cache-prompts",
            "--map-refresh", "always",
            "--yes",
        ]

    @staticmethod
    def run_command(cmd, window, env):
        process = None
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True, env=env)
            window.user_data['process'] = process
            
            for line in iter(process.stdout.readline, ''):
                line = line.strip()
                if 'error' in line.lower():
                    colored_line = ColorHandler.color_text(line, 'red')
                elif 'warning' in line.lower():
                    colored_line = ColorHandler.color_text(line, 'yellow')
                elif 'success' in line.lower():
                    colored_line = ColorHandler.color_text(line, 'green')
                else:
                    colored_line = line
                window.write_event_value('-OUTPUT-', colored_line + '\n')
            
            process.wait()
            
            if process.returncode != 0:
                window.write_event_value('-OUTPUT-', ColorHandler.color_text(f"\nAider s'est terminé avec le code de retour : {process.returncode}", 'red'))
        except subprocess.CalledProcessError as e:
            window.write_event_value('-OUTPUT-', f"Erreur lors de l'exécution d'Aider : {e}")
        except Exception as e:
            window.write_event_value('-OUTPUT-', f"Une erreur inattendue s'est produite : {e}")
        finally:
            if process and process.stdout:
                process.stdout.close()
            window.write_event_value('-THREAD-DONE-', '')

class SettingsManager:
    @staticmethod
    def save_settings(role, request, folder):
        try:
            with open('aider_settings.txt', 'w', encoding='utf-8') as f:
                f.write(f"role={role}\nrequest={request}\nfolder={folder}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des paramètres : {e}")

    @staticmethod
    def load_settings():
        try:
            if not os.path.exists('aider_settings.txt'):
                return '', '', ''
            with open('aider_settings.txt', 'r', encoding='utf-8') as f:
                settings = {}
                for line in f:
                    key, value = line.strip().split('=', 1)
                    settings[key] = value
                return settings.get('role', ''), settings.get('request', ''), settings.get('folder', '')
        except Exception as e:
            print(f"Erreur lors du chargement des paramètres : {e}")
            return '', '', ''

    @staticmethod
    def reset_settings():
        if os.path.exists('aider_settings.txt'):
            os.remove('aider_settings.txt')

class APIKeyManager:
    @staticmethod
    def get_env_file_path():
        return os.path.join(os.path.expanduser('~'), '.aider_env')

    @staticmethod
    def save_api_key(api_key):
        env_path = APIKeyManager.get_env_file_path()
        try:
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write(f"OPENAI_API_KEY={api_key}")
            print(f"API key saved to {env_path}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la clé API : {e}")

    @staticmethod
    def get_api_key():
        env_path = APIKeyManager.get_env_file_path()
        try:
            if not os.path.exists(env_path):
                return None
            with open(env_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content.startswith('OPENAI_API_KEY='):
                    return content.split('=', 1)[1]
        except Exception as e:
            print(f"Erreur lors de la lecture de la clé API : {e}")
        return None

    @staticmethod
    def prompt_for_api_key(current_key=None):
        layout = [
            [sg.Text("Please enter your OpenAI API key:")],
            [sg.Input(default_text=current_key, key='-API_KEY-', password_char='*')],
            [sg.Button('Submit'), sg.Button('Cancel')]
        ]
        window = sg.Window('OpenAI API Key', layout)
        event, values = window.read()
        window.close()
        if event == 'Submit':
            return values['-API_KEY-']
        return None

def update_progress_bar(window):
    progress = 0
    while True:
        time.sleep(0.1)
        progress = (progress + 1) % 100
        window.write_event_value('-PROGRESS-UPDATE-', progress)

def main():
    try:
        EncodingSetup.setup()
        
        sg.theme('DarkBlue14')
        sg.set_options(font=("Segoe UI", 10))

        python_cmd = AiderRunner.find_python()
        if not python_cmd:
            sg.popup_error("Python n'a pas été trouvé dans le PATH du système.")
            return

        api_key = ''
        saved_api_key = APIKeyManager.get_api_key()
        if saved_api_key:
            api_key = saved_api_key
        
        base_cmd = AiderRunner.get_base_command(python_cmd)
        saved_role, saved_request, saved_folder = SettingsManager.load_settings()

        layout = [
            [sg.Text("KinOS: A team of autonomous agents on your computer", font=("Segoe UI", 20), pad=(0, 10))],
            [sg.Text("OpenAI API Key:", size=(10, 1)), 
             sg.Input(default_text=api_key, key='-API_KEY-', size=(40, 1), password_char='*'),
             sg.Button('Show/Hide', key='-TOGGLE_API-'), 
             sg.Button('Save', key='-SAVE_API-')],
            [sg.Text("Rôle:", size=(10, 1)), sg.Input(default_text=saved_role, key='-ROLE-', size=(50, 1), font=("Segoe UI", 10))],
            [sg.Text("Requête:", size=(10, 1)), sg.Multiline(default_text=saved_request, key='-REQUEST-', size=(50, 5), font=("Segoe UI", 10))],
            [sg.Text("Dossier:", size=(10, 1)), sg.Input(default_text=saved_folder, key='-FOLDER-', size=(40, 1), font=("Segoe UI", 10)), 
             sg.FolderBrowse(button_color=('white', '#4CAF50'))],
            [sg.Button('Lancer', key='-LAUNCH-', button_color=('white', '#4CAF50'), size=(10, 1)),
             sg.Button('Arrêter', key='-STOP-', button_color=('white', '#F44336'), size=(10, 1), disabled=True),
             sg.Button('Sauvegarder', key='-SAVE-', button_color=('white', '#2196F3'), size=(10, 1)),
             sg.Button('Réinitialiser', key='-RESET-', button_color=('white', '#FF9800'), size=(10, 1)),
             sg.Button('Quitter', button_color=('white', '#607D8B'), size=(10, 1))],
            [sg.Multiline(size=(80, 20), key='-OUTPUT-', autoscroll=True, reroute_stdout=True, reroute_stderr=True, 
                          disabled=True, font=("Consolas", 10), background_color='#263238', text_color='white', expand_x=True, expand_y=True)],
            [sg.ProgressBar(100, orientation='h', size=(66, 20), key='-PROGRESS-', visible=False, expand_x=True)]
        ]

        window = sg.Window('Aider Launcher', layout, finalize=True, size=(700, 600), element_justification='center',
                           resizable=True, return_keyboard_events=True)

        window.maximize()
        window.user_data = {'process': None}

        # Assurez-vous que la clé API est correctement initialisée dans l'interface
        window['-API_KEY-'].update('*' * len(api_key))

        show_api_key = False
        aider_thread = None
        progress_thread = None

        while True:
            event, values = window.read(timeout=100)
            if event == sg.WINDOW_CLOSED or event == 'Quitter':
                break
            if event == '-LAUNCH-':
                if not values['-FOLDER-'] or not os.path.isdir(values['-FOLDER-']):
                    sg.popup_error("Veuillez sélectionner un dossier valide.")
                    continue
                cmd = base_cmd.copy()
                if values['-ROLE-']:
                    cmd.extend(['--role', values['-ROLE-']])
                if values['-REQUEST-']:
                    cmd.extend(['--request', values['-REQUEST-']])
                if values['-FOLDER-']:
                    cmd.extend(['--folder', values['-FOLDER-']])
                window['-OUTPUT-'].update('')
                window['-LAUNCH-'].update(disabled=True)
                window['-STOP-'].update(disabled=False)
                window['-PROGRESS-'].update(visible=True)
                env = os.environ.copy()
                env['OPENAI_API_KEY'] = api_key
                try:
                    def run_aider():
                        return AiderRunner.run_command(cmd, window, env)
                    
                    aider_thread = SafeThread(target=lambda: run_with_timeout(run_aider, timeout=300), daemon=True)
                    aider_thread.start()
                    
                    progress_thread = SafeThread(target=update_progress_bar, args=(window,), daemon=True)
                    progress_thread.start()
                except Exception as e:
                    sg.popup_error(f"Une erreur s'est produite lors du lancement d'Aider : {str(e)}")
                    window['-LAUNCH-'].update(disabled=False)
                    window['-STOP-'].update(disabled=True)
                    window['-PROGRESS-'].update(visible=False)
            elif event == '-STOP-':
                if window.user_data['process']:
                    window.user_data['process'].terminate()
                window['-LAUNCH-'].update(disabled=False)
                window['-STOP-'].update(disabled=True)
                window['-PROGRESS-'].update(visible=False)
            elif event == '-SAVE-':
                SettingsManager.save_settings(values['-ROLE-'], values['-REQUEST-'], values['-FOLDER-'])
                sg.popup("Paramètres sauvegardés avec succès !", title="Sauvegarde réussie", button_color=('white', '#2196F3'))
            elif event == '-RESET-':
                SettingsManager.reset_settings()
                window['-ROLE-'].update('')
                window['-REQUEST-'].update('')
                window['-FOLDER-'].update('')
                sg.popup("Paramètres réinitialisés avec succès !", title="Réinitialisation réussie", button_color=('white', '#FF9800'))
            elif event == '-OUTPUT-':
                parts = ColorHandler.parse_ansi_colors(values[event])
                for text, color in parts:
                    window['-OUTPUT-'].update(text, text_color_for_value=color, append=True)
            elif event == '-THREAD-DONE-':
                window['-LAUNCH-'].update(disabled=False)
                window['-STOP-'].update(disabled=True)
                window['-PROGRESS-'].update(visible=False)
            elif event == '-TOGGLE_API-':
                show_api_key = not show_api_key
                if show_api_key:
                    window['-API_KEY-'].update(api_key)
                    window['-API_KEY-'].update(password_char='')
                else:
                    window['-API_KEY-'].update('*' * len(api_key))
                    window['-API_KEY-'].update(password_char='*')
            elif event == '-SAVE_API-':
                new_api_key = values['-API_KEY-']
                if new_api_key:
                    api_key = new_api_key
                    APIKeyManager.save_api_key(api_key)
                    window['-API_KEY-'].update('*' * len(api_key))
                    window['-API_KEY-'].update(password_char='*')
                    show_api_key = False
                    sg.popup("API key saved successfully", title="API Key Saved", button_color=('white', '#2196F3'))
                else:
                    sg.popup_error("Please enter an API key before saving", title="Error", button_color=('white', '#F44336'))
            elif event == '-PROGRESS-UPDATE-':
                if window['-PROGRESS-'].visible:
                    window['-PROGRESS-'].update(values[event])

        # Nettoyage des ressources
        if aider_thread and aider_thread.is_alive():
            aider_thread.join(timeout=5)
        if progress_thread and progress_thread.is_alive():
            progress_thread.join(timeout=5)

        window.close()
    except Exception as e:
        sg.popup_error(f"Une erreur s'est produite : {str(e)}")
        print(f"Erreur : {str(e)}")

if __name__ == "__main__":    
    main()
