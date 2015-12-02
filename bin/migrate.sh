SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
python $SCRIPTPATH/../manage.py makemigrations $1
python $SCRIPTPATH/../manage.py migrate