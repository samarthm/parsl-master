export CORES=$(getconf _NPROCESSORS_ONLN)
echo "Found cores : $CORES"
WORKERCOUNT=1

CMD ( ) {
cd .
cat <<EOF > ipengine.json
{
  "ssh": "",
  "interface": "tcp://*",
  "registration": 52843,
  "control": 52845,
  "mux": 52847,
  "hb_ping": 52848,
  "hb_pong": 52849,
  "task": 52851,
  "iopub": 52853,
  "key": "796205ae-2e9586d917446a5419e56d14",
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
