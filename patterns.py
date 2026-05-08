"""
FP-Growth implementation without mlxtend — pure Python + pandas.
"""
import pandas as pd
import numpy as np
from collections import defaultdict
from itertools import combinations
from modules.preprocess import load_data


class FPNode:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.link = None

    def increment(self, count):
        self.count += count


class FPTree:
    def __init__(self, transactions, min_support):
        self.frequent = self._get_frequent(transactions, min_support)
        self.headers = {k: None for k in self.frequent}
        self.root = FPNode(None, 0, None)
        self._build_tree(transactions)

    def _get_frequent(self, transactions, min_support):
        counts = defaultdict(int)
        for t in transactions:
            for item in t:
                counts[item] += 1
        return {k: v for k, v in counts.items() if v >= min_support}

    def _build_tree(self, transactions):
        for trans in transactions:
            sorted_items = sorted(
                [i for i in trans if i in self.frequent],
                key=lambda x: self.frequent[x], reverse=True
            )
            self._insert_tree(sorted_items, self.root)

    def _insert_tree(self, items, node):
        if not items:
            return
        head = items[0]
        if head in node.children:
            node.children[head].increment(1)
        else:
            child = FPNode(head, 1, node)
            node.children[head] = child
            self._link(head, child)
        self._insert_tree(items[1:], node.children[head])

    def _link(self, item, node):
        if self.headers[item] is None:
            self.headers[item] = node
        else:
            current = self.headers[item]
            while current.link:
                current = current.link
            current.link = node

    def _prefix_paths(self, base_pattern, min_support):
        paths = []
        node = self.headers.get(base_pattern)
        while node:
            path = []
            parent = node.parent
            while parent and parent.item is not None:
                path.append(parent.item)
                parent = parent.parent
            if path:
                paths.append((path, node.count))
            node = node.link
        return paths

    def mine(self, prefix, min_support, results):
        for item in sorted(self.frequent, key=self.frequent.get):
            new_pattern = prefix | frozenset([item])
            results[new_pattern] = self.frequent[item]
            cond_transactions = []
            for path, count in self._prefix_paths(item, min_support):
                cond_transactions.extend([path] * count)
            if cond_transactions:
                cond_tree = FPTree(cond_transactions, min_support)
                cond_tree.mine(new_pattern, min_support, results)


def fp_growth(transactions, min_support):
    tree = FPTree(transactions, min_support)
    results = {}
    tree.mine(frozenset(), min_support, results)
    return results


def discretize_data(df):
    df = df.copy()
    df['High_BP'] = df['Blood Pressure'] >= 140
    df['High_Cholesterol'] = df['Cholesterol'] >= 200
    df['High_Glucose'] = df['Glucose'] >= 140
    df['High_BMI'] = df['BMI'] >= 30
    df['High_Triglycerides'] = df['Triglycerides'] >= 200
    df['High_HbA1c'] = df['HbA1c'] >= 6.5
    df['Smoker'] = df['Smoking'] == 1
    df['Family_Hx'] = df['Family History'] == 1
    df['High_Stress'] = df['Stress Level'] >= 7
    df['Low_Sleep'] = df['Sleep Hours'] <= 5
    df['Senior'] = df['Age'] >= 60

    for cond in df['Medical Condition'].unique():
        col = 'Has_' + cond.replace(' ', '_')
        df[col] = df['Medical Condition'] == cond

    bool_cols = [c for c in df.columns if df[c].dtype == bool]
    return df[bool_cols]


def run_fpgrowth(min_support_pct=0.20, min_confidence=0.50, min_lift=1.0):
    df = load_data()
    bool_df = discretize_data(df)
    n = len(bool_df)
    min_sup_count = int(min_support_pct * n)

    transactions = []
    for _, row in bool_df.iterrows():
        t = [col for col in bool_df.columns if row[col]]
        transactions.append(t)

    freq_items = fp_growth(transactions, min_sup_count)

    if not freq_items:
        return pd.DataFrame(), pd.DataFrame()

    # Build item support lookup
    item_support = {k: v / n for k, v in freq_items.items()}

    rules_list = []
    for itemset, sup_count in freq_items.items():
        if len(itemset) < 2:
            continue
        items = list(itemset)
        for r in range(1, len(items)):
            for ant_tuple in combinations(items, r):
                ant = frozenset(ant_tuple)
                con = itemset - ant
                if not con:
                    continue
                sup = sup_count / n
                ant_sup = item_support.get(ant, 0)
                if ant_sup == 0:
                    continue
                conf = sup / ant_sup
                con_sup = item_support.get(con, 0)
                lift = conf / con_sup if con_sup > 0 else 0

                if conf >= min_confidence and lift >= min_lift:
                    rules_list.append({
                        'Antecedents (IF)': ' + '.join(sorted(ant)),
                        'Consequents (THEN)': ' + '.join(sorted(con)),
                        'Support': round(sup, 4),
                        'Confidence': round(conf, 4),
                        'Lift': round(lift, 4),
                    })

    rules = pd.DataFrame(rules_list)
    if not rules.empty:
        rules = rules.sort_values('Lift', ascending=False).reset_index(drop=True)

    freq_df = pd.DataFrame({
        'itemset': [' + '.join(sorted(k)) for k in freq_items],
        'support': [v / n for v in freq_items.values()]
    })
    return freq_df, rules
