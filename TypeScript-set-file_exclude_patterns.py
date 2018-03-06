import os
import re
import json
import sublime
import sublime_plugin


def typescript_output(filename):
    basename = re.sub(r'\.tsx?$', '', filename)
    return [basename + '.js', basename + '.d.ts']


def read_tsconfig_files(path):
    '''
    Open the tsconfig file and read its list of files that are not *.d.ts files
    '''
    tsconfig_path = os.path.join(path, 'tsconfig.json')
    print('[set_file_exclude_patterns] reading .files from {}'.format(tsconfig_path))
    if os.path.exists(tsconfig_path):
        with open(tsconfig_path) as fp:
            tsconfig = json.load(fp)
            for file in tsconfig.get('files', []):
                if not file.endswith('.d.ts'):
                    yield file


def update_folder(folder):
    '''
    folder is a dict like {'path': '/Users/chbrown/github/urlio', 'file_exclude_patterns': ['*.tmp']}
    '''
    original_file_exclude_patterns = folder.get('file_exclude_patterns', [])
    typescript_sources = list(read_tsconfig_files(folder['path']))
    typescript_outputs = {output for source in typescript_sources for output in typescript_output(source)}
    new_typescript_outputs = list(typescript_outputs - set(original_file_exclude_patterns))
    print('[set_file_exclude_patterns] adding {}'.format(', '.join(new_typescript_outputs)))
    updated_file_exclude_patterns = original_file_exclude_patterns + new_typescript_outputs
    folder.update(file_exclude_patterns=updated_file_exclude_patterns)
    return folder


class SetFileExcludePatternsCommand(sublime_plugin.WindowCommand):
    '''
    In the console (Ctrl+`)
    Use like: window.run_command("set_file_exclude_patterns")
    Check like: sublime.active_window().project_data()
    '''

    def run(self):
        window = sublime.active_window()
        project_data = window.project_data()
        original_folders = project_data.get('folders', [])
        updated_folders = [update_folder(folder) for folder in original_folders]
        # why must Python make functional/immutable programming so difficult?
        #   dict(project_data.items() + [('folders', updated_folders)]) doesn't work anymore on Python 3
        project_data.update(folders=updated_folders)
        window.set_project_data(project_data)
