export CORES=$(getconf _NPROCESSORS_ONLN)
echo "Found cores : $CORES"
WORKERCOUNT=1

CMD ( ) {
cd .
cat <<EOF > ipengine.json
{
  "ssh": "",
  "interface": "tcp://*",
  "registration": 51582,
  "control": 51584,
  "mux": 51586,
  "hb_ping": 51587,
  "hb_pong": 51588,
  "task": 51590,
  "iopub": 51592,
  "key": "2975b176-0907329b90b77ad3d255a7c3",
  "location": "sillygoose.local",
  "pack": "json",
  "unpack": "json",
  "signature_scheme": "hmac-sha256"
}
EOF

mkdir -p '.ipengine_logs'
ipengine --file=ipengine.json >> .ipengine_logs/$JOBNAME.log 2>&1

}

for COUNT in $(seq 1 1 $WORKERCOUNT)
do
    echo "Launching worker: $COUNT"
    CMD &
done
wait
echo "All workers done"
