
#sensor name to retrieve
#log file start and stop time to match to sensors you are retrieving
#to me it looks like kat_store is running on a SAST timezone
def sensor_data_pvsn(sensor, timestart, timestop):
    import requests 
    sensors_url = 'http://portal.mkat.karoo.kat.ac.za/katstore/api/query'

    sample_params = {'sensor':sensor, 
                     'start_time':timestart.strftime('%s'), 
                     'end_time': timestop.strftime('%s'),
                     'include_value_time': True}

    #Debug
    #print(sample_params)
    try:
        resp = requests.get(sensors_url, sample_params)
    except Exception as exc:
        print('Something failed: {}'.format(exc))
    if resp.status_code == 200:
        sample_results = resp.json()
        #Debug
        #print(resp.json())
        timestampv=[sample['value_time'] for sample in sample_results['data']]
        timestamps=[sample['sample_time'] for sample in sample_results['data']]
        samples=[sample['value'] for sample in sample_results['data']]
    else:
        print("Request returned with a status code {}".format(resp.status_code))
        print(resp)
    return(timestampv,timestamps,samples)
 
