import os
import re

def convert_java_to_markdown(directory):
    markdown_content = ""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)

                # 获取文件名
                file_name = os.path.basename(file_path)

                java_file_path = os.path.join(root, file)
                with open(java_file_path, "r", encoding="utf-8") as java_file:
                    markdown_content += "####" + file_name + "\n"
                    markdown_content += f"```java\n"
                    # markdown_content += f"// {java_file_path}\n"
                    line_number = 1
                    for line in java_file:
                        markdown_content += f"{line_number}. {line}"
                        line_number += 1
                    markdown_content += "\n```\n\n"
    return markdown_content

def read_java_prefix_with_line(directory):
    source=""
    with open(directory, "r", encoding="utf-8") as java_file:
        # markdown_content += f"// {java_file_path}\n"
        line_number = 1
        for line in java_file:
            source += f"{[line_number]} {line}"
            line_number += 1

    return source

def extract_numbers_from_lines(text):
    # 正则表达式匹配每一行开头的[数字]
    pattern = r'^\[\d+\]'

    # 使用re.finditer()查找所有匹配的[数字]
    matches = re.finditer(pattern, text, flags=re.MULTILINE)

    # 提取匹配的[数字]部分
    extracted_numbers = [match.group(0) for match in matches]
    clean_numbers = [match.group(0) for match in matches]

    for nu in extracted_numbers:
        clean_numbers.append(nu[1:-1])

    return clean_numbers


def remove_line_prefix(text):
    # 正则表达式匹配每一行开头的数字后跟一个点
    pattern = r'^(\d+\.)'

    # 使用re.sub()替换掉匹配的部分
    new_text = re.sub(pattern, '', text, flags=re.MULTILINE)

    return new_text


def convert_java_to_markdown(directory):
    markdown_content = ""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)

                # 获取文件名
                file_name = os.path.basename(file_path)

                java_file_path = os.path.join(root, file)
                with open(java_file_path, "r", encoding="utf-8") as java_file:
                    markdown_content += "####" + file_name + "\n"
                    markdown_content += f"```java\n"
                    # markdown_content += f"// {java_file_path}\n"
                    line_number = 1
                    for line in java_file:
                        markdown_content += f"{line_number}. {line}"
                        line_number += 1
                    markdown_content += "\n```\n\n"
    return markdown_content



def find_file(filename, start_path='.'):
    for root, dirs, files in os.walk(start_path):
        if filename in files:
            return os.path.join(root, filename)
    return None



def extract_source_from_line_numbers(line_numbers:list):
    formatted_numbers = ['\[' + item + '\]' for item in line_numbers]
    formatted_string = r'.*\n'.join(formatted_numbers)

    # filled_string = ''.join(['['+element+']' + r'.*\n' for element in line_numbers[:-1]] + ['['+[line_numbers[-1]]+']'])
    return formatted_string#filled_string


def extract_code_blocks(markdown_text):
    # 正则表达式匹配Markdown中的代码块
    # 这个正则表达式假设代码块使用三个反引号包围，可能包含语言指定
    pattern = r'[a-zA-Z_]\w*.java.*\n+```.*\n([\s\S]*?)```'

    # 使用re.findall()查找所有匹配的代码块
    code_blocks = re.findall(pattern, markdown_text)

    return code_blocks



def apply_patches(directory,patch_file):
    patch_file_directory = os.path.join(directory, patch_file)
    response=""
    if os.path.exists(patch_file_directory):
        # 如果存在，则读取文件内容
        with open(patch_file_directory, "r") as file:
            response = file.read()
    else:
        return False

    codes=extract_code_blocks(response)
    files=extract_filename_with_code_block(response)
    if len(codes)!= len(files):
        return False
    for c,f in zip(codes,files):
        clean_c=remove_line_prefix(c)
        found_path = find_file(f, directory)
        if found_path==None:
            return False
        #code_with_line_numer=read_java_prefix_with_line(found_path)
        with open(found_path, 'w') as file:
             file.write(clean_c)
    return True



def remove_unwanted_lines(texts: list):
    if not isinstance(texts, list):
        raise TypeError("Input must be a list")
    pattern = r"^\[\d+\].*"
    filtered_texts=[]
    for text in texts:
        matches = re.findall(pattern, text, re.MULTILINE)
        filtered_texts.append("\n".join(matches))
    return filtered_texts

    # for text in texts:



def extract_changelog_sections(text):
    # 正则表达式匹配模式，匹配"ChangeLog:数字@所在行"，使用非贪婪匹配
    pattern = r"(ChangeLog:\d+@)(.*?)(?=ChangeLog:\d+@|$)"

    # 使用re.DOTALL使.匹配包括换行符在内的所有字符
    # 使用re.finditer查找所有匹配项
    matches = re.finditer(pattern, text, re.DOTALL)

    # 提取匹配的内容
    extracted_texts = [match.group(1) + match.group(2) for match in matches]

    return extracted_texts


def extract_content(begin,end,text):
    # 正则表达式匹配模式，匹配"OriginalCode@所在行"到下一个"FixedCode@"
    #pattern = r"(OriginalCode@\d+.*?\n)(.*?)(?=FixedCode@|\Z)"
    pattern = r"("+begin+r"\d+.*?\n)(.*?)(?="+end+r"|\Z)"
    # 使用re.DOTALL使.匹配包括换行符在内的所有字符
    # 使用re.finditer查找所有匹配项
    matches = re.finditer(pattern, text, re.DOTALL)

    # 提取匹配的内容
    extracted_contents = []
    for match in matches:
        # match.group(1) 是"OriginalCode@所在行"及其后的第一个换行符
        # match.group(2) 是"OriginalCode@所在行"和下一个"FixedCode@所在行"之间的所有内容
        extracted_contents.append(match.group(2))

    # 检查是否有最后一个OriginalCode@到文档末尾的内容需要提取
    # 如果文档以FixedCode@结束，我们需要提取从最后一个OriginalCode@到文档末尾的内容
    if re.search(begin+r"\d+.*?$", text):
        last_original_code = re.search(begin+r"\d+.*?$", text)
        last_content = text[last_original_code.start():]
        extracted_contents.append(last_content.strip())

    return extracted_contents


def extract_by_prefix(text, prefixes):
    lines = text.splitlines()

    # 遍历每一行
    for line in lines:
        # 检查行是否以'a'开头，strip()用于去除行首行尾的空白字符

        if line.strip().startswith('a'):
            # 输出以'a'开头的行
            print(line)

    # 创建一个正则表达式模式，匹配列表中任何元素作为开头的字符串
    # 转义列表中的每个元素，以确保特殊字符被视为普通字符
    # 使用'|'作为逻辑或操作符来分隔不同的前缀
    escaped_prefixes = map(re.escape, prefixes)  # 转义所有可能的特殊字符
    pattern = r'\b(' + '|'.join(escaped_prefixes) + r')\b'

    # 使用re.finditer()查找所有匹配项
    matches = re.finditer(pattern, text)

    # 提取所有匹配的字符串
    extracted_texts = [match.group(0) for match in matches]

    return extracted_texts



def extract_filename_with_code_block(markdown_text):
    # 正则表达式匹配文件名，后面紧跟换行符号和Markdown代码块
    # 假设文件名由字母、数字、下划线、短横线或点组成
    # pattern = r'(\w[\w\-\.]*)\n```'
    pattern =r'([a-zA-Z_]\w*.java).*\n+```'

    # 使用re.findall()查找所有匹配的文件名
    filenames = re.findall(pattern, markdown_text)

    return filenames


def extract_code_from_markdown(markdown_text):
    # 正则表达式匹配Markdown中的代码块内容
    # 这个正则表达式假设代码块使用三个反引号包围，可能包含语言指定
    pattern = r'```([\s\S]*?)```'

    # 使用re.findall()查找所有匹配的代码块
    code_blocks = re.findall(pattern, markdown_text)

    # 提取每个代码块内部的内容（去掉外围的反引号）
    extracted_code = []
    for block in code_blocks:
        # 分割代码块为行，并去掉首尾空白字符
        lines = block.strip().split('\n')
        # 去掉第一行和最后一行（通常是```）
        clean_lines = lines[1:-1]
        # 去掉每行开头和结尾的空白字符，并合并回一个字符串
        code = '\n'.join(line.strip() for line in clean_lines)
        extracted_code.append(code)

    return extracted_code


# # 示例Markdown文本
# markdown_text = """
# ```
#
# ManageAccount.java
# ```java
# """
#
# # 调用函数并打印结果
# filenames = extract_filename_with_code_block(markdown_text)
# for filename in filenames:
#     print(filename)
# text='''
# ```python
# # 这是一个Python代码块
# print("Hello, World!")
# ```
# '''
# print(extract_code_blocks(text))

