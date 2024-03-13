import json
import execjs

def create_prompt(config_file, traits_file, js_file):
    # Read the JavaScript function from createPrompt.js file
    with open(js_file, 'r') as js_file:
        js_code = js_file.read()
        print(js_code)

    # Load config and trait arguments from JSON files
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    with open(traits_file, 'r') as f:
        trait_args = json.load(f)

    # Create an ExecJS context
    ctx = execjs.compile(js_code)

    # Call the JavaScript function with arguments
    prompt = ctx.call('createPrompt', config, trait_args)
    return prompt

# Example usage
prompt = create_prompt('config.json', 'traits_definitions.json', 'createPrompt.js')
print(prompt)
