import os
import tools


def list_direct_subdirectories(directory):
    subdirectories = []
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_dir():
                subdirectories.append(os.path.join(directory, entry.name))
    return subdirectories


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def generate_prompt1_1(subdir,source):
    prompt = "##### You are given a concurrent program source code that may contain concurrency bugs along with explanations of the types of concurrency bugs.\n"
    prompt+="###source code\n"
    prompt+=source
    prompt += "###types of concurrency bugs\n"
    prompt += "1. Atomicity Violation: Occurs when an operation, which should be indivisible, gets interrupted or incomplete due to concurrent execution. This can lead to inconsistent or corrupted data.\n2. Order Violation: Happens when the expected sequence of operations in a concurrent program is disrupted, often due to improper synchronization or race conditions. This can result in unexpected outcomes or errors.\n3. Deadlock: A situation where two or more processes or threads are unable to proceed because each is waiting for the other to release a resource, leading to a standstill in program execution.\n4. Data Race: Occurs when two or more threads access shared data concurrently, with at least one thread performing a write operation, without proper synchronization. This can lead to unpredictable behavior and data corruption.\n"
    prompt +="### instruction\n"
    prompt +="Does the concurrent program contain any concurrency-related bugs? If so, please fix them. Please ensure that fixing doesn't introduce new bugs, such as deadlocks.Try to minimize the impact on concurrency due to the fixes. Do not attempt to change the functionality of any function, and do not modify any code that is unrelated to concurrency bugs."
    prompt += "For your answer, first comes a description of your fix. For example:\n"
    prompt += "Deascription:<summary>\n"
    prompt += "Your answer is then followed by all source code after applying the fix you propose.Each source code file corresponds to a code block. Before outputting each code block, the filename of the corresponding source code file should be displayed.For example:\n"
    prompt += "A.java\n"
    prompt += "<After applying the patch, all source code contents of A.java.>\n"
    prompt += "B.java\n"
    prompt += "<After applying the patch, all source code contents of B.java.>\n"
    file_path = os.path.join(subdir, "prompt1.txt")
    with open(file_path, 'w') as file:
        file.write(prompt)
    return prompt

def generate_prompt1(directory):
    # 调用函数列出所有直接子目录
    direct_subdirectories = list_direct_subdirectories(directory)

    # 打印直接子目录列表
    for subdir in direct_subdirectories:
        source = tools.convert_java_to_markdown(subdir)  # read source, format: line+code
        prompt1 = generate_prompt1_1(subdir, source)




def generate_prompt2_1(subdir,source):
    prompt=generate_prompt3_1(subdir,source)
    return prompt

def generate_prompt2_2(subdir,source):
    prompt = "##### You are given a concurrent program source code that may contain concurrency bugs, along with a concurrency bug detection report from ChatGPT\n"
    prompt += "### source code\n"
    prompt += source
    prompt +="### bug report\n"
    bug_report_path = os.path.join(subdir, "response1.txt")
    if os.path.exists(bug_report_path):
        # 如果存在，则读取文件内容
        with open(bug_report_path, "r") as file:
            bug_report = file.read()
            prompt += bug_report
    prompt += "\n"
    prompt +="### instruction\n"
    prompt +="Fix the concurrency bugs in this program.Please ensure that fixing doesn't introduce new bugs, such as deadlocks.Try to minimize the impact on concurrency due to the fixes. Do not attempt to change the functionality of any function, and do not modify any code that is unrelated to concurrency bugs. Please ensure that your response contains all the source code after you have fixed the program."
    prompt +="For your answer, first comes a description of your fix. For example:\n"
    prompt +="Deascription:<summary>\n"
    prompt +="Your answer is then followed by all source code after applying the fix you propose.Each source code file corresponds to a code block. Before outputting each code block, the filename of the corresponding source code file should be displayed.For example:\n"
    prompt +="A.java\n"
    prompt +="<After applying the patch, all source code contents of A.java.>\n"
    prompt +="B.java\n"
    prompt +="<After applying the patch, all source code contents of B.java.>\n"

    # prompt +="For eaxmple:"
    #          "If you believe the input fix does not require further modification, you can respond with the input ChangeLog. Do not attempt to change the functionality of any function, and do not modify any code that is unrelated to concurrency bugs."
    #
    # prompt +="Your response should include all source code after applying final version of the fix you propose.If you believe the input fix does not require further modification, you can directly apply it to fix the source code.Do not attempt to change the functionality of any function, and do not modify any code that is unrelated to concurrency bugs."

    file_path = os.path.join(subdir, "prompt2.txt")
    with open(file_path, 'w') as file:
        file.write(prompt)
    return prompt

# # 将markdown内容写入文件
# with open("java_code.md", "w", encoding="utf-8") as markdown_file:
#     markdown_file.write(markdown_content)
#
# print("Java源码已转换为Markdown格式并保存到java_code.md文件中。")


def generate_prompt3_1(subdir,source):
    prompt="##### You were given a program source code that may contain concurrency bugs, along with explanations of the types of concurrency bugs.\n"
    prompt+="###source code\n"
    prompt+=source
    prompt+="###types of concurrency bugs\n"
    prompt+="1. Atomicity Violation: Occurs when an operation, which should be indivisible, gets interrupted or incomplete due to concurrent execution. This can lead to inconsistent or corrupted data.\n2. Order Violation: Happens when the expected sequence of operations in a concurrent program is disrupted, often due to improper synchronization or race conditions. This can result in unexpected outcomes or errors.\n3. Deadlock: A situation where two or more processes or threads are unable to proceed because each is waiting for the other to release a resource, leading to a standstill in program execution.\n4. Data Race: Occurs when two or more threads access shared data concurrently, with at least one thread performing a write operation, without proper synchronization. This can lead to unpredictable behavior and data corruption.\n"
    prompt+="###Instructions\n"
    prompt+="Please check if this concurrent program has any concurrency bugs.For your response, return one or more bug reports, each report should include the type of the concurrency bug, a detailed description of that bug and the locations of the concurrecy bug. Specially, indicate the bug locations using file names and line numbers.Each report must be formatted with the below instructions.\n"
    prompt+="Format instructions: Please do not use Markdown format in your response.Each bug report should start with the bug type, followed by a detailed description of that bug and end with the bug locations.For example:\n"
    # prompt+="Bug Type: [Type of Bug Detected] \nDescription: [Description of the Bug]\n"
    # prompt+="For Example:\n"
    prompt+="Bug Report 1:\n"
    prompt+="Bug Type: [Type of Bug Detected] \nDescription: [Description of the Bug]\n"
    prompt+="Bug Location: [File of Bug Detected:line number]\n"
    prompt += "Bug Report 2:\n"
    prompt += "Bug Type: [Type of Bug Detected] \nDescription: [Description of the Bug]\n"
    prompt+="Bug Location: [File of Bug Detected:line number]\n"
    prompt += "...\n"
    prompt += "Bug Report k:\n"
    prompt += "Bug Type: [Type of Bug Detected] \nDescription: [Description of the Bug]\n"
    prompt += "Bug Location: [Files of Bug Detected:line number]\n"

    file_path = os.path.join(subdir, "prompt1.txt")
    with open(file_path, 'w') as file:
        file.write(prompt)
    return prompt

def generate_prompt3_2(subdir,source):
    prompt = "##### You are given a concurrent program source code that may contain concurrency bugs, along with a concurrency bug detection report from ChatGPT.\n"
    prompt += "### source code\n"
    prompt += source
    prompt += "### bug report\n"

    bug_report_path = os.path.join(subdir, "response1.txt")
    if os.path.exists(bug_report_path):
        # 如果存在，则读取文件内容
        with open(bug_report_path, "r") as file:
            bug_report = file.read()
            prompt +=bug_report
    prompt += "\n"
    prompt+="### Instructions\n"
    prompt+="Fix the concurrency bugs in this program.Please ensure that fixing doesn't introduce new bugs, such as deadlocks.Try to minimize the impact on concurrency due to the fixes. Do not attempt to change the functionality of any function, and do not modify any code that is unrelated to concurrency bugs.Note that you don't need to reply with the entire source code after it's been fixed. Just provide the parts that were modified.For your answer, return one or more ChangeLog groups, each containing one or more fixes to the above code snippets. Each group must be formatted with the below instructions.\n"
    prompt+="Format instructions: Each ChangeLog group must start with a description of its included fixes. The group must then list one or more pairs of (OriginalCode , FixedCode) code snippets. Each OriginalCode snippet must list all consecutive original lines of code that must be replaced (including a few lines before and after the fixes), followed by the FixedCode snippet with all consecutive fixed lines of code that must replace the original lines of code (including the same few lines before and after the changes). In each pair , the OriginalCode and FixedCode snippets must start at the same source code line number N. Each listed code line, in both the OriginalCode and FixedCode snippets must be prefixed with [N] that matches the line index N in the above snippets , and then be prefixed with exactly the same whitespace indentation as the original snippets above."
    prompt+="For example:\n"
    prompt+="ChangeLog:1@<file>\nFixDescription: <summary>.\nOriginalCode@4-6:\n[4] <white space> <original code line>\n[5] <white space> <original code line>\n[6] <white space> <original code line>\nFixedCode@4-6:\n[4] <white space> <fixed code line>\n[5] <white space> <fixed code line>\n[6] <white space> <fixed code line>\nOriginalCode@9 -10:\n[9] <white space> <original code line>\n[10] <white space> <original code line>\nFixedCode@9-9: \n[9] <white space> <fixed code line>\nChangeLog:2@<file>\nFixDescription: <summary>.\nOriginalCode@15-16:\n[15] <white space> <original code line>\n[16]<white space> <original code line>\nFixedCode@15-16:\n[15] <white space> <fixed code line>\n[16] <white space> <fixed code line>\nOriginalCode@23-23:\n[23] <white space> <original code line>\nFixedCode@23-23:\n[23] <white space> <fixed code line>\n"


    file_path = os.path.join(subdir, "prompt2.txt")
    with open(file_path, 'w') as file:
        file.write(prompt)
    return prompt

def generate_prompt3_3(subdir,source):
    prompt = "##### You are given a concurrent program source code that may contain concurrency bugs, along with a concurrency bug detection report from ChatGPT, as well as the corresponding changelog for the fixes suggested by ChatGPT.\n"
    prompt += "### source code\n"
    prompt += source
    prompt +="### bug report\n"
    bug_report_path = os.path.join(subdir, "response1.txt")
    if os.path.exists(bug_report_path):
        # 如果存在，则读取文件内容
        with open(bug_report_path, "r") as file:
            bug_report = file.read()
            prompt += bug_report
    prompt += "\n"
    prompt +="### changelog for the fixes\n"

    fix = os.path.join(subdir, "response2.txt")
    if os.path.exists(fix):
        # 如果存在，则读取文件内容
        with open(fix, "r") as file:
            bug_report = file.read()
            prompt += bug_report
    prompt += "\n"
    prompt +="### instruction\n"
    prompt +="Please check:\n1. Whether the fix can address the concurrency bug.\n2. Whether the fix introduces new concurrency bugs (such as deadlocks).\n3. Whether the fix introduces unnecessary synchronization, potentially affecting the performance of concurrent programs.\n"
    # prompt +="For your answer, first comes a description of the correctness and quality of the fix corresponding to the input ChangeLog. For example:\n"
    # prompt +="Evaluation for input fixes:<summary>\n"
    #
    # prompt +="Your answer is followed by one or more ChangeLog groups for the final version of the fix you propose. If you believe the input fix does not require further modification, you can respond with the input ChangeLog. Do not attempt to change the functionality of any function, and do not modify any code that is unrelated to concurrency bugs."
    #
    # prompt +="For each ChangeLog group, containing one or more fixes to the above code snippets. Each group must be formatted with the below instructions.\n"
    #
    # prompt +="Format instructions: Each ChangeLog group must start with a description of its included fixes. The group must then list one or more pairs of (OriginalCode , FixedCode) code snippets. Each OriginalCode snippet must list all consecutive original lines of code that must be replaced (including a few lines before and after the fixes), followed by the FixedCode snippet with all consecutive fixed lines of code that must replace the original lines of code (including the same few lines before and after the changes). In each pair, the OriginalCode and FixedCode snippets must start at the same source code line number N. Each listed code line , in both the OriginalCode and FixedCode snippets , must be prefixed with [N] that matches the line index N in the above snippets, and then be prefixed with exactly the same whitespace indentation as the original snippets above."
    #
    # prompt += "For example:\n"
    # prompt += "ChangeLog:1@<file>\nFixDescription: <summary>.\nOriginalCode@4-6:\n[4] <white space> <original code line>\n[5] <white space> <original code line>\n[6] <white space> <original code line>\nFixedCode@4-6:\n[4] <white space> <fixed code line>\n[5] <white space> <fixed code line>\n[6] <white space> <fixed code line>\nOriginalCode@9 -10:\n[9] <white space> <original code line>\n[10] <white space> <original code line>\nFixedCode@9-9: \n[9] <white space> <fixed code line>\nChangeLog:2@<file>\nFixDescription: <summary>.\nOriginalCode@15-16:\n[15] <white space> <original code line>\n[16]<white space> <original code line>\nFixedCode@15-16:\n[15] <white space> <fixed code line>\n[16] <white space> <fixed code line>\nOriginalCode@23-23:\n[23] <white space> <original code line>\nFixedCode@23-23:\n[23] <white space> <fixed code line>\n"
    prompt +="For your answer, first comes a description of the correctness and quality of the fix corresponding to the input ChangeLog. For example:\n"
    prompt +="Evaluation for input fixes:<summary>\n"
    prompt +="Your answer is then followed by all source code after applying final version of the fix you propose.Each source code file corresponds to a code block. Before outputting each code block, the filename of the corresponding source code file should be displayed.For example:\n"
    prompt +="A.java\n"
    prompt +="<After applying the patch, all source code contents of A.java.>\n"
    prompt +="B.java\n"
    prompt +="<After applying the patch, all source code contents of B.java.>\n"
    prompt +="Please note that if you believe the input fix does not require further modification, you can directly apply it to fix the source code.Do not attempt to change the functionality of any function, and do not modify any code that is unrelated to concurrency bugs."

    # prompt +="For eaxmple:"
    #          "If you believe the input fix does not require further modification, you can respond with the input ChangeLog. Do not attempt to change the functionality of any function, and do not modify any code that is unrelated to concurrency bugs."
    #
    # prompt +="Your response should include all source code after applying final version of the fix you propose.If you believe the input fix does not require further modification, you can directly apply it to fix the source code.Do not attempt to change the functionality of any function, and do not modify any code that is unrelated to concurrency bugs."

    file_path = os.path.join(subdir, "prompt3.txt")
    with open(file_path, 'w') as file:
        file.write(prompt)
    return prompt
"""Please note that no code content should be omitted between consecutive lines of code."""



""" prompt1 """
def generate_prompt2(directory):
    # 调用函数列出所有直接子目录
    direct_subdirectories = list_direct_subdirectories(directory)

    # 打印直接子目录列表
    for subdir in direct_subdirectories:
        source = tools.convert_java_to_markdown(subdir)     # read source, format: line+code
        prompt1 = generate_prompt1_1(subdir,source)

""" prompt2 """
def generate_prompt2(directory):
    # 调用函数列出所有直接子目录
    direct_subdirectories = list_direct_subdirectories(directory)

    # 打印直接子目录列表
    for subdir in direct_subdirectories:
        source = tools.convert_java_to_markdown(subdir)     # read source, format: line+code
        prompt1 = generate_prompt2_1(subdir,source)
        prompt2 = generate_prompt2_2(subdir,source)




""" prompt3 """
def generate_prompt3(directory):
    # 调用函数列出所有直接子目录
    direct_subdirectories = list_direct_subdirectories(directory)

    # 打印直接子目录列表
    for subdir in direct_subdirectories:
        source = tools.convert_java_to_markdown(subdir)     # read source, format: line+code
        prompt1 = generate_prompt3_1(subdir,source)
        prompt2 = generate_prompt3_2(subdir,source)
        prompt3 = generate_prompt3_3(subdir,source)





    # source=readSource("")
    #


def apply_patches(directory,patch_file):
    # 调用函数列出所有直接子目录
    direct_subdirectories = list_direct_subdirectories(directory)

    # 打印直接子目录列表
    for subdir in direct_subdirectories:
        flag=tools.apply_patches(subdir, patch_file)
        if flag:
            print(subdir+" apply patches successfully")
        else:
            print(subdir+" failture")


"""
generate_promote1:为第一组实验生成prompt(每个被测程序1个prompt)
generate_promote2:为第二组实验生成prompt(每个被测程序2个prompt)
generate_promote3:为第三组实验生成prompt(每个被测程序3个promopt)
"""
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #generate_prompt2("E:/mywork/LLM4CFIX/LLM4CFIX/src/main/java/LLM235")
    #generate_prompt1("E:/mywork/LLM4CFIX/LLM4CFIX/src/main/java/LLM14")
    #generate_prompt3("E:/mywork/LLM4CFIX/LLM4CFIX/src/main/java/LLM335")
    #tools.apply_patches("E:/mywork/LLM4CFIX/LLM4CFIX/src/main/java/LLM135","response1.txt")
    apply_patches("E:/mywork/LLM4CFIX/LLM4CFIX/src/main/java/LLM14","response1.txt")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# source = tools.convert_java_to_markdown("E:/mywork/LLM4CFIX/LLM4CFIX/src/main/java/LLM335/mergesort")  # read source, format: line+code
# prompt1 = generate_prompt3_1("E:/mywork/LLM4CFIX/LLM4CFIX/src/main/java/LLM335/mergesort", source)
