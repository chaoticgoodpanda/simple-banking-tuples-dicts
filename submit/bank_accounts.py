'''
This Python assignment will involve implementing a bank program that manages bank accounts and allows
for deposits, withdrawals, and purchases.

The program will initially load a list of accounts from a .txt file, and deposits and withdrawals from
additional .csv files. Then it will parse and combine all of the data and store it in a dictionary.

'''

def init_bank_accounts(accounts, deposits, withdrawals):
    '''
    Loads the given 3 files, stores the information for individual bank accounts in a dictionary,
    and calculates the account balance.

    Accounts file contains information about bank accounts.
    Each row contains an account number, a first name, and a last name, separated by vertical pipe (|).
    Example:
    1|Brandon|Krakowsky

    Deposits file contains a list of deposits for a given account number.
    Each row contains an account number, and a list of deposit amounts, separated by a comma (,).
    Example:
    1,234.5,6352.89,1,97.60

    Withdrawals file contains a list of withdrawals for a given account number.
    Each row contains an account number, and a list of withdrawal amounts, separated by a comma (,).
    Example:
    1,56.3,72.1

    Stores all of the account information in a dictionary named 'bank_accounts', where the account number is the key,
    and the value is a nested dictionary.  The keys in the nested dictionary are first_name, last_name, and balance,
    with the corresponding values.
    Example:
    {'1': {'first_name': 'Brandon', 'last_name': 'Krakowsky', 'balance': 6557.59}}

    This function calculates the total balance for each account by taking the total deposit amount
    and subtracting the total withdrawal amount.
    '''

    bank_accounts = {}

    # TODO insert your code
    f_accounts = open(accounts, 'r')
    f_deposits = open(deposits, 'r')
    f_withdrawals = open(withdrawals, 'r')

    # first, accounts
    # read all lines in account into a list
    acct_lines = f_accounts.readlines()

    # clean up accounts list
    for line in acct_lines:
        # strip whitespace and split by bar separator
        lst = line.strip().split('|')

        # strip whitespace from first part, call it a 'key'
        key = lst[0].strip()

        # strip whitespace from second part, call it 'first_name'
        first_name = lst[1].strip()

        # strip whitespace from 3rd part, call it 'last_name'
        last_name = lst[2].strip()

        #add key, {first name, last name} to bank accounts dict
        bank_accounts[key] = {}
        bank_accounts[key]['first_name'] = first_name
        bank_accounts[key]['last_name'] = last_name

    # second, deposits
    # read from file
    acct_deposits = f_deposits.readlines()

    # read each row in deposits csv
    for line in acct_deposits:
        # split into comma-separated list
        d_lst = line.split(',')

        # strip whitespace from first part, call it a 'key'
        key = d_lst[0].strip()

        # if line length is 1 or less, set balance to zero
        if len(d_lst) <= 1:
            bank_accounts[key]['balance'] = 0
            continue

        sum_row = 0
        # sum the remaining values in the line
        for i in range(1, len(d_lst)):
            sum_row += float(d_lst[i])

        # truncate float
        sum_row = round(sum_row, 2)

        # add key, {balance, value} to bank accounts dict
        bank_accounts[key]['balance'] = sum_row

    # finally, read from withdrawals csv
    acct_with = f_withdrawals.readlines()

    # read each row in withdrawals
    for line in acct_with:
        # split into comma-separated list
        w_lst = line.split(',')

        # strip whitespace from first part, call it a 'key'
        key = w_lst[0].strip()

        # if line length is 1 or less, skip
        if len(w_lst) <= 1:
            continue

        sum_with = 0
        # sum the total withdrawals in the line
        for i in range(1, len(w_lst)):
            sum_with += float(w_lst[i])

        # truncate float
        sum_with = round(sum_with, 2)

        # subtract from balance withdrawals
        bank_accounts[key]['balance'] -= sum_with

    # close files
    f_accounts.close()
    f_deposits.close()
    f_withdrawals.close()

    return bank_accounts

def round_balance(bank_accounts, account_number):
    '''Rounds the given amount to two decimal places.
    '''

    # TODO insert your code
    round_number = round(bank_accounts[account_number]['balance'], 2)

    return round_number

def get_account_info(bank_accounts, account_number):
    '''Returns the account information for the given account_number as a dictionary.
    Example:
    {'first_name': 'Brandon', 'last_name': 'Krakowsky', 'balance': 6557.59}
    If the account doesn't exist, returns None.
    '''

    # TODO insert your code
    if account_number not in bank_accounts:
        return None
    account_info = bank_accounts[account_number]

    return account_info

def withdraw(bank_accounts, account_number, amount):
    '''Withdraws the given amount from the account with the given account_number.
    Rounds the new balance to 2 decimal places.
    If the account doesn't exist, prints a friendly message.
    Raises a RuntimeError if the given amount is greater than the available balance.
    Prints the new balance.
    '''

    # TODO insert your code
    if account_number not in bank_accounts:
        return "Sorry! The typed number is not in a bank account."
    if bank_accounts[account_number]['balance'] < amount:
        raise RuntimeError('The requested withdrawal is greater than the amount remaining in the bank account!')
    else:
        bank_accounts[account_number]['balance'] -= amount
        bank_accounts[account_number]['balance'] = round_balance(bank_accounts, account_number)
        print(str(amount) + ' has been withdrawn and your new balance is: ' + str(bank_accounts[account_number]['balance']))

def deposit(bank_accounts, account_number, amount):
    '''Deposits the given amount into the account with the given account_number.
    Rounds the new balance to 2 decimal places.
    If the account doesn't exist, prints a friendly message.
    Prints the new balance.
    '''

    # TODO insert your code

    if account_number not in bank_accounts:
        return "Sorry! The typed number is not in a bank account."
    else:
        bank_accounts[account_number]['balance'] += amount
        bank_accounts[account_number]['balance'] = round_balance(bank_accounts, account_number)
        print(str(amount) + ' has been deposited and your new balance is: ' + str(bank_accounts[account_number]['balance']))


def purchase(bank_accounts, account_number, amounts):
    '''Makes a purchase with the total of the given list of amounts from the account with the given account_number.
    If the account doesn't exist, prints a friendly message.
    Calculates the total purchase amount based on the sum of the given list of amounts, plus (6%) sales tax.
    Raises a RuntimeError if the total purchase amount is greater than the available balance.
    Prints the new balance.
    '''

    # TODO insert your code
    if account_number not in bank_accounts:
        return "Sorry! The typed number is not in a bank account."
    # calculate sum of numbers in list
    total_purchase_amt = 0
    for i in amounts:
        total_purchase_amt += i

    
    total_purchase_amt += calculate_sales_tax(total_purchase_amt)
    if total_purchase_amt > bank_accounts[account_number]['balance']:
        raise RuntimeError('The requested purchase amount is greater than the amount remaining in the bank account!')
    else:
        withdraw(bank_accounts, account_number, total_purchase_amt)

def calculate_sales_tax(amount):
    '''Calculates and returns a 6% sales tax for the given amount.'''

    # TODO insert your code
    sales_tax = amount * 0.06
    return sales_tax

def sort_accounts(bank_accounts, sort_type, sort_direction):
    '''Converts the key:value pairs in the given bank_accounts dictionary to
    a list of tuples and sorts based on the given sort_type and sort_direction.
    Returns the sorted list of tuples.

    If the sort_type argument is the string ‘account_number’, sorts the list of tuples based on
    the account number (e.g. ‘3’, '5') in the given sort_direction (e.g. 'asc', 'desc').
    Example sorted results based on 'account_number' in ascending order:
    ('1', {'first_name': 'Brandon', 'last_name': 'Krakowsky', 'balance': 6557.59}),
    ('2', {'first_name': 'Chenyun', 'last_name': 'Wei', 'balance': 4716.89})
    ('3', {'first_name': 'Dingyi', 'last_name': 'Shen', 'balance': 4.14})

    otherwise, if the sort_type argument is 'first_name', 'last_name', or 'balance', sorts the list based on
    the associated values (e.g. 'Brandon', 'Krakowsky', or 6557.59) in the given sort_direction (e.g. 'asc', 'desc').
    Example sorted results based on 'balance' in descending order:
    ('6', {'first_name': 'Karishma', 'last_name': 'Jain', 'balance': 6700.19}),
    ('1', {'first_name': 'Brandon', 'last_name': 'Krakowsky', 'balance': 6557.59}),
    ('2', {'first_name': 'Chenyun', 'last_name': 'Wei', 'balance': 4716.89})

    Example sorted results based on 'last_name' in ascending order:
    ('4', {'first_name': 'Zhe', 'last_name': 'Cai', 'balance': 114.31}),
    ('9', {'first_name': 'Ruijie', 'last_name': 'Cao', 'balance': 651.44}),
    ('1', {'first_name': 'Brandon', 'last_name': 'Krakowsky', 'balance': 6557.59})

    Example sorted results based on 'first_name' in descending order
    ('4', {'first_name': 'Zhe', 'last_name': 'Cai', 'balance': 114.31}),
    ('10', {'first_name': 'Tianshi', 'last_name': 'Wang', 'balance': 0.0})
    ('6', {'first_name': 'Karishma', 'last_name': 'Jain', 'balance': 6700.19}),
    ('1', {'first_name': 'Brandon', 'last_name': 'Krakowsky', 'balance': 6557.59})
    '''

    # TODO insert your code
    tuple_list = list(bank_accounts.items())
    if sort_type == 'account_number':
        if sort_direction == 'asc':
            # sort the tuple list, cast x[0] to int so numbers are truly in order and '10' doesn't come immediately after '1'
            sorted_tuple_list = sorted(tuple_list, key=lambda x: int(x[0]))
            return sorted_tuple_list
        if sort_direction == 'desc':
            # reverse the sign to sort in descending order, cast to int
            sorted_tuple_list = sorted(tuple_list, key=lambda x: -int(x[0]))
            return sorted_tuple_list
    else:
        if sort_type == 'first_name':
            if sort_direction == 'asc':
                sorted_tuple_list = sorted(tuple_list, key=lambda x: x[1]['first_name'])
                return sorted_tuple_list
            if sort_direction == 'desc':
                sorted_tuple_list = sorted(tuple_list, key=lambda x: x[1]['first_name'], reverse=True)
                return sorted_tuple_list
        if sort_type == 'last_name':
            if sort_direction == 'asc':
                sorted_tuple_list = sorted(tuple_list, key=lambda x: x[1]['last_name'])
                return sorted_tuple_list
            if sort_direction == 'desc':
                sorted_tuple_list = sorted(tuple_list, key=lambda x: x[1]['last_name'], reverse=True)
                return sorted_tuple_list
        if sort_type == 'balance':
            if sort_direction == 'asc':
                sorted_tuple_list = sorted(tuple_list, key=lambda x: float(x[1]['balance']))
                return sorted_tuple_list
            if sort_direction == 'desc':
                sorted_tuple_list = sorted(tuple_list, key=lambda x: -float(x[1]['balance']))
                return sorted_tuple_list


def export_statement(bank_accounts, account_number, output_file):
    '''Exports the given account information to the given output file in the following format:

    First Name: Huize
    Last Name: Huang
    Balance: 34.57
    '''

    # TODO insert your code
    lst = []
    lst.insert(0, 'First Name: ' + bank_accounts[account_number]['first_name'] + '\n')
    lst.insert(1, 'Last Name: ' + bank_accounts[account_number]['last_name'] + '\n')
    round_balance(bank_accounts, account_number)
    lst.insert(2, 'Balance: ' + str(bank_accounts[account_number]['balance']) + "\n'''")
    fout = open(output_file, 'w')
    fout.writelines(lst)

    # close the file to save it
    fout.close()

def main():

    #load and get all account info
    bank_accounts = init_bank_accounts('accounts.txt', 'deposits.csv', 'withdrawals.csv')

    #for testing
    #print(bank_accounts)

    while True:

        #print welcome and options
        print('\nWelcome to the bank!  What would you like to do?')
        print('1: Get account info')
        print('2: Make a deposit')
        print('3: Make a withdrawal')
        print('4: Make a purchase')
        print('5: Sort accounts')
        print('6: Export a statement')
        print('0: Leave the bank')

        # get user input
        option_input = input('\n')

        # try to cast to int
        try:
            option = int(option_input)

        # catch ValueError
        except ValueError:
            print("Invalid option.")

        else:

            #check options
            if (option == 1):

                #get account number and print account info
                account_number = input('Account number? ')
                print(get_account_info(bank_accounts, account_number))

            elif (option == 2):

                # get account number and amount and make deposit
                account_number = input('Account number? ')

                # input cast to float
                amount = float(input('Amount? '))

                deposit(bank_accounts, account_number, amount)

            elif (option == 3):

                # get account number and amount and make withdrawal
                account_number = input('Account number? ')

                #input cast to float
                amount = float(input('Amount?  '))

                withdraw(bank_accounts, account_number, amount)

            elif (option == 4):

                # get account number and amounts and make purchase
                account_number = input('Account number? ')
                amounts = input('Amounts (as comma separated list)? ')

                # convert given amounts to list
                amount_list = amounts.split(',')
                amount_list = [float(i) for i in amount_list]

                purchase(bank_accounts, account_number, amount_list)

            elif (option == 5):

                # get sort type
                sort_type = input("Sort type ('account_number', 'first_name', 'last_name', or 'balance')? ")

                # get sort direction
                sort_direction = input("Sort type ('asc' or 'desc')? ")

                print(sort_accounts(bank_accounts, sort_type, sort_direction))

            elif (option == 6):

                # get account number to export
                account_number = input('Account number? ')

                export_statement(bank_accounts, account_number, account_number + '.txt')

            elif (option == 0):

                # print message and leave the bank
                print('Goodbye!')
                break


if __name__ == "__main__":
    main()
