"""
A program that stores the following book information:
Title, Author
Year, ISBN

User can:
View all records
Search an entry
Add an entry
Update an entry
Delete Entries
Close the application (+ the connection to the database)
"""

import tkinter as tk
from backend import Database

database = Database("books.db")

class Library:

    def __init__(self, window, title):
        #create window
        self.window = window 

        #add window icon
        self.window.iconbitmap('icons\\books.ico')

        # add window-title
        self.window.wm_title(title)

            #create labels
        l1 = tk.Label(self.window, text="Title")
        l1.grid(row=0, column=0)

        l2 = tk.Label(self.window, text="Author").grid(row=0, column=2) #HERE: grid can alse be appended directly, as no methods will be called on l2 later on

        l3 = tk.Label(self.window, text="Year")
        l3.grid(row=1, column=0)

        l4 = tk.Label(self.window, text="ISBN")
        l4.grid(row=1, column=2)

        #create StringVar()-objects and entry-widgets using StringVar() as textvariable
        self.title_text = tk.StringVar() #A StringVar() is used to edit a widget's text
        self.e1 = tk.Entry(self.window, textvariable=self.title_text)
        self.e1.grid(row=0, column=1) #NOTE: call .grid() separately as it returns None and e1 should not have the value of None

        self.author_text = tk.StringVar() #A StringVar() is used to edit a widget's text
        self.e2 = tk.Entry(self.window, textvariable=self.author_text)
        self.e2.grid(row=0, column=3)

        self.year_text = tk.StringVar() #A StringVar() is used to edit a widget's text
        self.e3 = tk.Entry(self.window, textvariable=self.year_text)
        self.e3.grid(row=1, column=1)

        self.isbn_text = tk.StringVar() #A StringVar() is used to edit a widget's text
        self.e4 = tk.Entry(self.window, textvariable=self.isbn_text)
        self.e4.grid(row=1, column=3)

        #create listbox-widget
        self.list1 = tk.Listbox(self.window, height=6, width=70)
        self.list1.grid(row=2, column=0, rowspan=6, columnspan=2) #NOTE: grid() called separately here as using it returns None, which can not be used to use subsequent methods (e.g. configure or set) on it

        #create scrollbar --> will not be refereneced outside of __init__-method, so "self." does not need to be pre-appended
        sb1 = tk.Scrollbar(self.window)
        sb1.grid(row=2, column=2, rowspan=6)

        #add scrollbar to listbox
        self.list1.configure(yscrollcommand=sb1.set)
        sb1.configure(command=self.list1.yview)

        # bind function to list1-widget --> select row for subsequent operations (e.g. deleting)
        self.list1.bind('<<ListboxSelect>>', self.get_selected_row)

        #create buttons
        b1 = tk.Button(self.window, text="View all", width = 12, command= self.view_command)
        b1.grid(row=2, column=3)

        b2 = tk.Button(self.window, text="Search entry", width = 12, command= self.search_command)
        b2.grid(row=3, column=3)

        b3 = tk.Button(self.window, text="Add entry", width = 12, command= self.add_command)
        b3.grid(row=4, column=3)

        b4 = tk.Button(self.window, text="Update", width = 12, command= self.update_command)
        b4.grid(row=5, column=3)

        b5 = tk.Button(self.window, text="Delete", width = 12, command = self.delete_command)
        b5.grid(row=6, column=3)

        b6 = tk.Button(self.window, text="Close", width = 12, command = self.close_command)
        b6.grid(row=7, column=3)


    # function pretty-printing SQL-query results
    def pretty_print(self, book):
            return f"{book[0]} {book[1]} {book[2]} {book[3]} {book[4]}"

    # command listing all books in database, to pass to b1
    def view_command(self):
        # make sure list ist empty before starting
        self.list1.delete(0, tk.END)
        # get all books' info from db
        books = database.view()
        # iterate over results and add them into list1 per row
        for book in books:
            self.list1.insert(tk.END, self.pretty_print(book))

    def search_command(self):
        # make sure list ist empty before starting
        self.list1.delete(0, tk.END)
        # get results for specified values
        books = database.search(title=self.title_text.get(),
                                author=self.author_text.get(),
                                year=self.year_text.get(),
                                isbn=self.isbn_text.get()) #.get()-method converts StringVar()-objects (from respective entry-fields) into Python string-objects 
        # iterate over results and insert into list1
        for book in books:
            self.list1.insert(tk.END, self.pretty_print(book))

    def add_command(self):
        # get value input from entry-fields
        title=self.title_text.get()
        author=self.author_text.get()
        year=self.year_text.get()
        isbn=self.isbn_text.get()
        # insert into db
        database.insert(title, author, year, isbn)
        # use search_command() in order to print newly added book info to list1 (NOTE: parameters are same as above and taken from same entry)
        self.search_command()
        # update list1 - view
        self.view_command()

    def get_selected_row(self, event):
        try:
            # get list1-index of selected row
            index = self.list1.curselection()[0] 
            # get value (string is pretty_print was used, otherwise tuple) from selected index
            selected_tuple = self.list1.get(index)
            # separate string by whitespace and save book_id (database-id) into variable 
            global book_id_to_modify #make global so that it can be used without calling get_selected_function() again
            book_id_to_modify = selected_tuple.split()[0]
            # get book-info from db based on id -->for aesthetic purposes as database.delete() takes only ID as argument
            book_props = database.search_by_id(book_id_to_modify)
            # # clear entry field entries and fill book proeprties into entry fields -->for aesthetic purposes as database.delete() takes only ID as argument
            self.e1.delete(0, tk.END)
            self.e1.insert(tk.END, book_props[1])
            self.e2.delete(0, tk.END)
            self.e2.insert(tk.END, book_props[2])
            self.e3.delete(0, tk.END)
            self.e3.insert(tk.END, book_props[3])
            self.e4.delete(0, tk.END)
            self.e4.insert(tk.END, book_props[4])
            # return global book_id 
            return book_id_to_modify
        except IndexError:
            pass

    def update_command(self):
        # get (updated) infor from entry fields
        title=self.title_text.get()
        author=self.author_text.get()
        year=self.year_text.get()
        isbn=self.isbn_text.get()
        # update selected entry
        database.update(book_id_to_modify, title, author, year, isbn)
        # update list1 - view
        self.view_command()


    def delete_command(self):
        # delete selected entry
        database.delete(book_id_to_modify)
        # oipdate list1 - view
        self.view_command()

    def close_command(self):
        database.close()  
        self.window.destroy() 



if __name__ == "__main__":
    window=tk.Tk()
    Library(window, 'Library')
    #should always be at the end of Tkinter-code
    window.mainloop()

