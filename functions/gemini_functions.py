import sys;
import os;
from dependencies.dependencies import types,run_python_file, system_prompt, load_dotenv, genai, functions_dict;

class Gemini_Functions:
    def __init__(self: object):
        self.get_files_info: object = types.FunctionDeclaration(
            name="get_files_info",
            description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "directory": types.Schema(
                        type=types.Type.STRING,
                        description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                    ),
                    "r_flag" : types.Schema(
                        type = types.Type.BOOLEAN,
                        description = "a Bool value ues to set the function into recursive mode (i.e. List ALL files under working directory needs to be given permission to use it with a direct \"r_flag\" quote from user.\nExample: How's ??? function is implamented in file ?!?.py"
                    )
                },
            ),
        );
        self.get_file_content: object = types.FunctionDeclaration(
            name = 'get_file_content',
            description = "Retrices the file's content in the specified path, constrained to the working directory.",
            parameters = types.Schema(
                type = types.Type.OBJECT,
                properties = {
                    'file_path': types.Schema(
                        type = types.Type.STRING,
                        description = 'The file to retrive content from, relative to the working directory.',
                    ),
                },
            ),
        );
        self.run_python_file: object = types.FunctionDeclaration(
            name = 'run_python_file',
            description = "Retrices the file's content in the specified path, constrained to the working directory.",
            parameters = types.Schema(
                type = types.Type.OBJECT,
                properties = {
                    'file_path': types.Schema(
                        type = types.Type.STRING,
                        description = 'The file to retrive content from, relative to the working directory.',
                    ),
                },
            ),
        );
        self.write_file: object = types.FunctionDeclaration(
            name = 'write_file',
            description = "Retrices the file's content in the specified path, constrained to the working directory.",
            parameters = types.Schema(
                type = types.Type.OBJECT,
                properties = {
                    'file_path': types.Schema(
                        type = types.Type.STRING,
                        description = 'The file to retrive content from, relative to the working directory.',
                    ),
                    'content': types.Schema(
                    type = types.Type.STRING,  
                    description = 'The content to write to the file_path provided.'
                    ),
                },
            ),
        );

def call_function(function_call_part: object, verbose: bool = False):
    print(function_call_part.args)
    if not  function_call_part.name in functions_dict:
        return types.Content(
        role ="tool",
        parts = [
            types.Part.from_function_response(
                name=function_call_part.name,
                response = {
                    "error": f"Unknown function: {function_call_part.name}"
                },
            ),
        ],
    );
    argumemts: dict = function_call_part.args.copy();
    argumemts['working_directory'] = '.';
    func: function = functions_dict[function_call_part.name];
    return types.Content(
        role = "tool",
        parts = [
            types.Part.from_function_response(
                name = function_call_part.name,
                response = {
                    "result": func(**argumemts) 
                },
            ),
        ],
    );

def test_gemini_response() -> str:
    if (not load_dotenv()):
        return 'Error loading envoirnment file';
    
    verbose: bool = sys.argv[-1] == ("--verbose");
    
    if (verbose): 
        sys.argv.pop();
    
    query: str = " ".join(sys.argv[1 :]);
    
    if (not query): 
        raise(
            ValueError("Please Input A Prompt!")
        );
    
    functions: object = Gemini_Functions();
    available_funtions: object = types.Tool(
        function_declarations = [
            functions.get_files_info,
            functions.get_file_content,
            functions.run_python_file,
            functions.write_file
        ],
    );
    api_key: str = os.environ.get("GEMINI_API_KEY");
    client: object  = genai.Client(api_key = api_key);
    messages: list[object] = [
        types.Content(
            role = "user",
            parts = [types.Part(text= query)]
        )
    ];
    x: int = 20;
    
    for i in range(x):
        print(f'Iteration: {i}')
        response: object = client.models.generate_content(
                model = 'gemini-2.0-flash-001',
                contents = messages,
                config = types.GenerateContentConfig(
                    tools = [available_funtions, ],
                    system_instruction = system_prompt
                ),
            );
        if response.function_calls:
            for j in range(len(response.function_calls)):
                function_call_result:object = call_function(response.function_calls[j], verbose);
                messages.append(response.candidates[j].content);
                messages.append(function_call_result);
                #print(f'Messages: {messages}\n');
                if not (
                    function_call_result and
                    function_call_result.parts and
                    len(function_call_result.parts) > 0 &
                    hasattr(function_call_result.parts[0], 'function_response') &
                    hasattr(function_call_result.parts[0].function_response, 'response')
                ):
                        raise Exception("Unexpected function call response structure from call_function")
                print(f'Calling function: {response.function_calls[j].name}({response.function_calls[j].args})');           
            
            if (not response.candidates[0]) or (not response.candidates):
                if (verbose):
                    print(f'->{function_call_result.parts[0].function_response.response['result']}');
                    break
                else:
                    print(f' - Calling function: {response.function_calls[i].name}\n=>Response: {function_call_result.parts[0].function_response.response['result']}')
                    break
    print(f'Called functions: {response.function_calls[i].name}({response.function_calls[i].args})\n-> {function_call_result.parts[0].function_response.response['result']}');      
    if (verbose): 
        print(f'User prompt: {query}\n\nPrompt tokens: {response.usage_metadata.prompt_token_count}\n\nResponse tokens: {response.usage_metadata.candidates_token_count}\n\nResponse: {response.text}');
                
        
    

    else: 
        print(messages)
        print(response.text);
    
    
    print("exiting Convo")
    return;