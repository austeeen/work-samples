
ROOTDIR="./"

SECRETS="secrets.txt"

if [[ $# -eq 1 ]]; then
    ROOTDIR=$ROODIR"$1"
fi

cat $SECRETS | while read line; do
    echo "-- $line -- "
    grep -winr "$line"  "$ROOTDIR" --exclude "secrets.txt" --exclude "secrets.log" --exclude ".git"
    echo "-//-"
done
