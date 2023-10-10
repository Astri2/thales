if [ $# = 0 ]; then
    echo "missing arguments!"
    echo "Format: ./run [<samples_folder>] [<solution_file>] (<unit tests to run...>)"
    exit 1
fi
s="main.py -c -d $1 -f $2"
if [ $# -gt 2 ]; then
    s=$s" -t ${@:3:99}"
fi

# echo "=> python3 $s"
python3 $s