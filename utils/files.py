import os

def get_latest_data_file(dir='../input'):
    import glob
    
    list_of_files = glob.glob(os.path.join(dir,'*.csv')) # * means all if need specific format then *.csv
    if not any(list_of_files):
        return None

    return max(list_of_files, key=os.path.getctime)


def get_result_filename(fullname, all_eps=True):
    if not all_eps:
        output_fname_tags ='(closed_eps)'
    else:
        output_fname_tags = '(with_open_eps)'
    
    base = os.path.basename(fullname)
    input_filename = os.path.splitext(base)[0]
    return os.path.join("output", f"./{input_filename}_{output_fname_tags}")
