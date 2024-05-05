#!/bin/bash

input_folder=""
collector=""
verion=""

while getopts "f:c:v:" opt; do
  case ${opt} in
    f )
      input_folder="$OPTARG"
      ;;
    c )
      collector="$OPTARG"
      ;;
    v )
      verion="$OPTARG"
      ;;
    \? )
      echo "Neplatný přepínač: -$OPTARG" 1>&2
      exit 1
      ;;
    : )
      echo "Přepínač -$OPTARG vyžaduje argument." 1>&2
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

echo "SandRouter simulations, concentrated on LACNIC registry:"
python3 SandRouter.py -m 0 -b "${input_file}/LACNIC_base.txt" -u "${input_file}/LACNIC_updates.txt" -d "../BT/LACNIC/${collector}"
python3 SandRouter.py -m 1 -b "${input_file}/LACNIC_base.txt" -u "${input_file}/LACNIC_updates.txt" -d "../TBM/LACNIC/${collector}"

echo "SandRouter simulations, concentrated on ARIN registry:"
python3 SandRouter.py -m 0 -b "${input_file}/ARIN_base.txt" -u "${input_file}/ARIN_updates.txt" -d "../BT/ARIN/${collector}"
python3 SandRouter.py -m 1 -b "${input_file}/ARIN_base.txt" -u "${input_file}/ARIN_updates.txt" -d "../TBM/ARIN/${collector}"

echo "SandRouter simulations, concentrated on AFRINIC registry:"
python3 SandRouter.py -m 0 -b "${input_file}/AFRINIC_base.txt" -u "${input_file}/AFRINIC_updates.txt" -d "../BT/AFRINIC/${collector}"
python3 SandRouter.py -m 1 -b "${input_file}/AFRINIC_base.txt" -u "${input_file}/AFRINIC_updates.txt" -d "../TBM/AFRINIC/${collector}"

echo "SandRouter simulations, concentrated on APNIC registry:"
python3 SandRouter.py -m 0 -b "${input_file}/APNIC_base.txt" -u "${input_file}/APNIC_updates.txt" -d "../BT/APNIC/${collector}"
python3 SandRouter.py -m 1 -b "${input_file}/APNIC_base.txt" -u "${input_file}/APNIC_updates.txt" -d "../TBM/APNIC/${collector}"

echo "SandRouter simulations, concentrated on RIPE_NCC registry:"
python3 SandRouter.py -m 0 -b "${input_file}/RIPE_NCC_base.txt" -u "${input_file}/RIPE_NCC_updates.txt" -d "../BT/RIPE_NCC/${collector}"
python3 SandRouter.py -m 1 -b "${input_file}/RIPE_NCC_base.txt" -u "${input_file}/RIPE_NCC_updates.txt" -d "../TBM/RIPE_NCC/${collector}"

echo "End"