#!/bin/bash

RIR=""
input_folder=""
version=""
destination=""

print_help() {
    echo "Usage: $(basename "$0") [options]"
    echo "Info: This script setting up bgpdump options to be used to generate the base.out contant or updates.out content,"
    echo "further used in a SandRouter tool in simulations. This script provides the selection of RIR (see more info of option -i)."
    echo "The script provides the option to select the version of IP protocol to be filtered (see more info of option -v)."
    echo "If the selected version is IPv6, the pattern option is ignored."
    echo "......................................................................................................................."
    echo "Options:"
    echo "  -h               Show this help message and exit"
    echo "  -i [choice]      Regional Internet Registry, choices:[LACNIC, APNIC, ARIN, AFRINIC, RIPE_NCC]."
    echo "                   Info: With no choice of registry selected, all RIRs are comprised."
    echo "  -f [file]        The input folder, containing one bview.(bz2) of rib.(gz) file and one and more updates files."
    echo "  -d [file]        The destination folder, where generated files will be placed."
    echo "  -v [choice]      Selection of the verion of IP protocol, choices:[v4, v6], where 'v4' stands for IPv4 and 'v6' stands for IPv6"
}

while getopts "hi:f:v:d:bu" opt; do
  case ${opt} in
    f )
      input_folder="$OPTARG"
      ;;
    i )
      RIR="$OPTARG"
      ;;
    v )
      version="$OPTARG"
      ;;
    d )
      destination="$OPTARG"
      ;;
    h )
      print_help
      exit 0
      ;;
    \? )
      echo "Invalid option: -$OPTARG" 1>&2
      exit 1
      ;;
    : )
      echo "Option -$OPTARG needs an argument." 1>&2
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

if [ ! -d "$input_folder" ]; then
    echo "Error: Provided file '$input_file' does not exists." >&2
    exit 1
fi

#Select the regex pattern based on the selected RIR
pattern_updates=""
pattern_base=""

if [ "$RIR" == "LACNIC" ]; then
    if [ "$base_flag" == true ]; then
        pattern_base="^0.0.0.0/0\|^177.\|^179.\|^181.\|^186.\|^187.\|^189.\|^190.\|^200.\|^201.\|^191."
    fi

    if [ "$update_flag" == true ]; then
        pattern=" 177\.\| 179\.\| 181\.\| 186\.\| 187\.\| 189\.\| 190\.\| 200\.\| 201\.\| 191\."
    fi
fi

if [ "$RIR" == "AFRINIC" ]; then
    if [ "$base_flag" == true ]; then
        pattern_base="^0.0.0.0/0\|^41.\|^102.\|^105.\|^197.\|^154.\|^196."
    fi

    if [ "$update_flag" == true ]; then
        pattern=" 41\.\| 102\.\| 105\.\| 197\.\| 154\.\| 196\."
    fi
fi

if [ "$RIR" == "RIPE_NCC" ]; then
    if [ "$base_flag" == true ]; then
        pattern_base="^0.0.0.0/0\|^2.\|^5.\|^31.\|^37.\|^46.\|^62.\|^77.\|^78.\|^79.\|^80.\|^81.\|^82.\|^83.\|^84.\|^85.\|^86.\|^87.\|^88.\|^89.\|^90.\|^91.\|^92.\|^93.\|^94.\|^95.\|^109.\|^176.\|^178.\|^185.\|^193.\|^194.\|^195.\|^212.\|^213.\|^217.\|^25.\|^51.\|^57.\|^141.\|^145.\|^151.\|^188."
    fi

    if [ "$update_flag" == true ]; then
        pattern=" 2\.\| 5\.\| 31\.\| 37\.\| 46\.\| 62\.\| 77\.\| 78\.\| 79\.\| 80\.\| 81\.\| 82\.\| 83\.\| 84\.\| 85\.\| 86\.\| 87\.\| 88\.\| 89\.\| 90\.\| 91\.\| 92\.\| 93\.\| 94\.\| 95\.\| 109\.\| 176\.\| 178\.\| 185\.\| 193\.\| 194\.\| 195\.\| 212\.\| 213\.\| 217\.\| 25\.\| 51\.\| 57\.\| 141\.\| 145\.\| 151\.\| 188\."
    fi
fi

if [ "$RIR" == "APNIC" ]; then
    if [ "$base_flag" == true ]; then
        pattern_base="^0.0.0.0/0\|^1\.\|^14\.\|^27\.\|^36\.\|^39\.\|^42\.\|^49\.\|^58\.\|^59\.\|^60\.\|^61\.\|^101\.\|^103\.\|^106\.\|^110\.\|^111\.\|^112\.\|^113\.\|^114\.\|^115\.\|^116\.\|^117\.\|^118\.\|^119\.\|^120\.\|^121\.\|^122\.\|^123\.\|^124\.\|^125\.\|^126\.\|^175\.\|^180\.\|^182\.\|^183\.\|^202\.\|^203\.\|^210\.\|^211\.\|^218\.\|^219\.\|^220\.\|^221\.\|^222\.\|^223\.\|^43\.\|^133\.\|^150\.\|^153\.\|^163\.\|^171\."
    fi

    if [ "$update_flag" == true ]; then
        pattern=" 1\.\| 14\.\| 27\.\| 36\.\| 39\.\| 42\.\| 49\.\| 58\.\| 59\.\| 60\.\| 61\.\| 101\.\| 103\.\| 106\.\| 110\.\| 111\.\| 112\.\| 113\.\| 114\.\| 115\.\| 116\.\| 117\.\| 118\.\| 119\.\| 120\.\| 121\.\| 122\.\| 123\.\| 124\.\| 125\.\| 126\.\| 175\.\| 180\.\| 182\.\| 183\.\| 202\.\| 203\.\| 210\.\| 211\.\| 218\.\| 219\.\| 220\.\| 221\.\| 222\.\| 223\.\| 43\.\| 133\.\| 150\.\| 153\.\| 163\.\| 171\."
    fi
fi

if [ "$RIR" == "ARIN" ]; then
    if [ "$base_flag" == true ]; then
        pattern_base="^0.0.0.0/0\|^23\.\|^24\.\|^50\.\|^63\.\|^64\.\|^65\.\|^66\.\|^67\.\|^68\.\|^69\.\|^70\.\|^71\.\|^72\.\|^73\.\|^74\.\|^75\.\|^76\.\|^96\.\|^97\.\|^98\.\|^99\.\|^100\.\|^104\.\|^107\.\|^108\.\|^173\.\|^174\.\|^184\.\|^199\.\|^204\.\|^205\.\|^206\.\|^207\.\|^208\.\|^209\.\|^216\.\|^3\.\|^4\.\|^7\.\|^8\.\|^9\.\|^13\.\|^15\.\|^16\.\|^18\.\|^20\.\|^32\.\|^34\.\|^35\.\|^40\.\|^44\.\|^45\.\|^47\.\|^48\.\|^52\.\|^54\.\|^56\.\|^128\.\|^129\.\|^130\.\|^131\.\|^132\.\|^134\.\|^135\.\|^136\.\|^137\.\|^138\.\|^139\.\|^140\.\|^142\.\|^143\.\|^144\.\|^146\.\|^147\.\|^148\.\|^149\.\|^152\.\|^155\.\|^156\.\|^157\.\|^158\.\|^159\.\|^160\.\|^161\.\|^162\.\|^164\.\|^165\.\|^166\.\|^167\.\|^168\.\|^169\.\|^170\.\|^172\.\|^192\.\|^198\.\|^17\.\|^6\.\|^12\.\|^21\.\|^22\.\|^26\.\|^29\.\|^30\.\|^33\.\|^11\.\|^55\.\|^28\.\|^19\.\|^38\.\|^214\.\|^215\."
    fi

    if [ "$update_flag" == true ]; then
        pattern=" 23\.\| 24\.\| 50\.\| 63\.\| 64\.\| 65\.\| 66\.\| 67\.\| 68\.\| 69\.\| 70\.\| 71\.\| 72\.\| 73\.\| 74\.\| 75\.\| 76\.\| 96\.\| 97\.\| 98\.\| 99\.\| 100\.\| 104\.\| 107\.\| 108\.\| 173\.\| 174\.\| 184\.\| 199\.\| 204\.\| 205\.\| 206\.\| 207\.\| 208\.\| 209\.\| 216\.\| 3\.\| 4\.\| 7\.\| 8\.\| 9\.\| 13\.\| 15\.\| 16\.\| 18\.\| 20\.\| 32\.\| 34\.\| 35\.\| 40\.\| 44\.\| 45\.\| 47\.\| 48\.\| 52\.\| 54\.\| 56\.\| 128\.\| 129\.\| 130\.\| 131\.\| 132\.\| 134\.\| 135\.\| 136\.\| 137\.\| 138\.\| 139\.\| 140\.\| 142\.\| 143\.\| 144\.\| 146\.\| 147\.\| 148\.\| 149\.\| 152\.\| 155\.\| 156\.\| 157\.\| 158\.\| 159\.\| 160\.\| 161\.\| 162\.\| 164\.\| 165\.\| 166\.\| 167\.\| 168\.\| 169\.\| 170\.\| 172\.\| 192\.\| 198\.\| 17\.\| 6\.\| 12\.\| 21\.\| 22\.\| 26\.\| 29\.\| 30\.\| 33\.\| 11\.\| 55\.\| 28\.\| 19\.\| 38\.\| 214\.\| 215\."
    fi
fi

base_file=""
updates_file=""

if ls ${input_folder}/bview* 1> /dev/null 2>&1; then
    base_file=${input_folder}/bview.*
elif ls ${input_folder}/rib* 1> /dev/null 2>&1; then
    base_file=${input_folder}/rib.*
fi

if test -f "$destination/updates.txt"; then
  rm "$destination/updates.txt"
fi

touch "$destination/updates.txt"

if test -f "$destination/base.txt"; then
  rm "$destination/base.txt"
fi

touch "$destination/base.txt"

if [ "$version" == "v4" ]; then
    eval 'bgpdump $base_file | grep PREFIX | python3 ./scripts/address_parser.py -b -v4 | grep $pattern_base | sort | uniq >> $destination/base.txt'

    for filename in ${input_folder}/updates.*; do
        eval 'bgpdump -M $filename | python3 ./scripts/address_parser.py -u -v4 | grep $pattern >> $destination/updates.txt'
    done
fi

if [ "$version" == "v6" ]; then
    eval 'bgpdump $base_file | grep PREFIX | python3 ./scripts/address_parser.py -b -v6 | sort | uniq > $destination/base.txt'

    for filename in ${input_folder}/updates.*; do
        eval 'bgpdump -M $filename | python3 ./scripts/address_parser.py -u -v6 >> $destination/updates.txt'
    done
fi