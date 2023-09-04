#!/bin/bash

filename="$1"
shift

target_dir="results"

str_args=""

times=5

for arg in "$@"; do
    str_args+=" $arg"
done

check_target_dir() {
    if [ ! -d "$1" ]; then
        return 1
    else
        return 0
    fi
}

create_target_dir() {
    if [ ! -d "$1" ]; then
        mkdir "$1"
        return $?
    else
        return 1
    fi
}

remove_target_dir() {
    if [ -d "$1" ]; then
        rm -rf "$1"
        return $?
    else
        return 1
    fi
}

create_info_data() {
    storage="$1"
    hash="$2"
    memo="$3"
    if [ "$memo" = "--no-cache" ]; then
        python3 "./$filename" $str_args --no-cache >> "$target_dir/no-cache"
        echo "Done --no-cache"
    else
        beg="python3 ./$filename"
        end=" -m $memo -H $hash -s $storage >> $target_dir/$storage#$hash#$memo"
        eval "$beg$str_args$end"
        echo "Done $storage $hash $memo"
    fi
}

memories=('2d-ad-t' '1d-ow' '1d-ad' '2d-ad' 'ad' '2d-ad-f' '2d-ad-ft' '2d-lz')
hashes=('md5' 'murmur' 'xxhash')
storages=('db-file' 'db' 'file')

main() {
    remove_target_dir "$target_dir"

    if ! create_target_dir "$target_dir"; then
        echo "Erro ao adicionar diretorio"
        exit 1
    fi

    if ! check_target_dir "$target_dir"; then
        echo "Diretorio nao foi achado..."
        exit 1
    fi

    for storage in "${storages[@]}"; do
        for hash in "${hashes[@]}"; do
            for memo in "${memories[@]}"; do
                for ((i=0; i<$times; i++)); do
                    create_info_data "$storage" "$hash" "$memo"
                done
            done
        done
        remove_target_dir "./.intpy"
    done

    for ((i=0; i<$times; i++)); do
        create_info_data "" "" "--no-cache"
    done
}

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <filename> [args...]"
    exit 1
fi

main
