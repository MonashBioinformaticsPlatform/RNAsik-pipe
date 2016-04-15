#
t_type=`sed -n '47p' $1 | grep -Po "transcript_type"`

if [ -z "$t_type" ]; then
  # this isn't ideal, but i think its going to work fine for now
  check_type=`sed -n '47p' $1 | grep -Po "(gene|transcript)_(bio)?type"`
  array=($check_type)
  check_case=""

  for item in ${array[@]}; do
    check_case=$item
    if [[ $type =~ "transcrip_biotype" ]]; then
      check_type=$item
      break
    fi
  done
  
  case $check_case in
    transcript_biotype)
      sed -i 's/transcript_biotype/transcript_type/' $1
      ;;
    gene_biotype)
      sed -i 's/gene_biotype/transcript_type/' $1
      ;;
    gene_type)
      sed -i 's/gene_type/transcript_type/' $1
      ;;
  esac
fi
