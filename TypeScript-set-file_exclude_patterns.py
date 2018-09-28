import os
import subprocess
import sublime
import sublime_plugin


####################################
# Generic Sublime Text API Helpers #

def update_window_project_data(window, f):
    '''
    Get the project_data dict from the given window, run it through f,
    and set the project_data on that window to the result.
    '''
    window.set_project_data(f(window.project_data()))


#############################
# TypeScript Project Config #

def log(*messages):
    print('[set_file_exclude_patterns]', *messages)


def read_tsc_emitted_files(folder_path):
    args = ['npx', 'tsc', '--listEmittedFiles']
    log('running subprocess:', ' '.join(args))
    lines = subprocess.check_output(args, cwd=folder_path, universal_newlines=True)
    for line in lines.split('\n'):
        if line.startswith('TSFILE: '):
            # strip first 8 characters ('TSFILE: ')
            filepath = line[8:]
            # relativize filepath to given folder path
            yield os.path.relpath(filepath, folder_path)


def update_folder(folder):
    '''
    folder is a dict like:
        {'path': '/Users/chbrown/github/urlio',
         'file_exclude_patterns': ['*.tmp']}
    '''
    file_exclude_patterns = folder.get('file_exclude_patterns', [])
    for tsc_emitted_file in read_tsc_emitted_files(folder['path']):
        if tsc_emitted_file not in file_exclude_patterns:
            file_exclude_patterns.append(tsc_emitted_file)
    return dict(folder, file_exclude_patterns=file_exclude_patterns)


def update_project_data(project_data):
    return dict(project_data, folders=list(map(update_folder, project_data.get('folders', []))))


class SetFileExcludePatternsCommand(sublime_plugin.WindowCommand):
    '''
    In the console (Ctrl+`)
    Use like: window.run_command("set_file_exclude_patterns")
    Check like: sublime.active_window().project_data()
    '''
    def run(self):
        window = self.window
        update_window_project_data(window, update_project_data)
