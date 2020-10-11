from tkinter import *

#create window-object 
window = Tk()

#create and add 1st-row widgets

#create label
Label(window, text="Kg").grid(row=0, column=0, columnspan=2)

#create function to pass to button as command
def kg_calculator():
    # get kg value from e1
    kg = e1_value.get()
    # convert kg into desired units
    gram = float(kg)*1000
    lbs = float(kg)*2.20462
    oz = float(kg)*35.274
    #output calculated units into respective fields upon clicking b1
    t1.delete("1.0", END)  # Deletes the content of the Text box from start to END
    t1.insert(END, f"{int(gram)}")  # Fill in the text box with the value of gram variable
    t2.delete("1.0", END)
    t2.insert(END, f'{lbs:.2f}')
    t3.delete("1.0", END)
    t3.insert(END, f'{oz:.2f}')

    

#get text variable to pass to textvariable-parameter
e1_value=StringVar()
#create and add entry-widget
e1=Entry(window, textvariable=e1_value)
e1.grid(row=0, column=2, columnspan=2)

#create button-widget
b1 = Button(window, text="Convert", command=kg_calculator) #NOTE: do NOT pass () after function-name, as command is only referencing the function
#add button to specific window-Object location
b1.grid(row=0, column=4, columnspan=2)


#create and add second-row widgets

#create label
Label(window, text="g", justify=CENTER).grid(row=1, column=0)
#create and add text-widget1
t1=Text(window,height=1, width=20)
t1.grid(row=1,column=1)

#create label
Label(window, text="lb", justify=CENTER).grid(row=1, column=2)
#create and add text-widget2
t2=Text(window,height=1, width=20)
t2.grid(row=1,column=3)

#create label
Label(window, text="oz.", justify=CENTER).grid(row=1, column=4)
#create and add text-widget3
t3=Text(window,height=1, width=20)
t3.grid(row=1,column=5)

#shoudl always be at the end of Tkinter-code
window.mainloop()