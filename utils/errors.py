import copy
from MDSValidator.rule_checker.field_lists import (involved_field_sets,
                                      rd_with_involved_fields,
                                      rd_wo_involved_fields)

v_er_date_lam = lambda rec_idx, cid, date_field , err_val: {"index":rec_idx,
                                    "cid":cid,
                                    "etype":"date-format",
                                    "field":date_field,
                                    "message":f"Invalid date format {err_val}"}

v_er_lam = lambda rule_i, rules, rec_idx, cid: { "index": rec_idx,
                                    "cid":cid,
                                    "etype":"logic",
                                    "field":rules[rule_i]['field'],
                                    "message":rules[rule_i]['message']}

v_warn_lam = lambda rec_idx, cid, required, got: {
                    "index": rec_idx, "cid":cid, "required": required, "got": got
                    }


def add_error_to_list(error_obj, errors):
    ve_idx = error_obj['index']
    if ve_idx in errors:
        errors[ve_idx].append(error_obj)
    else:
        errors[ve_idx] = [error_obj]


def add_error_obj(errors, e, dataObj, id_field):
    path = e.path
    row = path[1]
    error_obj = {"index": row, "cid": dataObj['episodes'][row][id_field],
                               "etype": e.validator}
    
    if len(path) > 2:
        error_obj["field"]   = path[2]
        error_obj["message"] = f"invalid value/format: '{e.instance}'"
    else:
        error_obj["field"]= '<>'
        if len(e.message) > 50:   # oneOf fields are missing . Not checked as part of header checks
          if len(e.validator_value) > 0 and 'required' in e.validator_value[0]:
            st = e.validator_value[0]['required']        
            error_obj["message"]= f"Missing fields {st}.  row: {error_obj['index']} cid: {error_obj['cid']}"
            add_error_to_list(error_obj, errors)
            return -1
        else:
          error_obj["message"]= e.message

    add_error_to_list(error_obj, errors)
    return 0


def remove_vrules(error_fields):
    """
        Validation for fields that we already know have errors is pointless.
        Can't (check logic) i.e. do date comparisons, when the dates are not even well-formatted.
        So we remove rules that have dependencies on (involved with) those fields. 
        For now this just means dates.
    """
    error_field_set = set(error_fields)
    new_rd = copy.deepcopy(rd_wo_involved_fields)

    rule_defs_wo_errors = [rd_with_involved_fields[i]
                        for i, inv_fld_set in enumerate(involved_field_sets)
                        if error_field_set.isdisjoint(inv_fld_set)]

    new_rd.extend(rule_defs_wo_errors)

    return new_rd


def compile_errors(schema_validation_verrors, logic_errors):
    errors = []
    if logic_errors:
        logic_errors = (l for l in logic_errors if l)
        errors =  (item for sublist in logic_errors for item in sublist)
        
    if schema_validation_verrors:
        errors.extend(schema_validation_verrors)

    return errors


def _check_row_errors(array_of_dicts, suggestions, slk_field):
    """
    Note: there could be two rows with same client id, but one of them may have accurate SLK.
    This will added the error to both rows.
    """
    for d in array_of_dicts:
        if d['cid'] in suggestions and d['field'] == slk_field:
            d['message'] = suggestions[d['cid']]
            return


def compile_logic_errors(result, rule_defs, data_row, rec_idx, id_field, date_conversion_errors):
    # false values means that rule was violated. So we only want the indices of falses :

    idxes = (i for i, r in enumerate(result) if not r)
    
    rule_errors = [v_er_lam(rule_i, rule_defs, rec_idx, data_row[id_field]) for rule_i in idxes]
    if rule_errors: 
        if date_conversion_errors:
            rule_errors.extend(date_conversion_errors)
        return rule_errors

    return date_conversion_errors
