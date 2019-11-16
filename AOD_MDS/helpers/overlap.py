

from AOD_MDS.constants import MDS, MDS_END_FLD, MDS_ST_FLD, MDS_Dates
from rule_checker.constants import MODE_LOOSE, NOW, NOW_ORD
from utils import get_datestring_from_ordinal


def prep_and_check_overlap(data_row, client_eps, errors, rec_idx, date_error_fields):
    if not ((MDS['COMM_DATE'] in date_error_fields) 
                              or (MDS['END_DATE'] in date_error_fields)):
        cid = data_row[MDS['ID']]
        ep_dates_obj = { MDS_ST_FLD: data_row[MDS_ST_FLD],
                            MDS['COMM_DATE']: data_row[MDS['COMM_DATE']], 
                            'idx': rec_idx }
        if MDS_END_FLD in data_row:
            ep_dates_obj[MDS_END_FLD] = data_row[MDS_END_FLD]
            ep_dates_obj[MDS['END_DATE']] = data_row[MDS['END_DATE']]

        else: #end date is blank, use current date  as end date to check overlap ?
            ep_dates_obj[MDS_END_FLD] = NOW_ORD
            ep_dates_obj[MDS['END_DATE']] = NOW

        if (cid in client_eps): # any(client_eps.get(cid, [])):
            client_eps[cid].append(ep_dates_obj)
            check_overlap(data_row, client_eps[cid], errors, rec_idx, 
                          st_fld=MDS_ST_FLD, end_fld=MDS_END_FLD)
        else:
            client_eps[cid] = [ep_dates_obj]


"""
  check if the current episode client_eps, overlaps with any previously seen 
  episode for this client.
"""
def check_overlap(current_ep, client_eps, errors, rec_idx,
                  st_fld=MDS["COMM_DATE"], end_fld=MDS["END_DATE"]):

    start_date = client_eps[-1] [st_fld]
    end_date = client_eps[-1][end_fld]

    for ep in client_eps[:-1]:
        if min(end_date, ep[end_fld]) >= max(start_date, ep[st_fld]):
            other_st = get_datestring_from_ordinal(ep[st_fld], dtformat="%d/%m/%Y")
            other_end = get_datestring_from_ordinal(ep[end_fld], dtformat="%d/%m/%Y")

            errors[rec_idx].append( { 'index': rec_idx,
                                    'cid': current_ep[MDS['ID']],
                                    'etype': 'logic',
                                    'field': MDS['END_DATE'],
                                    'message': \
                f"Overlaps with other episode Start: {other_st} End: {other_end}"
                                    })
            errors[ep['idx']].append( { 'index': ep['idx'],
                                    'cid': current_ep[MDS['ID']],
                                    'etype': 'logic',
                                    'field': MDS['END_DATE'],
                                    'message': \
                f"Overlaps with other episode Start: {ep[MDS['COMM_DATE']]} End: {ep[MDS['END_DATE']]}"
                                    })


