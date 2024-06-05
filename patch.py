import re

# # 读取Java源文件内容
# with open("E:/mywork/LLM4CFIX/LLM4CFIX/src/main/java/alarmclock/AlarmClock.java", 'r') as file:
#     java_code = file.read()
#
#
# class_name = 'Clock'
# # class_pattern = re.compile(
# #     r'\bclass\s+' + re.escape(class_name) +
# #     r'\s*(extends\s+\w+(<.*?>)?|implements\s+\w+(<.*?>)?)*\s*\{([^}]*)\}',
# #     re.DOTALL
# # )
# class_pattern = re.compile(
#     rf'\bclass\s+{re.escape(class_name)}'
#     r'(\s*extends\s+\w+(<.*?>)?\s*)?'
#     r'(\s*implements\s+\w+(<.*?>)?\s*)*'
#     r'\s*\{{([^}]*)\}\s*;',
#     re.DOTALL
# )
#
# # 使用正则表达式搜索匹配的类定义
# match = class_pattern.search(java_code)
#
# if match:
#     # 如果找到了匹配的类，打印类名和代码
#     print(f"Found class '{class_name}' with the following code:")
#     print(match.group(1).strip())  # 打印类定义（不包括类名和大括号）
# else:
#     print(f"Class '{class_name}' not found in the source code.")
#
# import re


def find_class_in_java_file(file_path, class_name):
    with open(file_path, 'r') as file:
        content = file.read()

    # 构建一个正则表达式，用于匹配类的开始和结束
    class_pattern = re.compile(r'\bclass\s+' + re.escape(class_name) + r'\b.*?\{(?:[^{}]*|\{[^{}]*\})*\}', re.S)

    # 搜索匹配的类
    match = class_pattern.search(content)
    if match:
        return match.group()
    else:
        return None


# 示例用法
file_path = "E:/mywork/LLM4CFIX/LLM4CFIX/src/main/java/alarmclock/AlarmClock.java"
class_name = 'Clock'
class_code = find_class_in_java_file(file_path, class_name)

if class_code:
    print("找到类代码：")
    print(class_code)
else:
    print("未找到指定类")
