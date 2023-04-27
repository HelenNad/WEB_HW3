from datetime import datetime
from multiprocessing import Pool, cpu_count
def factorize(*number):
    for num in number:
        dil = []
        i = 1
        while i <= num:
            if num % i == 0:
                dil.append(i)
            i += 1
        print(dil)


if __name__ == "__main__":

    start = datetime.now().timestamp()
    print(f"Count CPU: {cpu_count()}")
    with Pool(cpu_count()) as p:
        p.map_async(factorize, [128, 255, 99999, 10651060], )
        p.close()
        p.join()

    end = datetime.now().timestamp()
    result = end - start
    print(result)
