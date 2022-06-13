echo $(date) ": starting script"
now="$(date +"%Y_%m_%d_%H_%M_%S")"

Rx_root=/notebooks/Auto_Reports/Receiver

echo "$Rx_root/Daily/rx_daily_$now.ipynb"

echo $(date) ": copying template"
cp "$Rx_root/Daily/rx_daily_template.ipynb" "$Rx_root/Daily/rx_daily_$now.ipynb"

echo $(date) ": running jupyter"
/usr/local/bin/jupyter nbconvert --ExecutePreprocessor.timeout=6000 --to notebook --ExecutePreprocessor.allow_errors=True --inplace --execute "$Rx_root/Daily/rx_daily_$now.ipynb" >> $Rx_root/Daily/notebook.log

echo $(date) ": ending script\n\n"

