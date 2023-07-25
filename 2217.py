#!/usr/bin/env python
import math
import os
import sys
from bisect import bisect_left, bisect_right
from io import BytesIO, IOBase


def solve():
    """Write code here"""
    N, M = map(int, input().split())
    output = []
    count = 1
    nums = list(map(int, input().split()))
    mapper = {}
    for i, num in enumerate(nums):
        mapper[num] = i
    for i in range(2, N + 1):
        if mapper[i] < mapper[i - 1]:
            count += 1

    for _ in range(M):
        pos_a, pos_b = map(int, input().split())
        ab = [nums[pos_a - 1], nums[pos_b - 1]]
        seen = set()
        for num in ab:
            if num != 1 and mapper[num] < mapper[num - 1] and num not in seen:
                count -= 1
                seen.add(num)
            if num != N and mapper[num + 1] < mapper[num] and num + 1 not in seen:
                count -= 1
                seen.add(num + 1)

        mapper[nums[pos_a - 1]] = pos_b - 1
        mapper[nums[pos_b - 1]] = pos_a - 1
        nums[pos_a - 1], nums[pos_b - 1] = nums[pos_b - 1], nums[pos_a - 1]
        seen = set()
        for num in ab:
            if num != 1 and mapper[num] < mapper[num - 1] and num not in seen:
                count += 1
                seen.add(num)
            if num != N and mapper[num + 1] < mapper[num] and num + 1 not in seen:
                count += 1
                seen.add(num + 1)

        output.append(count)

    return output


def main():
    output = solve()
    if isinstance(output, bool):
        if output:
            print("YES")
        else:
            print("NO")
    elif isinstance(output, list):
        print(" ".join([str(num) for num in output]))
    else:
        print(output)


# region fastio

BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._file = file
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

# endregion

if __name__ == "__main__":
    main()

