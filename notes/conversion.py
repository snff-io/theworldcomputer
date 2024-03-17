import os
import re
import shutil
import sys

def convert_csharp_to_python(csharp_code):
    # Define regular expressions for C# constructs
    class_pattern = r'class\s+(\w+)\s*{([^}]+)}'
    method_pattern = r'(\w+)\s+(\w+)\s*\(([^)]*)\)\s*{([^}]+)}'

    # Find all classes in the C# code
    classes = re.findall(class_pattern, csharp_code, re.MULTILINE | re.DOTALL)

    python_code = ''
    for class_match in classes:
        class_name, class_body = class_match
        python_code += f'class {class_name}:\n'

        # Find all methods in the class
        methods = re.findall(method_pattern, class_body)
        for method_match in methods:
            return_type, method_name, params, method_body = method_match
            python_code += f'    def {method_name}({params}):{method_body}\n'

    return python_code

def convert_file(input_path, output_path):
    with open(input_path, 'r') as f:
        csharp_code = f.read()
    python_code = convert_csharp_to_python(csharp_code)
    with open(output_path, 'w') as f:
        f.write(python_code)

def convert_directory(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".cs"):
                input_file = os.path.join(root, file)
                output_file = input_file.replace(input_dir, output_dir)[:-2] + "py"
                output_dirname = os.path.dirname(output_file)
                os.makedirs(output_dirname, exist_ok=True)
                convert_file(input_file, output_file)

def main(input_dir, output_dir):
    convert_directory(input_dir, output_dir)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csharp_to_python.py <input_dir> <output_dir>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    main(input_dir, output_dir)
