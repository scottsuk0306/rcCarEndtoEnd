#! /usr/bin/env python

from curtsies import Input

def main():
    with Input(keynames='curses') as input_generator:
        for e in input_generator:
            if e=='w': print("go front")
            if e=='s': print("go back")
            print()

if __name__ == '__main__':
    main()