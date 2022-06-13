echo $(date) ": starting script"
now="$(date +"%Y_%m_%d_%H_%M_%S")"

Rx_root=/notebooks/Auto_Reports/Receiver

echo "$Rx_root/Monthly/rx_monthly_$now.ipynb"

echo $(date) ": copying template"
cp "$Rx_root/Monthly/rx_monthly_template.ipynb" "$Rx_root/Monthly/rx_monthly_$now.ipynb"

echo $(date) ": running jupyter"
/usr/local/bin/jupyter nbconvert --ExecutePreprocessor.timeout=10000 --to notebook --ExecutePreprocessor.allow_errors=True --inplace --execute "$Rx_root/Monthly/rx_monthly_$now.ipynb" >> $Rx_root/Monthly/notebook.log

echo $(date) ": ending script\n\n"


