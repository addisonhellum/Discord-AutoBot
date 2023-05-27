from colorama import Fore, Style
import subprocess
import openai
import atexit
import signal
import sys
import os

# Load your API key from an environment variable or secret management service
openai.api_key = "{OPENAI API KEY HERE}"

# Ask user what the generated code should do
goal = input(f'{Fore.GREEN}What should the code do? {Style.RESET_ALL}')

# Read example library usage file
print(f'\n{Fore.YELLOW}Analyzing documentation...{Style.RESET_ALL}')
example_file = open('example.py', 'r')
example_contents = example_file.read()

# Ask GPT 3.5-Turbo to generate code using the library to accomplish specified task
print(f'{Fore.YELLOW}Generating code...{Style.RESET_ALL}')
response = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages = [
        {'role': 'system', 'content': 'Here is an example of how a library should be used, with comments:\n\n---\n\n'+example_contents},
        {'role': 'user', 'content': 'Using only the library given, write Python code (with imports) to '+goal+'. Respond with only the code, no additional text or explanations.'},
    ],
    max_tokens = 2000
)

generated_code = response.choices[0]['message']['content']
if ('```python' in generated_code): generated_code = generated_code.split('```python')[1]
elif ('```' in generated_code): generated_code = generated_code.split('```')[1]
generated_code = generated_code.replace('```', '')

# Define a function to delete the temporary file
def delete_file():
    os.remove('tmp.py')

# Define a function to handle the SIGINT signal
def sigint_handler(signal, frame):
    atexit._run_exitfuncs()
    sys.exit(0)

# Register the function to delete the file on exit
atexit.register(delete_file)

# Register the function to handle the SIGINT signal
signal.signal(signal.SIGINT, sigint_handler)

# Write generated code to a file as tmp.py
print(f'{Fore.YELLOW}Saving code to file...{Style.RESET_ALL}\n')
with open('tmp.py', 'w') as f:
    f.write(generated_code)

# Run the generated Python code
try:
    # Execute the code in the temporary run file
    print(f'{Fore.GREEN}Running script... press CTRL + C to exit.{Style.RESET_ALL}')
    print(f'\n{Fore.WHITE}{generated_code}{Style.RESET_ALL}\n')
    subprocess.run(['python3', 'tmp.py'], check=True)

except subprocess.CalledProcessError as e:
    # Some error in the generated code, print the problematic code
    print(Fore.RED + generated_code + Style.RESET_ALL)