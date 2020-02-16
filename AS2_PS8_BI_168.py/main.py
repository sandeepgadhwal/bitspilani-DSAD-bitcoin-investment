#!/usr/bin/env python
# coding: utf-8


import os
import time


# Linear solution
def solve_linear(data):
    best_buy_price_idx = 0
    best_sell_price_idx = 0
    buy_price_idx = 0
    buy_price = data[buy_price_idx]
    sale_price = data[0]
    max_profit = 0
    change_buy_price = False

    for i in range(len(data)):        
        sale_price = data[i]
        
        if sale_price < buy_price:
            buy_price = data[i]
            buy_price_idx = i
        else:
            new_profit = sale_price - buy_price
            if new_profit > max_profit:
                max_profit = new_profit
                best_buy_price_idx = buy_price_idx
                best_sell_price_idx = i
            change_buy_price = False
    
    if max_profit > 0:
        return best_buy_price_idx, best_sell_price_idx
    else:
        return None

# Advance solution

lowest_sum = -1000

def get_max_cross_array(arr, l, m, h):
    
    # Get Left side results
    best_left_sum = lowest_sum
    best_left_sum_idx = m
    left_sum = 0
    
    for i in range(m, l-1, -1):
        left_sum+= arr[i]
        #print(best_left_sum, left_sum)
        
        if left_sum > best_left_sum:
            best_left_sum = left_sum
            best_left_sum_idx = i
            
    # Get right side results
    best_right_sum = lowest_sum
    best_right_sum_idx = m+1
    right_sum = 0
    
    for i in range(m+1, h, 1):
        right_sum+=arr[i]
        
        if right_sum > best_right_sum:
            best_right_sum = right_sum
            best_right_sum_idx = i
            
    return best_left_sum+best_right_sum, best_left_sum_idx, best_right_sum_idx+1

def merge_results(result1, result2, result3):
    best_result = result1
    if result2[0] > best_result[0]:
        best_result = result2
    if result3[0] > best_result[0]:
        best_result = result3
    return best_result
    
    
def max_subarray(arr, l, h):
    
    # Base Case
    if l==h:
        return arr[l], l, h
    
    # Find middle of array
    m = (l+h) // 2
    
    result1 = max_subarray(arr, l, m)
    result2 = max_subarray(arr, m+1, h)
    result3 = get_max_cross_array(arr, l, m, h)
    result = merge_results(result1, result2, result3)

    return result

def get_changes(arr):
    changes = []
    for i in range(len(arr)-1):
        changes.append(arr[i+1]-arr[i])
    return changes

def solve_advance(data):
    changes = get_changes(data)
    l = 0
    h = len(changes)
    m = h // 2
    result = max_subarray(changes, l, h-1)
    return result[1], result[2]



# Base Class
class Solver(object):
    def __init__(self, input_file, output_file='outputPS8.txt'):
        self.input_file = os.path.abspath(input_file)
        self.output_file = os.path.abspath(output_file)
        self._data = self.input(self.input_file)

    @property
    def data(self):
        _i = None
        _j = None
        for i, j in zip(self._data[0], self._data[1]):
            change = "-"
            if _j is not None:
                change = j - _j
            print(
                f"Bitcoin price on day {i} is {j} with a change of {change}"
            )
            _i = i 
            _j = j

    def input(self, file=None):
        if file is None:
            file = self.input_file

        with open(file) as f:
            lines = f.read()
            
        lines = lines.replace(',', "")
        line_store = [[], []]
        for line in lines.split('\n')[:-1]:
            day, price = line.split('/')
            line_store[0].append(int(day))
            line_store[1].append(int(price))
        return line_store

    def solve(self, method='linear'): 
        """
        Valid Inputs
        -----------------------------------------------------------------------
        methods: linear, advance
        """
        if method == 'linear':
            solution = solve_linear(self._data[1])
        elif method == 'advance':
            solution = solve_advance(self._data[1])
        else:
            raise Exception("unknown method: supported valued for method are linear, advance")

        if solution is None:
            raise Exception("No Solution")
        
        best_buy_price_idx, best_sell_price_idx = solution
        profit = self._data[1][best_sell_price_idx] - self._data[1][best_buy_price_idx]
        buy_date = self._data[0][best_buy_price_idx]
        sell_date = self._data[0][best_sell_price_idx]

        return buy_date, sell_date, profit

    def output(self, output_file:str='outputPS8.txt'):
        linear_result = self.solve('linear')
        advance_result = self.solve('advance')

        output = f"""
        Maximum Profit (Divide & Conquer solution): {linear_result[2]}
        Day to buy: {linear_result[0]}
        Day to sell: {linear_result[1]}

        Maximum Profit (Iterative solution): {advance_result[2]}
        Day to buy: {advance_result[0]}
        Day to sell: {advance_result[1]}
        """.replace("  ", "").strip()

        with open(output_file, 'w') as f:
            f.write(output)


    # def _solve_tester(self) -> {"purchase date": int, "sale date": int, "profit": int}:
    #     """
    #     Testing function

    #     it will always return correct answer
    #     """
    #     best_buy_price_idx = 0
    #     best_sell_price_idx = 0
    #     change = 0
    #     for i, price in enumerate(self._data[1]):
    #         for j in range(i, len(self._data[1])):
    #             if self._data[1][j]  > self._data[1][i]:
    #                 _change = self._data[1][j] - self._data[1][i]
    #                 if _change > change:
    #                     best_buy_price_idx = i
    #                     best_sell_price_idx = j
    #                     change = _change
    #     # return best_buy_price_idx, best_sell_price_idx, change
    #     profit = self._data[1][best_sell_price_idx] - self._data[1][best_buy_price_idx]
    #     buy_date = self._data[0][best_buy_price_idx]
    #     sell_date = self._data[0][best_sell_price_idx]

    #     return buy_date, sell_date, profit

    # def _randomize(self):
    #     """
    #     testing function
    #     """
    #     self._data[1] = [random.randint(0, 10000) for x in range(len(self._data[1]))]

    # def _run_tests(self, n_times=10):
    #     """
    #     testing function
    #     """
    #     self._test_now()
    #     print("-- algorithm test passed on original data ")

    #     for i in range(n_times):
    #         print(f"-- tesing algorithm {i+1}/{n_times}")
    #         self._randomize
    #         self._test_now()
    
    # def _test_now(self):
    #     """
    #     testing function
    #     """
    #     solution = self._solve_tester()
    #     if not (solution == self.solve("linear")):
    #         raise Exception("--# linear algo failed")
    #     if not (solution == self.solve("advance")):
    #         raise Exception("--# advance algo failed")  


