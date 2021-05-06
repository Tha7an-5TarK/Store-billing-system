from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
import sqlite3 as db


def connection():
    connectObj = db.connect("shopManagement.db")
    cur = connectObj.cursor()
    sql = '''
    create table if not exists sellings (
        date string,
        product string,
        price number,
        quantity number,
        total number
        )
    '''
    cur.execute(sql)
    connectObj.commit()


connection()
window = Tk()
window.title("STSM Shop Manager")
tabs = ttk.Notebook(window)
root = ttk.Frame(tabs)
root2 = ttk.Frame(tabs)

tabs.add(root, text='Sell')
tabs.add(root2, text='Stock')
tabs.pack(expand=1, fill="both")


# ----------------------------------------------tab1 ----------------------------------

def GenerateBill():
    choice = messagebox.askyesno('Continue?', 'This bill can\'t be modified if you press yes')
    if not choice:
        return
    if len(curr_items) == 0:
        messagebox.showerror('No item', 'No item purchased')
        return

    connectObj = db.connect("shopManagement.db")
    cur = connectObj.cursor()

    global billarea

    billarea.delete('1.0', END)
    billarea.insert(END, "\t|| STSM Shop Manager ||")
    billarea.insert(END, f"\n\nDATE: {dateE.get()}")
    billarea.insert(END, "\n_________________________________________\n")
    billarea.insert(END, "\nProducts\t Price\t QTY\t Sub total")
    billarea.insert(END, "\n==========================================")
    total_price = 0

    for item in curr_items:
        billarea.insert(END, f'\n{item[1]}\t {item[2]}\t {item[3]}\t {item[4]}')
        insert_sql = '''
                INSERT INTO Sellings VALUES
                (?, ?, ?, ?,?)
                '''
        cur.execute(insert_sql, (dateE.get(), item[1], item[2], item[3], item[4]))
        connectObj.commit()
        total_price += item[4]

    billarea.insert(END, '\n------------------------------------------')
    billarea.insert(END, f'\nTOTAL: Rs. {total_price}/-')
    billarea.insert(END, '\n------------------------------------------')
    curr_items.clear()



def view():
    viewarea.delete('0.0', END)
    connectObj = db.connect("shopManagement.db")
    cur = connectObj.cursor()

    sql = 'Select * from Sellings'
    cur.execute(sql)

    rows = cur.fetchall()
    viewarea.insert(END, f"Date\tProduct\tAmount\tQuantity\tPrice\n")

    _sum = 0
    for i in rows:
        _sum += i[4]
        allrows = ""
        for j in i:
            allrows += str(j) + '\t'
        allrows += '\n'
        viewarea.insert(END, allrows)


    viewarea.insert(END, '\n-------------------------------------------')
    viewarea.insert(END, f'\n\tTOTAL: Rs. {_sum}/-')
    viewarea.insert(END, '\n-------------------------------------------')


dateL = Label(root, text="Date", bg="maroon", fg = 'white', width=12, font=('Times New Roman', 15, 'bold'))
dateL.grid(row=0, column=0, padx=7, pady=7)

dateE = DateEntry(root, width=12, font=('arial', 15, 'bold'))
dateE.grid(row=0, column=1, padx=7, pady=7)

Label(root, text="Product", font=('Times New Roman', 15, 'bold'), bg="maroon", fg = 'white', width=12)\
    .grid(row=1, column=0, padx=7, pady=7)

Label(root, text="Quantity", font=('Times New Roman', 15, 'bold'), bg="maroon", fg = 'white', width=12)\
    .grid(row=1, column=1, padx=7, pady=7)

Label(root, text="Sub total", font=('Times New Roman', 15, 'bold'), bg="maroon", fg = 'white', width=12)\
    .grid(row=1, column=2, padx=7, pady=7)

# ----product 1----------------------------------------------------


def calc_price():
    global b
    global qty_entry
    global curr_items
    global temp_items

    connectObj2 = db.connect("shopManagement.db")
    cur = connectObj2.cursor()

    if b['text'] == 'Continue':
        # sql = f'select price, quantity from stocks where product = \'{prod_entry.get()}\''
        sql = f'select * from stocks where product = \'{prod_entry.get()}\''
        cur.execute(sql)
        details = cur.fetchone()
        if details is None:
            messagebox.showerror('Not found', 'No such item found')
        else:
            _, _, price_, quantity = details
            details = list(details)
            if qty_entry.get() == '':
                messagebox.showerror('No quantity', 'Enter quantity')
                return

            details[3] = int(qty_entry.get())
            # curr_items.append(details)
            # print(curr_items)
            details.append(price_ * int(qty_entry.get()))
            if quantity < int(qty_entry.get()):
                messagebox.showerror('Not enough stock', f'Only {quantity} is left')

            else:
                subtotal_label['text'] = f'{price_*int(qty_entry.get())}'
                if b['text'] == 'Continue':
                    b['text'] = 'Add to bill'
                qty_entry['state'] = DISABLED
                prod_entry['state'] = DISABLED
                b2['state'] = NORMAL
                temp_items = details


    elif b['text'] == 'Add to bill':
        sql = f'update stocks set quantity = quantity - {int(qty_entry.get())} where product = \'{prod_entry.get()}\''
        b['text'] = 'Continue'
        b2['state'] = DISABLED
        qty_entry['state'] = NORMAL
        prod_entry['state'] = NORMAL
        qty_entry.delete('0', END)
        prod_entry.delete('0', END)
        subtotal_label['text'] = ''
        cur.execute(sql)
        connectObj2.commit()
        if temp_items is not None:
            curr_items.append(temp_items)
            # print(curr_items)
            temp_items = None


def return_from_func():
    b2['state'] = DISABLED
    b['text'] = 'Continue'
    qty_entry['state'] = NORMAL
    prod_entry['state'] = NORMAL


temp_items = None
curr_items = []

# l = Label(root, text=p1name.get(), font=('arial', 15, 'bold'), width=12)
prod_entry = Entry(root, font=('arial', 15, 'bold'))
prod_entry.grid(row=2, column=0, padx=0, pady=7)

qty_entry = Entry(root, font=('arial', 15, 'bold'), width=12)
qty_entry.grid(row=2, column=1, padx=0, pady=7)

subtotal_label = Label(root, font=('arial', 15, 'bold'), width=12)
subtotal_label.grid(row=2, column=2, padx=0, pady=7)


b = Button(root, text = 'Continue', pady = 10, padx = 10, command = calc_price)
b.grid(row = 3, column = 1, pady = 10)

b2 = Button(root, text = 'Back', height = 1, state = DISABLED, command = return_from_func)
b2.grid(row = 4, column = 1)



# ------------------------bill-------------------------
bill_frame = Frame(root)
bill_frame.grid(columnspan = 3, sticky = NSEW)
billarea = Text(bill_frame)

submitbtn = Button(bill_frame, command=GenerateBill, text="Bill", fg = 'white',
                   font=('Times New Roman', 15, 'bold'), bg="maroon", width=20)

submitbtn.grid(row=6, column=0, padx=7, pady=7, sticky = NSEW)

viewbtn = Button(bill_frame, command=view, text="View All Sellings", fg = 'white',
                 font=('Times New Roman', 15, 'bold'), bg="maroon", width=20)

viewbtn.grid(row=6, column=2, padx=7, pady=7, sticky = NSEW)
billarea.grid(row=9, column=0)
viewarea = Text(bill_frame)
viewarea.grid(row=9, column=2)


# ----------------------------------------------tab2 ----------------------------------
def connection2():
    connectObj2 = db.connect("shopManagement.db")
    cur = connectObj2.cursor()
    sql = '''
    create table if not exists stocks (
        date string,
        product string,
        price number,
        quantity number
        )
    '''
    cur.execute(sql)
    connectObj2.commit()


connection2()


def update_stock():
    # global dateE2, qty, name, price

    if name.get() == '':
        messagebox.showerror('No name', 'No name entered')
        return

    if price.get() == 0 and add_or_del.get() == 10:
        messagebox.showwarning('Free item?', 'The price is set to 0')

    if qty.get() == 0 and add_or_del.get() == 10:
        messagebox.showwarning('Ghost item?', 'The quantity is set to 0')



    connectObj = db.connect("shopManagement.db")
    cur = connectObj.cursor()
    insert_new_sql = '''
            INSERT INTO stocks VALUES 
            (?, ?, ?, ?)
            '''
    existence_sql = f'SELECT EXISTS(SELECT * from stocks WHERE product = \'{name.get()}\')'
    cur.execute(existence_sql)
    exist = cur.fetchone()[0]

    if add_or_del.get() == 10:
        update_sql = f'update stocks set date = \'{dateE.get()}\', price = {int(price.get())},' \
                     f' quantity = quantity + {int(qty.get())} where product = \'{name.get()}\''
        if exist == 0:
            cur.execute(insert_new_sql, (dateE2.get(), name.get(), price.get(), qty.get()))
            viewarea2.insert(END, '\n---------------------------------')
            viewarea2.insert(END, f'\n[ADDED] {name.get()}')
        else:
            # cur.execute(update_sql)
            update_or_not = messagebox.askyesno('Pre existing', f'{name.get()} already exists.'
                                                                f'Do you want to update its price and quantity?')
            if update_or_not:
                cur.execute(update_sql)
                viewarea2.insert(END, '\n---------------------------------')
                viewarea2.insert(END, f'\n[UPDATED] {name.get()}')

    elif add_or_del.get() == 20:
        del_sql = f'DELETE FROM stocks WHERE product = \'{name.get()}\''

        if exist == 0:
            messagebox.showerror('No such item', 'No such item found')
        else:
            cur.execute(del_sql)
            viewarea2.insert(END, '\n---------------------------------')
            viewarea2.insert(END, f'\n[REMOVED] {name.get()}')

    connectObj.commit()



def viewStock():
    viewarea2.delete('0.0', END)

    connectObj = db.connect("shopManagement.db")
    cur = connectObj.cursor()

    sql = 'Select * from stocks'
    cur.execute(sql)

    rows = cur.fetchall()
    viewarea2.insert(END, f"Date \tProduct\t  Price\t  Quantity\t \n")

    for i in rows:
        allrows = ""
        for j in i:
            allrows += str(j) + '\t'
        allrows += '\n'
        viewarea2.insert(END, allrows)


def disable_entry_price():
    update_btn['state'] = NORMAL
    Qty['state'] = DISABLED
    Price['state'] = DISABLED


def enable_entry_price():
    update_btn['state'] = NORMAL

    if Qty['state'] == DISABLED:
        Qty['state'] = NORMAL

    if Price['state'] == DISABLED:
        Price['state'] = NORMAL


date_frame = Frame(root2)
date_frame.pack()
prod_frame = Frame(root2)
prod_frame.pack()
price_frame = Frame(root2)
price_frame.pack()
qty_frame = Frame(root2)
qty_frame.pack()
btns_frame = Frame(root2)
btns_frame.pack()

dateL = Label(date_frame, text="Date", bg="steel blue", fg = 'white', width=12, font=('Times New Roman', 15, 'bold'))
dateL.grid(row=0, column=0, padx=7, pady=7)

dateE2 = DateEntry(date_frame, width=10, bg = 'steel blue', fg = 'white', font=('arial', 15, 'bold'))
dateE2.grid(row=0, column=1, padx=7, pady=7)

Label(prod_frame, text="Product", fg = 'white', font=('Times New Roman', 15, 'bold'), bg="steel blue", width=12)\
    .grid(row=0, column=0, padx=7, pady=7)

Label(price_frame, text="Price", fg = 'white', font=('Times New Roman', 15, 'bold'), bg="steel blue", width=12)\
    .grid(row=0, column=0, padx=7, pady=7)

Label(qty_frame, text="Quantity", fg = 'white', font=('Times New Roman', 15, 'bold'), bg="steel blue", width=12)\
    .grid(row=0, column=0, padx=7, pady=7)

name = StringVar()
price = IntVar()
qty = IntVar()
add_or_del = IntVar()

Name = Entry(prod_frame, textvariable=name, font=('arial', 15, 'bold'), width=12)
Name.grid(row=0, column=1, padx=7, pady=7)

Price = Entry(price_frame, textvariable=price, font=('arial', 15, 'bold'), width=12)
Price.grid(row=0, column=1, padx=7, pady=7)

Qty = Entry(qty_frame, textvariable=qty, font=('arial', 15, 'bold'), width=12)
Qty.grid(row=0, column=1, padx=7, pady=7)

update_btn = Button(btns_frame, command=update_stock, text="Update", fg ='white', state = DISABLED,
            font=('arial', 12, 'bold'), bg="steel blue", width=7)
update_btn.grid(row=1, column=2, padx=7, pady=7)

Radiobutton(btns_frame, text = 'Add to stock', value = 10, var = add_or_del,
            command = enable_entry_price).grid(row = 1, column = 0)

Radiobutton(btns_frame, text = 'Remove from stock', value = 20, var = add_or_del,
            command = disable_entry_price).grid(row = 1, column = 1)


viewarea2 = Text(root2)
viewarea2.pack()

viewbtn2 = Button(root2, command=viewStock, text="View Stock", fg = 'white',
                  font=('Times New Roman', 15, 'bold'), bg="steel blue", width=20).pack()


mainloop()
