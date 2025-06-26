from functions.Files_API import os, sys, subprocess, functions_dict;
from calculator.pkg.calculator import Calculator;
from calculator.pkg.render import render;
from dependencies.system_prompt import system_prompt;
from dotenv import load_dotenv;
from functions.Files_API import get_file_content, get_files_info, write_file, run_python_file, os, subprocess, sys;
from google.genai import types;
from google import genai;
from functions.gemini_functions import Gemini_Functions, call_function, test_gemini_response;
