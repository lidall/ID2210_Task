
import os, sys
from random import shuffle
import argparse
import json
from time import time


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--file',
                        required=False,
                        action='store',
                        default='/tmp/monkeytest',
                        help='The file to read/write to')
    parser.add_argument('-s', '--size',
                        required=False,
                        action='store',
                        type=int,
                        default=128,
                        help='Total MB to write')
    parser.add_argument('-w', '--write-block-size',
                        required=False,
                        action='store',
                        type=int,
                        default=1024,
                        help='The block size for writing in bytes')
    parser.add_argument('-r', '--read-block-size',
                        required=False,
                        action='store',
                        type=int,
                        default=512,
                        help='The block size for reading in bytes')
    parser.add_argument('-j', '--json',
                        required=False,
                        action='store',
                        help='Output to json file')
    args = parser.parse_args()
    return args


class Benchmark:

    def __init__(self, file,write_mb, write_block_kb, read_block_b):
        self.file = file
        self.write_mb = write_mb
        self.write_block_kb = write_block_kb
        self.read_block_b = read_block_b
        wr_blocks = int(self.write_mb * 1024 / self.write_block_kb)
        rd_blocks = int(self.write_mb * 1024 * 1024 / self.read_block_b)
        self.write_results = self.write_test( 1024 * self.write_block_kb, wr_blocks)
        self.read_results = self.read_test(self.read_block_b, rd_blocks)

    def write_test(self, block_size, blocks_count, show_progress=True):

        f = os.open(self.file, os.O_CREAT | os.O_WRONLY, 0o777)  # low-level I/O

        took = []
        for i in range(blocks_count):
            if show_progress:
                # dirty trick to actually print progress on each iteration
                sys.stdout.write('\rWriting: {:.2f} %'.format(
                    (i + 1) * 100 / blocks_count))
                sys.stdout.flush()
            buff = os.urandom(block_size)
            start = time()
            os.write(f, buff)
            os.fsync(f)  # force write to disk
            t = time() - start
            took.append(t)

        os.close(f)
        return took

    def read_test(self, block_size, blocks_count, show_progress=True):

        f = os.open(self.file, os.O_RDONLY, 0o777) 
        offsets = list(range(0, blocks_count * block_size, block_size))
        shuffle(offsets)

        took = []
        for i, offset in enumerate(offsets, 1):
            if show_progress and i % int(self.write_block_kb * 1024 / self.read_block_b) == 0:
                sys.stdout.write('\rReading: {:.2f} %'.format(
                    (i + 1) * 100 / blocks_count))
                sys.stdout.flush()
            start = time()
            os.lseek(f, offset, os.SEEK_SET)
            buff = os.read(f, block_size)
            t = time() - start
            if not buff: break
            took.append(t)

        os.close(f)
        return took

    def print_result(self):
        result = ('\n\nWritten {} MB in {:.4f} s\nWrite speed is  {:.2f} MB/s'
                  '\n  max: {max:.2f} MB/S, min: {min:.2f} MB/S \n'.format(
            self.write_mb, sum(self.write_results), self.write_mb / sum(self.write_results),
            max=self.write_block_kb / (1024 * min(self.write_results)),
            min=self.write_block_kb / (1024 * max(self.write_results))))
        result += ('\nRead {} x {} B blocks in {:.4f} s\nRead speed is  {:.2f} MB/s'
                   '\n  max: {max:.2f} MB/S, min: {min:.2f} MB/S\n'.format(
            len(self.read_results), self.read_block_b,
            sum(self.read_results), self.write_mb / sum(self.read_results),
            max=self.read_block_b / (1024 * 1024 * min(self.read_results)),
            min=self.read_block_b / (1024 * 1024 * max(self.read_results))))
        print(result)


    def get_json_result(self,output_file):
        results_json = {}
        results_json["Written MB"] = self.write_mb
        results_json["Write time (sec)"] = round(sum(self.write_results),2)
        results_json["Write speed in MB/s"] = round(self.write_mb / sum(self.write_results),2)
        results_json["Read blocks"] = len(self.read_results)
        results_json["Read time (sec)"] = round(sum(self.read_results),2)
        results_json["Read speed in MB/s"] = round(self.write_mb / sum(self.read_results),2)
        with open(output_file,'w') as f:
            json.dump(results_json,f)


def main():
    args = get_args()
    benchmark = Benchmark(args.file, args.size, args.write_block_size, args.read_block_size)
    if args.json is not None:
        benchmark.get_json_result(args.json)
    else:
        benchmark.print_result()
    os.remove(args.file)

if __name__ == "__main__":
    main()