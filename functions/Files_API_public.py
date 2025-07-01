
import subprocess
import sys
from functions.File_API_Workers import get_files_info_r, format_stdo , produce_working_directory_error, get_abs_path_data, os

def get_files_info(
    working_directory: str, 
    directory: str | None = None, 
    r_flag: bool = False
    )->str:
    working_directory_abs, target_abs = get_abs_path_data(working_directory, directory or '.');
    if not (target_abs.startswith(working_directory_abs)):
        return produce_working_directory_error('list',directory);
        
    if (not os.path.isdir(target_abs)):
        return f'Error: "{directory}" is not a directory';
    

    try:
        if r_flag:
            return format_stdo(
                get_files_info_r(target_abs),
                target_abs
            );
        else: 
            return format_stdo(
                [os.path.join(target_abs, file) for file in os.listdir(target_abs)],
                target_abs
            );
    
    except Exception as e:
        return f'Error: {e}';
    


def get_file_content(
    working_directory: str, 
    file_path: str
    )->str:
    MAX_CHARS: int = 10000
    CMAX_CHARS: int = 10005
    
    working_directory_abs, target_abs = get_abs_path_data(working_directory, file_path);
    
    if (not target_abs.startswith(working_directory_abs)):
        return produce_working_directory_error('read', file_path);
    
    if (not os.path.isfile(target_abs)):
        return f'Error: File not found or is not a regular file: "{file_path}"';
    try:
        with open(target_abs, 'r') as file:
            file_contetnt: str = file.read(CMAX_CHARS);
            content_length: int = len(file_contetnt);
            if (content_length > MAX_CHARS):
                return f'{file_contetnt[ : MAX_CHARS]}[...File "{file_path}" truncated at 10000 characters]';
            
            return f'{file_contetnt}';
    except Exception as e:
        return f'Error: {e}';
    
def write_file(
    working_directory: str,
    file_path: str,
    content: str
)->str:
    working_directory_abs, target_abs = get_abs_path_data(working_directory, file_path);
    if (not target_abs.startswith(working_directory_abs)):
        return produce_working_directory_error('write', file_path, '-wf');
    file_parent_directry_path: str = os.path.dirname(target_abs);
    if (not os.path.exists(file_parent_directry_path)):
        os.makedirs(file_parent_directry_path);
    try:
        with open(target_abs,'w', encoding = 'utf8') as f:
            f.write(content);
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)';

    except OSError as e:
        return f'Error: {e}';


def run_python_file(
    working_directory: str,
    file_path: str
    )->str:
    working_directory_abs, target_abs = get_abs_path_data(working_directory, file_path);
    
    if (not target_abs.startswith(working_directory_abs)):
        return produce_working_directory_error('execute', file_path);
    
    if (not os.path.exists(target_abs)):
        return f'Error: File "{file_path}" not found.';
    
    if (not file_path.endswith('.py')):
        return f'Error: "{file_path}" is not a Python file.';
    
    try:
        result: object = subprocess.run(args = [sys.executable, target_abs],
                                        capture_output = True, 
                                        timeout = 30.0, 
                                        cwd = working_directory_abs,
                                        text = True
                                        );
        output: str | None = ''
        if result.stderr:
            output += f'STDERR:\n{result.stderr}';    
        
        if result.stdout:
            output += f'STDOUT:\n{result.stdout}';
        
        if result.returncode != 0:
            output += f'Process exited with code {result.returncode}';
        return output;
    
    except Exception as e:
        return f'Error: executing Python file: {e}';
    
functions_dict: dict = {'get_files_info' : get_files_info,
                        'get_file_content': get_file_content,
                        'run_python_file': run_python_file,
                        'write_file': write_file};