import shutil
import sys
import os

filename = sys.argv[1]

args = sys.argv[2:]

target_dir = "results"

str_args = ""

times = 5

for arg in args:
    str_args += str(arg) + " "

def check_target_dir(target_dir):
    if target_dir not in os.listdir():
        return False
    else:
        return os.path.isdir(target_dir)

def create_target_dir(target_dir):
    try:
        os.mkdir(target_dir)
        return True
    
    except FileExistsError:
        return False

def remove_target_dir(target_dir):
    try:
        shutil.rmtree(target_dir)
        return True

    except FileNotFoundError:
        return False

def create_info_data(storage, hash, memo):
    if memo == "--no-cache":
        os.system(f"python3 ./{filename} {str_args} --no-cache >> {target_dir}/no-cache")
        return "Done --no-cache"
    else:
        beg = f"python3 ./{filename} "
        end = f"-m {memo} -H {hash} -s {storage} >> {target_dir}/{storage}#{hash}#{memo}"
        os.system(beg + str_args + end)
        return f"Done {storage} {hash} {memo}"


memories = ['2d-ad-t', '1d-ow', '1d-ad', '2d-ad', 'ad', '2d-ad-f', '2d-ad-ft', '2d-lz']

hashes = ['md5', 'murmur', 'xxhash']

storages = ['db-file', 'db', 'file']

def main():
    remove_target_dir(target_dir)
    
    if not create_target_dir(target_dir):
        exit("Erro ao adicionar diretorio")
    
    if not check_target_dir(target_dir):
        exit("Diretorio nao foi achado...")

    for storage in storages:
        for hash in hashes:
            for memo in memories:
                for i in range(times):
                    print(create_info_data(storage, hash, memo))
        remove_target_dir("./.intpy")

    for i in range(times):
        print(create_info_data("","",memo="--no-cache"))
            
if __name__ == '__main__':
    main()

# 2d-ad-t é a versão que da ruim
# as vezes 2d-ad