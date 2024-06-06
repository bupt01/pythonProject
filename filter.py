import os
import re
import shutil


from pathlib import Path

from main1 import list_direct_subdirectories


class JavaCommentFilter:
    def __init__(self, file_path: str):
        """
        初始化工具类，读取Java文件内容。
        :param file_path: Java源文件的路径。
        """
        self.file_path = Path(file_path)
        self.content = self._read_file()

    def _read_file(self) -> str:
        """
        读取Java文件的全部内容。
        :return: 文件内容字符串。
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def filter_comments(self) -> str:
        """
        过滤掉Java源代码中的单行和多行注释。
        :return: 过滤注释后的代码字符串。
        """
        # 匹配单行注释
        pattern_single_line_comment = re.compile(r'//.*')
        # 匹配多行注释的开始和结束
        pattern_multi_line_comment = re.compile(r'/\*.*?\*/', re.DOTALL)

        # 移除单行注释
        content_without_single_line_comments = re.sub(pattern_single_line_comment, '', self.content)
        # 移除多行注释
        content_without_comments = re.sub(pattern_multi_line_comment, '', content_without_single_line_comments)

        return content_without_comments

    def save_filtered_content(self, output_path: str):
        """
        将过滤掉注释后的代码保存到文件。
        :param output_path: 输出文件的路径。
        """
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(self.filter_comments())

class JavaProjectCleaner:
    def __init__(self, file_path: str):
        """
        初始化工具类，读取Java文件内容。
        :param file_path: Java源文件的路径。
        """
        self.file_path = Path(file_path)

    def clean(self):
        direct_subdirectories = list_direct_subdirectories(self.file_path)
        for subdir in direct_subdirectories:
            # print(subdir)
            for root, dirs, files in os.walk(subdir):
                for file in files:
                    if file.endswith(".java"):
                        file_path = os.path.join(root, file)
                        filter=JavaCommentFilter(file_path)
                        clean_code=filter.filter_comments()
                        dest=os.path.join(root, (file+".ori"))
                        if not Path(dest).exists():
                            try:
                                shutil.copy(file_path, dest)
                                print(f"File copied from {file} to {dest}")
                            except IOError as e:
                                print(f"Unable to copy file. {e}")
                        with open(file_path, 'w') as file:
                            file.write(clean_code)

# 使用示例
if __name__ == "__main__":
    # file_path = 'Example.java'  # 指定Java文件的路径
    # output_path = 'ExampleFiltered.java'  # 指定输出文件的路径
    # file_path="E:/mywork/LLM4CFIX/LLM4CFIX/src/main/java/airline/Bug.java"
    #
    # comment_filter = JavaCommentFilter(file_path)
    # print(comment_filter.filter_comments())
    # comment_filter.save_filtered_content(output_path)
    # print(f"Filtered content saved to {output_path}")
    direct_subdirectories=list_direct_subdirectories("E:\mywork\FixExamples-master\main")
    #打印直接子目录列表
    for subdir in direct_subdirectories:
        # print(subdir)
        loc = 0
        for root, dirs, files in os.walk(subdir):
            for file in files:
                if file.endswith(".ori"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        # loc+=sum(1 for _ in f)
                        loc+=len(f.read())
        index = subdir.rfind('\\')
        pro_name=subdir[index + 1:]
        print(str(loc))
    # cleaner=JavaProjectCleaner("E:\mywork\FixExamples-master\main")
    # cleaner.clean()
