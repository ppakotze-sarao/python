echo $(date) ": starting script"
now="$(date +"%Y_%m_%d_%H_%M_%S")"
year="$(date +"%Y")"
month="$(date +"%B")"

Rx_root=/notebooks/Auto_Reports/Receiver

mkdir -p "$Rx_root/Weekly/$year/$month"

notebook="$Rx_root/Weekly/$year/$month/rxs_weekly_$now.ipynb"

echo "$notebook"

echo $(date) ": copying template"
cp "$Rx_root/Weekly/RXS_Weekly_Check.ipynb" $notebook

echo $(date) ": running jupyter"
/usr/local/bin/jupyter nbconvert --ExecutePreprocessor.timeout=6000 --to notebook --ExecutePreprocessor.allow_errors=True --inplace --execute $notebook >> $Rx_root/Weekly/notebook.log

/usr/local/bin/jupyter nbconvert --to pdf $notebook >> $Rx_root/Weekly/notebook.log

echo $(date) ": ending script\n\n"

