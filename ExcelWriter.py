from math import ceil
import xlwings as xw
from utils import now_string


def get_row(header, hlen, row_dict, errors):
    row = []

    errfield_mesg = {er['field']: er['message'] for er in errors }
    
    for i in range(0,hlen-1,2):
        error = ""
        header_field = header[i]   
        if header_field in errfield_mesg:
            error = errfield_mesg[header_field]
        if header_field in row_dict:
            row.extend([row_dict[header_field], error])
        else:
            row.extend(["",error])

    return row


def get_rows_to_write(headers, hlen, data, errors_dict):    
    return [get_row(headers, hlen, row_dict, errors_dict.get(i,[])) for i, row_dict in enumerate(data) if errors_dict.get(i)]


def _process_chunks(ws, data_rows, starter, ender, chunk_size=10):

    line_num = starter
    for line_num in range(starter, ender-chunk_size+1, chunk_size):
                            #2- > 682  +200 =  882
        st_row_num = line_num + 2
        ed_row_num = st_row_num + chunk_size
        ws.range(f'A{str(st_row_num)}:A{str(ed_row_num)}').value = \
                    data_rows[line_num:line_num+chunk_size]  # 0:5  -> 0,1,2,3,4
        print(f"end row number : {ed_row_num} " )
    
    starter = line_num+chunk_size
    chunk_size = ceil(0.2 * (ender - starter))
    if chunk_size < 1 : #or ((starter+chunk_size) > (ender - starter)):
        return
    print(f"calling process chunks agagin start {starter }  chunksize {chunk_size}  ")
    _process_chunks(ws, data_rows, starter, ender, chunk_size)
    

def write_data_to_book(data, errors, book_name):

    try:
        app = xw.App(visible=False)
        book = app.books.open("./MDSTemplate.xltx")
        ws = book.sheets[0]
        headers = ws.range('A1:BT1').value
      
        rows = get_rows_to_write(headers,  len(headers),  data, errors)

        endval = len(rows)
        chunk_size = ceil(0.2 * endval) # chunksize 20% 
        print ( f"\t >>> endval {endval}  chunksize {chunk_size} <<< \n")
        _process_chunks(ws, rows, starter=0, ender=endval, chunk_size=chunk_size) #800)

        book.save(f"{book_name}_{now_string()}.xlsx")
    #except Exception as e:
    #    print(e)
    finally:
        book.close()
        app.quit()
        print(" app pid : " , app.pid)
        app.kill()

    


if __name__ == '__main__':

    from test_data import setup_test_data, test_errors
    
    data = setup_test_data('./data copy.csv')
    #print(data)
    errors = test_errors()

    write_data_to_book(data['episodes'] , errors,'./two')
    

    
