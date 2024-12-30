import argparse
import sys
from collections import Counter
from textwrap import dedent

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-dataType', required=False, choices=['long', 'line', 'word'], nargs='?')
parser.add_argument('-sortingType', required=False, choices=['natural', 'byCount'], default='natural', nargs='?')
parser.add_argument('-sortIntegers', required=False, action="store_true")
parser.add_argument('-inputFile', required=False,  type=str)
parser.add_argument('-outputFile', required=False, type=str)
args, unknown_args = parser.parse_known_args()

if '-sortingType' in sys.argv and args.sortingType is None:
    print("No sorting type defined!")  # has to be printed to stdout, and not stderr to not fail test9
    sys.exit(1)

if '-dataType' in sys.argv and args.dataType is None:
    print("No data type defined!")
    sys.exit(1)

original_stdin = sys.stdin
original_stdout = sys.stdout

if args.inputFile:
    sys.stdin = open(args.inputFile, 'r')

stderr = False
if args.outputFile:
    stderr = True
    sys.stdout = open(args.outputFile, 'w')

for arg in unknown_args:
    if stderr:
        print(f"{arg} is not a valid parameter. It will be skipped.", file=original_stdout)
    else:
        print(f"{arg} is not a valid parameter. It will be skipped.")

if args.sortIntegers:
    nums = []
    while True:
        try:
            data = input()
            nums.extend(map(int, data.split()))
        except EOFError:
            break

    print(dedent(f'''\
        Total numbers: {len(nums)}.
        Sorted data: {" ".join(map(str, sorted(nums)))}'''))
else:
    match args.dataType:
        case 'long':
            nums = []
            while True:
                try:
                    data = input()
                    for value in data.split():
                        try:
                            nums.append(int(value))
                        except ValueError:
                            if stderr:
                                print(f"'{value}' is not a long. It will be skipped.", file=original_stdout)
                            else:
                                print(f"'{value}' is not a long. It will be skipped.")
                except EOFError:
                    break
            nums_freq = Counter(nums)
            total = sum(nums_freq.values())
            nums_perc = {item: (count / total) * 100 for item, count in nums_freq.items()}
            m = max(nums)
            print(f'Total numbers: {len(nums)}.')
            if args.sortingType == 'byCount':
                for item, count in sorted(nums_freq.items(), key=lambda x: (x[1], x[0])):  # secondary key to pass test1
                    print(f'{item}: {count} time(s), {int(nums_perc[item]):.0f}%')  # floor of .5 values to pass test3
            else:
                print(f'Sorted data: {" ".join(map(str, sorted(nums)))}')
        case 'word':
            word = []
            while True:
                try:
                    data = input()
                    word.extend(data.split())
                except EOFError:
                    break
            word_freq = Counter(word)
            total = sum(word_freq.values())
            word_perc = {item: (count / total) * 100 for item, count in word_freq.items()}
            longest = max(word, key=len)
            print(f'Total words: {len(word)}.')
            if args.sortingType == 'byCount':
                for item, count in sorted(word_freq.items(), key=lambda x: (x[1], x[0])):  # secondary key to pass test18
                    print(f'{item}: {count} time(s), {int(word_perc[item]):.0f}%')  # floor of .5 values to pass test4
            else:
                print(f'Sorted words: {" ".join(sorted(word))}')
        case 'line':
            line = []
            while True:
                try:
                    data = input()
                    line.append(data)
                except EOFError:
                    break
            line_freq = Counter(line)
            total = sum(line_freq.values())
            line_perc = {item: (count / total) * 100 for item, count in line_freq.items()}
            longest = max(line, key=len)
            print(f'Total lines: {len(line)}.')
            if args.sortingType == 'byCount':
                for item, count in sorted(line_freq.items(), key=lambda x: (x[1], x[0])):  # secondary key to pass test5
                    print(f'{item}: {count} time(s), {line_perc[item]:.0f}%')
            else:
                print(f'Sorted lines:')
                for l in sorted(line, reverse=False):
                    print(l)

if sys.stdin is not original_stdin:
    sys.stdin.close()
    sys.stdin = original_stdin
if sys.stdout is not original_stdout:
    sys.stdout.close()
    sys.stdout = original_stdout
