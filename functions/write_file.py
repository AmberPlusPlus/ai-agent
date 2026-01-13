import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    work_dir_abs = "/home/amber/workspace/github.com/AmberPlusPlus/ai-agent"
    
    abs_working_dir = os.path.normpath(os.path.abspath(working_directory))
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
    is_inside = abs_file_path == abs_working_dir or abs_file_path.startswith(abs_working_dir + os.sep)
    #valid_target_dir = os.path.commonpath([abs_working_dir, abs_file_path]) == abs_working_dir

    #print("DEBUG write_file:", working_directory, file_path, abs_working_dir, abs_file_path, "is_inside=", is_inside)


    if not is_inside:
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(file_path):
        f'Error: Cannot write to "{file_path}" as it is a directory'
    
    try:
        os.makedirs(abs_working_dir, exist_ok=True)
    except:
        return "Error: unable to create directories"

    try:
        with open(abs_file_path, "w") as file:
            try:
                file.write(content)
            except:
                return f'Error: file "{file_path}" could not be written.'
    except:
        return f"Error: file {file_path} was not found"
        
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text to a specified file path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the file to be written to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to the file. Existing content will be overwritten.",
            ),
        },
        required=["file_path", "content"]
    ),
)