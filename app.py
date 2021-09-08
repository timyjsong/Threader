from time import sleep, perf_counter
from argparse import ArgumentParser
from threading import Thread, Lock
from queue import Queue

print_lock = Lock()
list_lock = Lock()


def threader(total, func, jobs):
    """ total = total number of threads, 
        func = target function
        jobs = a matrix of arguments
    """

    que = Queue()  # CREATES A FIFO QUEUE

    for job in jobs:
        que.put(job)

    for _ in range(total):
        que.put(None)

    def slave():
        while True:
            # try:
            #     with list_lock:
            #         job = jobs.pop()
            # except IndexError:
            #     break
            # else:
            #     func(*job)
            data = que.get()
            if data is not None:
                func(*data)
                que.task_done()
            else:
                break

    threads = []
    for _ in range(args.threads):
        thread = Thread(target=slave, args=(), daemon=True)
        threads.append(thread)

    for thread in threads:
        thread.start()
        
    for thread in threads:
        thread.join()


def sleeper(delay, job_num):
    with print_lock:
        print(f"running {job_num}, sleeping {delay} seconds")
    sleep(delay)


def main(args):
    jobs = [(args.delay, job) for job in range(args.jobs)]

    s_time = perf_counter()
    threader(args.threads, sleeper, jobs)
    e_time = perf_counter()

    print(f"finished in {e_time-s_time} seconds")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-d", "--delay", metavar="delay",
        type=int, required=True,
        help="specify the number of seconds to sleep"
    )
    parser.add_argument(
        "-j", "--jobs", metavar="jobs",
        type=int, required=True,
        help="specify the number of jobs to run"
    )
    parser.add_argument(
        "-t", "--threads", metavar="threads",
        type=int, required=True,
        help="specify the number of threads to run"
    )
    args = parser.parse_args()
    main(args)
