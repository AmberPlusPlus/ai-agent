import os
import subprocess
from google import genai
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
        
    work_dir_abs = "/home/amber/workspace/github.com/AmberPlusPlus/ai-agent"

    abs_working_dir = os.path.normpath(os.path.abspath(working_directory))
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
    is_inside = abs_file_path == abs_working_dir or abs_file_path.startswith(abs_working_dir + os.sep)
    #valid_target_file = os.path.commonpath([abs_working_dir, abs_file_path]) == abs_working_dir

    print("DEBUG run_python_file:", working_directory, file_path, abs_working_dir, abs_file_path, "is_inside=", is_inside)


    if not is_inside:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not str(abs_file_path).endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", abs_file_path]
    command.extend(args)

    try:
        result = subprocess.run(command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30)

        output_str = ""
        if result.returncode:
            output_str += f"Process exited with code {result.returncode}\n"
        if not result.stdout.strip() and not result.stderr.strip():
            output_str += "No output produced\n"
        else:
            if result.stdout.strip():
                output_str += f"STDOUT: {result.stdout.strip()}\n"
            if result.stderr.strip():
                output_str += f"STDERR: {result.stderr.strip()}\n"
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    return output_str

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the file to be executed.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                        type=types.Type.STRING,
                        description="A single CLI argument"
                    ),
                description="List of optional CLI string arguments"
            )
        },
        required=["file_path"]
    ),
)