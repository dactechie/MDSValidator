
from MDSValidator.AOD_MDS.constants import MDS
from MDSValidator.utils import v_er_date_lam


# Note: this modifies the original data_row (not a pure function)
def fix_check_dates(data_row, rec_idx, fn_date_converter,
                    id_field, date_fields) -> list:
    k = None
    date_conversion_errors = []
    
    for d in date_fields:
        k = MDS[d]
        dt = data_row[k]
        if not dt: #and not expect_all: # end date might be blank, nothing to convert : 
                                      # FIXME: above is not true, might have overlapping open episodes
            continue
        l = len(dt)
        # if l < 7:
        #     logger.warn(f"Warning : invalid date string {dt}. Not converting to Date.")
        #     continue
        if l == 7 or dt.find('/') == 1 : #no leading zero in the case of 1_01_1981 or 1/01/1981
            dt = '0' + dt
            data_row[k] = dt
        try:
            data_row['O'+k] = fn_date_converter(dt)
        except ValueError :#as e:
            date_conversion_errors.append(v_er_date_lam(rec_idx, data_row[id_field], k, dt))

    return date_conversion_errors

