import difPy
import os


def get_subdirectories(folder_path):
    subdirectories = [f.path for f in os.scandir(folder_path) if f.is_dir()]
    return subdirectories


def main():
    # print(get_subdirectories('../data'))
    dif = difPy.build(get_subdirectories('../data'))
    search = difPy.search(dif)
    print(search.result)


if __name__ == "__main__":
    main()

