#!/bin/bash
APPDIR=$PWD
VENVDIR=$APPDIR/venv

# Tidy up local files and database
[ ! -f public_names.db ] || mv public_names.db public_names.db.old
[ ! -f final_merged.txt ] || mv final_merged.txt final_merged.txt.old
rm -f save_pid.txt
rm -f nohup.out

# Re-download the latest tsv files so we can rebuild the database
curl -s https://gitlab.com/wtsi-grit/darwin-tree-of-life-sample-naming/-/raw/master/final_merged.txt -o final_merged.txt
curl -s https://gitlab.com/wtsi-grit/darwin-tree-of-life-sample-naming/-/raw/master/unique_ids_assigned.txt -o unique_ids_assigned.txt

# activate Python virtual environment
source $VENVDIR/bin/activate

# start pyton server
nohup python3 -m swagger_server &
echo $! > save_pid.txt

# Rebuild the database
sleep 5  # Wait for the server to start, could change to use "wait"
curl -X POST "http://localhost:8080/verify-database" -H  "accept: */*" -d ""  # Rebuild
echo "Server running. To stop the Python server use 'kill -9 `cat save_pid.txt`'"
echo "Testing the local database by searching for Homo sapiens, taxid 9606"
curl -X GET "http://localhost:8080/public-name?taxonomyId=6344&specimenId=SAN0000100" -H  "accept: application/json"
