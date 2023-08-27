import os

def isfloat(var: str) -> bool:
    try:
        if var.isnumeric(): return False # Numero que tem ponto.

        nvar = float(var) # se não da erro, tem ponto.
        return True
    
    except:
        return False

def gen_data_from_raw(position=0):

    min_time  = 1e10
    min_param = ['','','']

    target_dir = "results"

    r_data_arq = os.listdir(f"./{target_dir}")

    storages = ['db-file', 'db', 'file']

    hashes = ['md5', 'murmur', 'xxhash']

    memories = ['2d-ad-t', '1d-ow', '1d-ad', '2d-ad', 'ad', '2d-ad-f', '2d-ad-ft', '2d-lz']

    f_data = {}

    for storage in storages:
        f_data[storage] = {}
        for hash in hashes:
            f_data[storage][hash] = {}
            for memo in memories:
                f_data[storage][hash][memo] = 0.

    f_data["no-cache"] = {}
    f_data["no-cache"]["no-cache"] = {}
    f_data["no-cache"]["no-cache"]["no-cache"] = 0.

    for r_data in r_data_arq:
        if '.png' in r_data:
            continue
        
        try:
            storage, hash, memo = r_data.split('#')
        except ValueError: # Too many values to unpack.
            storage, hash, memo = "no-cache", "no-cache", "no-cache"

        with open(f"{target_dir}/{r_data}") as f:
            lines = f.read().splitlines()
            n = 0 # non-time lines OR first time line index
            p = 0 # total
        
            while True:
                if not isfloat(lines[n]):
                    n += 1
                else:
                    break

            while True:
                if isfloat(lines[n+1+p]):
                    p += 1
                else:
                    break

            n, p = n, (n+1) + p

            one_data = sorted(lines[n+position::p])
            # Se for do interesse do senhor, podemos printar max, min stand dev, mean, median
            
            #print(storage, hash, memo, one_data)

            f_data[storage][hash][memo] = float(one_data[int(len(one_data)/2)])
            
            if f_data[storage][hash][memo] < min_time:
                min_time  = f_data[storage][hash][memo]
                min_param = [storage,hash,memo,min_time]

    return f_data, min_param