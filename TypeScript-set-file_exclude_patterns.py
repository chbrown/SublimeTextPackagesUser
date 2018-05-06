import os
import re
import json
import sublime
import sublime_plugin


####################################
# Generic Sublime Text API Helpers #

def update_window_project_data(f, window=None):
    '''
    Get the project_data dict from the given window (defaults to the currently active window),
    run it through f, and set the project_data on that window to the changed dict.
    '''
    if window is None:
        window = sublime.active_window()
    window.set_project_data(f(window.project_data()))


#############################
# TypeScript Project Config #

def log(message):
    print('[set_file_exclude_patterns]', message)


def read_gitignore_exclude_patterns(path):
    gitignore_path = os.path.join(path, '.gitignore')
    try:
        log('reading {}'.format(gitignore_path))
        with open(gitignore_path) as fp:
            log('excluding .gitignore patterns')
            for line in fp:
                gitignore_line = line.strip()
                if not gitignore_line.startswith('#'):
                    yield gitignore_line
    except FileNotFoundError:
        pass


def read_tsconfig_exclude_patterns(path):
    '''
    Open the tsconfig file and read its `files` and `exclude` fields.
    '''
    tsconfig_path = os.path.join(path, 'tsconfig.json')
    try:
        log('reading {}'.format(tsconfig_path))
        with open(tsconfig_path) as fp:
            tsconfig = json.load(fp)
            log('excluding derivatives of .files')
            for source in tsconfig.get('files', []):
                basename = re.sub(r'\.tsx?$', '', source)
                for extension in ['.js', '.d.ts']:
                    yield basename + extension
            log('excluding .exclude patterns')
            for pattern in tsconfig.get('exclude', []):
                yield pattern
    except FileNotFoundError:
        pass


def update_folder(folder):
    '''
    folder is a dict like:
        {'path': '/Users/chbrown/github/urlio',
         'file_exclude_patterns': ['*.tmp']}
    '''
    path = folder['path']
    new_file_exclude_patterns = set(read_gitignore_exclude_patterns(path)) | set(read_tsconfig_exclude_patterns(path))
    original_file_exclude_patterns = folder.get('file_exclude_patterns', [])
    added_file_exclude_patterns = set(new_file_exclude_patterns) - set(original_file_exclude_patterns)
    log('adding new exclude patterns: {}'.format(', '.join(added_file_exclude_patterns)))
    updated_file_exclude_patterns = original_file_exclude_patterns + list(added_file_exclude_patterns)
    folder.update(file_exclude_patterns=updated_file_exclude_patterns)
    return folder


def update_project_data(project_data):
    project_data.update(folders=list(map(update_folder, project_data.get('folders', []))))
    return project_data


class SetFileExcludePatternsCommand(sublime_plugin.WindowCommand):
    '''
    In the console (Ctrl+`)
    Use like: window.run_command("set_file_exclude_patterns")
    Check like: sublime.active_window().project_data()
    '''
    def run(self):
        update_window_project_data(update_project_data)
