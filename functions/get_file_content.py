from functions import get_files_info
import os
from google import genai
from google.genai import types

work_dir_abs = "/home/amber/workspace/github.com/AmberPlusPlus/ai-agent"

def get_file_content(working_directory, file_path):

    abs_working_dir = os.path.normpath(os.path.abspath(working_directory))
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
    is_inside = abs_file_path == abs_working_dir or abs_file_path.startswith(abs_working_dir + os.sep)
    #valid_target_file = os.path.commonpath([abs_working_dir, abs_file_path]) == abs_working_dir

    print("DEBUG get_file_content:", repr(working_directory), repr(file_path), repr(abs_working_dir), repr(abs_file_path), "is_inside=", is_inside)


    if not is_inside:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    max_chars = 10000

    try:
        with open(abs_file_path, "r") as f:
            content = f.read(max_chars)
            if f.read(1):
                content += '[...File "'
                content += str(file_path)
                content += '" truncated at '
                content += str(max_chars)
                content += " characters]"
    except:
        return "Error: Unable to open specified file path"
    
    return content

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves contents of a file, up to a max of 10,000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the file to be opened.",
            ),
        },
        required=["file_path"]
    ),
)