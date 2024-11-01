import os
import zipfile

import pysrt


class FilesMagic:
    def __init__(self, input_directory="./simpsons/", srt_directory="./srt/", txt_directory="./txt/",
                 cleaned_directory="./cleaned/"):
        self.input_directory = input_directory
        self.srt_directory = srt_directory
        self.txt_directory = txt_directory
        self.cleaned_directory = cleaned_directory

    def unzip_directory(self, directory=None, output_dir=None):
        if not directory:
            directory = self.input_directory
        if not output_dir:
            output_dir = self.srt_directory

        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)

            if os.path.isdir(item_path):
                self.unzip_directory(item_path, output_dir)

            elif item.endswith(".zip"):
                with zipfile.ZipFile(item_path, 'r') as zip_ref:
                    try:
                        zip_ref.extractall(output_dir)
                    except zipfile.BadZipfile:
                        print(end="")

    def srt_to_txt(self):
        input_dir = self.srt_directory
        output_dir = self.txt_directory

        total_count = 0
        delete_count = 0
        completely_fucked_count = 0
        for root, dirs, files in os.walk(input_dir):
            for filename in files:
                if filename.endswith(".srt"):
                    srt_file = os.path.join(input_dir, filename)
                    txt_file = os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")
                    line_count = 0
                    os.makedirs(os.path.dirname(txt_file), exist_ok=True)
                    try:
                        subs = pysrt.open(srt_file, encoding="utf-8")
                        with open(txt_file, "w") as txt:
                            for sub in subs[:-1]:
                                txt.write(sub.text + " ")
                                line_count += 1
                    except UnicodeDecodeError:
                        line_count = 100
                        completely_fucked_count += 1
                    except UnicodeEncodeError:
                        print(end="")
                    total_count += 1
                    if line_count < 100:
                        os.remove(txt_file)
                        delete_count += 1
        print(f"Total files = {total_count}\nFiles fucked too early = {delete_count}\nCan't open files = "
              f"{completely_fucked_count}\nGot files in the end = {total_count - delete_count - completely_fucked_count}")

    def nuke_special_chars(self):
        directory = self.txt_directory
        output = self.cleaned_directory
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                before = os.path.join(directory, filename)
                after = os.path.join(output, filename)
                os.makedirs(os.path.dirname(after), exist_ok=True)
                with open(before, 'r') as file:
                    text = file.read()
                    cleaned_text = ''.join(' ' if c.isspace() else c if c.isalpha() or c == '\'' else ' ' for c in text)
                    cleaned_text = ' '.join(cleaned_text.split())
                with open(after, 'w') as file:
                    file.write(cleaned_text)

    def get_files(self):
        self.unzip_directory()
        self.srt_to_txt()
        self.nuke_special_chars()


if __name__ == "__main__":
    magic = FilesMagic()
    magic.get_files()
