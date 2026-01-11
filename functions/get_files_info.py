import os
from google import genai
from google.genai import types


work_dir_abs = "/home/amber/workspace/github.com/AmberPlusPlus/ai-agent/calculator"

def get_files_info(working_directory, directory="."):

    abs_working_dir = os.path.normpath(os.path.abspath(working_directory))
    target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))                     #target_dir = os.path.normpath(os.path.join(work_dir_abs, directory))
    valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir     #valid_target_dir = os.path.commonpath([work_dir_abs, target_dir]) == work_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    match directory:
        case ".":
            result_header = "Result for current directory:"
        case _:
            result_header = f"Result for '{directory}' directory:"
    item_details = [result_header]
    try:
        for item in os.listdir(target_dir):
            name = item
            size = os.path.getsize(os.path.join(target_dir,item))
            is_dir = os.path.isdir(os.path.join(target_dir,item))
            item_details.append(f"- {name}: file size={size} bytes, is_dir={is_dir}")

    except:
        return "Error: unable to parse file/directory details"
    
    return "\n".join(item_details)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["directory"]
    ),
)