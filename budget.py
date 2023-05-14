class Category:

    def __init__(self, catname):
        'generate an empty list for a ledger and create name of category'
        self.ledger = []
        self.__name__ = catname

    def deposit(self, amount, description=''):
        'add funds to ledger'
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=''):
        'withdraw amount from ledger if we have the funds'
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False

    def get_balance(self):
        'sum of all amounts'
        return sum(x['amount'] for x in self.ledger)

    def transfer(self, amount, destination):
        'tranfer amount between categories if we have the funds'
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": f'Transfer to {destination.__name__}'})
            destination.ledger.append({"amount": amount, "description": f'Transfer from {self.__name__}'})
            return True
        else:
            return False

    def check_funds(self, amount):
        'check available funds in balance'
        if self.get_balance() >= amount:
            return True
        else:
            return False

    def __str__(self):
        'return result for print func'
        #generate title
        title = self.__name__.center(30, '*')

        #create func for round float numbers
        def toFixed(numObj, digits=2):
            'round float numbers to 2 digits after dot'
            return f"{numObj:.{digits}f}"

        #generate the mega-string of records from ledger
        all_ledger = []
        for x in self.ledger:
            all_ledger.append(f'{(x["description"][:23]).ljust(23, " ")}{(toFixed(x["amount"])[:7]).rjust(7, " ")}')
        all_ledger = "\n".join(all_ledger)

        #round total amount
        total = f'Total: {toFixed(self.get_balance())}'
        return title+'\n'+all_ledger+'\n'+total

def create_spend_chart(categories):
    'it draws one of craziest chart in the world'

    #calculate spendings by categories and round down to the nearest 10
    spendings = {}
    for i in categories:
        #sum of all withdraws
        spendings[i.__name__] = sum([x["amount"] for x in  i.ledger if x["amount"] < 0])
    #round down to the nearest 10
    spendings = {x: round(y/sum(spendings.values()), 2)*100 for x, y in spendings.items()}

    #generate list with first element - the title of the table
    table = ['Percentage spent by category']

    #generate strings with 10s spendings
    for i in range(100, -1,  -10):

        #wtite 10s in new list
        total_st = [f'{str(i).rjust(3, " ")}|']

        #add 'o ' or '  ' to list
        for x, y in spendings.items():
            if y >= i:
                total_st.append('o ')
            else:
                total_st.append('  ')
        #add string to table
        table.append(' '.join(total_st)+' ')

    #add '-' string
    table.append(f'    {"-"*(len(categories)*3+1)}')

    #generate strings with letters of categories names
    letters = []
    cats_names = [x.__name__ for x in categories]
    max_len_cat_name= len(max(cats_names, key=len))
    #create lists with letters and ' '
    for i in cats_names:
       letters.append(list(i.ljust(max_len_cat_name, " ")))
    #zip all lists for generate string for table
    letters = zip(*letters)
    for i in letters:
        table.append(f'     {"  ".join(i)}  ')

    return '\n'.join(table)

