import subprocess


def main():
    p = subprocess.Popen(['wal-g --version'], shell=True, stdout=subprocess.PIPE)
    print(p.stdout.read().decode())


if __name__ == '__main__':
    main()
