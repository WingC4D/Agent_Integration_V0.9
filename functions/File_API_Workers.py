import os

def get_files_info_r(
    working_directory_abs: str
    )->list[str]:
    directories_to_scan: list[str] = [working_directory_abs];
    file_paths: list[str] = [working_directory_abs];
    while directories_to_scan:
        scanned_directory: str = directories_to_scan.pop();
        for path in os.listdir(scanned_directory):
            if (path.endswith('venv') | path.endswith('__pycache__') | path.endswith('.git')):
                continue;
            abs_path: str = os.path.join(scanned_directory, path);
            if os.path.isdir(abs_path):
                directories_to_scan.append(abs_path);
            file_paths.append(abs_path);
    return file_paths;

def format_stdo(
    paths: list[str],
    target_abs: str
    )->str:
    return '\n'.join(
        [
            f'- {
                    os.path.relpath(path, target_abs)
                }: file_size={
                    os.path.getsize(path)
                } bytes, is_dir={
                    os.path.isdir(path)
                }' for path in paths
        ]
    );

def produce_working_directory_error(
    action: str, 
    path: str,
    flag: None | str = None
    )->str | None:
    if flag:
        match flag:
            case '-wf':
                return f'Error: Cannot {action} to "{path}" as it is outside the permitted working directory';
    return f'Error: Cannot {action} "{path}" as it is outside the permitted working directory'         

def get_abs_path_data(
    working_directory: str,
    path: str
    )->tuple:
    '''
    ## Args:
        working_directory : Str
        path : Str
    
    ## Returns:
        A tuple with 2 object in it:
        1. working_directory_abs : Str
        2. target_abs : Str

    '''
    target: str = os.path.join(working_directory, path);
    return (os.path.abspath(working_directory), os.path.abspath(target));
