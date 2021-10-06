import unittest

from bank_accounts import *

class BankAccounts_Tests(unittest.TestCase):

    def setUp(self):

        self.bank_accounts = init_bank_accounts('accounts.txt', 'deposits.csv', 'withdrawals.csv')

    def test_init_bank_accounts(self):

        # get balance of existing accounts

        #6685.99 - 128.4 = 6557.59
        self.assertAlmostEqual(6557.59, self.bank_accounts['1']['balance'])

        #4739.87 - 22.98
        self.assertAlmostEqual(4716.89, self.bank_accounts['2']['balance'])

        #0 - 0
        self.assertEqual(0.0, self.bank_accounts['7']['balance'])

        #0 - 0
        self.assertEqual(0.0, self.bank_accounts['10']['balance'])


    def test_get_account_info(self):

        #get account info from existing accounts
        account_info = get_account_info(self.bank_accounts, '1')
        self.assertAlmostEqual(6557.59, account_info['balance'])
        self.assertEqual('Brandon', account_info['first_name'])
        self.assertEqual('Krakowsky', account_info['last_name'])

        account_info = get_account_info(self.bank_accounts, '2')
        self.assertAlmostEqual(4716.89, account_info['balance'])

        account_info = get_account_info(self.bank_accounts, '7')
        self.assertEqual(0.0, account_info['balance'])
        self.assertEqual('Huize', account_info['first_name'])
        self.assertEqual('Huang', account_info['last_name'])

        account_info = get_account_info(self.bank_accounts, '10')
        self.assertEqual(0.0, account_info['balance'])

        #get account info from non-existant account
        account_info = get_account_info(self.bank_accounts, '1234')
        self.assertEqual(None, account_info)

    def test_withdraw(self):

        #withdraw from existing accounts
        self.assertAlmostEqual(6700.19, get_account_info(self.bank_accounts, '6')['balance'])
        withdraw(self.bank_accounts, '6', .19)
        #6700.19 - .19 = 6700.00
        self.assertAlmostEqual(6700.00, get_account_info(self.bank_accounts, '6')['balance'])

        self.assertAlmostEqual(651.44, get_account_info(self.bank_accounts, '9')['balance'])
        withdraw(self.bank_accounts, '9', 651)
        #651.44 - 651 = .44
        self.assertAlmostEqual(.44, get_account_info(self.bank_accounts, '9')['balance'])

        # withdraw too much
        self.assertEqual(0.0, get_account_info(self.bank_accounts, '10')['balance'])
        #0.0 - .1 = RuntimeError
        self.assertRaises(RuntimeError, withdraw, self.bank_accounts, '10', .1)

        #withdraw from non-existant accounts
        withdraw(self.bank_accounts, '3ew231', 1.99)

    def test_deposit(self):

        # deposit to existing accounts
        self.assertAlmostEqual(6700.19, get_account_info(self.bank_accounts, '6')['balance'])
        deposit(self.bank_accounts, '6', 1)
        #6700.19 + 1 = 6701.19
        self.assertAlmostEqual(6701.19, get_account_info(self.bank_accounts, '6')['balance'])

        self.assertAlmostEqual(651.44, get_account_info(self.bank_accounts, '9')['balance'])
        deposit(self.bank_accounts, '9', 1000.01)
        # 651.44 + 1000.01 = 1651.45
        self.assertAlmostEqual(1651.45, get_account_info(self.bank_accounts, '9')['balance'])

        self.assertEqual(0.0, get_account_info(self.bank_accounts, '10')['balance'])
        deposit(self.bank_accounts, '10', 0)
        # 0.0 + 0 = 0.0
        self.assertEqual(0.0, get_account_info(self.bank_accounts, '10')['balance'])

        # deposit to non-existent account
        deposit(self.bank_accounts, '3ew231', 1.99)

    def test_purchase(self):

        # purchase from existing accounts
        self.assertAlmostEqual(4716.89, get_account_info(self.bank_accounts, '2')['balance'])
        purchase(self.bank_accounts, '2', [3.2, 4.89, 32.9])
        #4716.89 - (40.99 + 2.46) = 4673.44
        self.assertAlmostEqual(4673.44, get_account_info(self.bank_accounts, '2')['balance'], 2)

        self.assertAlmostEqual(6557.59, get_account_info(self.bank_accounts, '1')['balance'])
        # 6557.59 - (6557.59 + 393.46) = RuntimeError
        self.assertRaises(RuntimeError, purchase, self.bank_accounts, '1', [6557, .59])

        self.assertAlmostEqual(651.44, get_account_info(self.bank_accounts, '9')['balance'])
        # 651.44 - (651.45 + 39.087) = RuntimeError
        self.assertRaises(RuntimeError, purchase, self.bank_accounts, '9', [.45, 651])

        # purchase from non-existent account
        purchase(self.bank_accounts, '3425', [1.99])

    def test_sort_accounts(self):
        sorted_accounts = sort_accounts(self.bank_accounts, 'balance', 'desc')
        self.assertEqual(('6', {'first_name': 'Karishma', 'last_name': 'Jain', 'balance': 6700.19}), sorted_accounts[0])
        self.assertEqual(('1', {'first_name': 'Brandon', 'last_name': 'Krakowsky', 'balance': 6557.59}),
                         sorted_accounts[1])
        self.assertEqual(('2', {'first_name': 'Chenyun', 'last_name': 'Wei', 'balance': 4716.89}), sorted_accounts[2])

        sorted_accounts = sort_accounts(self.bank_accounts, 'last_name', 'asc')
        self.assertEqual(('4', {'first_name': 'Zhe', 'last_name': 'Cai', 'balance': 114.31}), sorted_accounts[0])
        self.assertEqual(('9', {'first_name': 'Ruijie', 'last_name': 'Cao', 'balance': 651.44}), sorted_accounts[1])
        self.assertEqual(('7', {'first_name': 'Huize', 'last_name': 'Huang', 'balance': 0}), sorted_accounts[2])

        sorted_accounts = sort_accounts(self.bank_accounts, 'first_name', 'desc')
        self.assertEqual(('4', {'first_name': 'Zhe', 'last_name': 'Cai', 'balance': 114.31}), sorted_accounts[0])
        self.assertEqual(('10', {'first_name': 'Tianshi', 'last_name': 'Wang', 'balance': 0.0}), sorted_accounts[1])
        self.assertEqual(('9', {'first_name': 'Ruijie', 'last_name': 'Cao', 'balance': 651.44}), sorted_accounts[2])

        sorted_accounts = sort_accounts(self.bank_accounts, 'account_number', 'asc')
        self.assertEqual(('1', {'first_name': 'Brandon', 'last_name': 'Krakowsky', 'balance': 6557.59}),
                         sorted_accounts[0])
        self.assertEqual(('2', {'first_name': 'Chenyun', 'last_name': 'Wei', 'balance': 4716.89}), sorted_accounts[1])
        self.assertEqual(('3', {'first_name': 'Dingyi', 'last_name': 'Shen', 'balance': 4.14}), sorted_accounts[2])

    def test_export_statement(self):

        export_statement(self.bank_accounts, '3', '3.txt')
        export_statement(self.bank_accounts, '4', '4.txt')
        export_statement(self.bank_accounts, '5', '5.txt')

        # check file exports for correct formatting of the info

if __name__ == '__main__':
    unittest.main()