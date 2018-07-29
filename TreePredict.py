# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 15:08:51 2018

@author: zy
"""

class decisionnode:
    def __init__(self,col=-1, value=None, results=None, tb=None, fb=None):
        """
        col 待检验的判断条件
        value 为使得结果为true，当前列必须匹配的值
        """
        self.col = col
        self.value=value
        self.results=results
        self.tb = tb
        self.fb = fb
        
    def divideset(rows, column, value):
        split_function = None
        if isinstance(value, int) or isinstance(value, float):
            split_function = lambda row : row[column] >= value
        else:
            split_function = lambda row: row[column] == value
        set1 = [row for row in rows if split_function(row)]
        set2 = [row for row in rows if not split_function(row)]
        
        return set(set1, set2)
    
    def uniquecounts(rows):
        results = {}
        for row in rows:
            r = row[len(row)-1]
            if r not in results: results[r] =0
            results[r] += 1
        
        return results
    
    def giniimpurity(rows):
        total = len(rows)
        counts = uniquecounts(rows)
        imp = 0
        for k1 in counts:
            p1 = counts[k1]/total
            for k2 in counts:
                if k1==k2: continue
                p2 = counts[k2]/total
                imp += p1*p2
        
        return imp
    
    def entropy(rows):
        from math import log2
        results = uniquecounts(rows)
        ent = 0
        for r in results.keys():
            p = results[r]/len(rows)
            ent = ent - p*log2(p)
            
        return ent
            
    def buildtree(rows, scoref=entropy):
        if len(rows)==0:
            return decisionnode()
        current_score = scoref(rows)
        best_gain = 0
        best_criteria = None
        best_sets = None
        column_count = len(rows[0]) - 1
        for col in range(0, column_count):
            column_values = {}
            for row in rows:
                column_values[row[col]] = 1
        for value in column_values.keys():
            (set1, set2) = divideset(rows, col, value)
            p = len(set1)/len(rows)
            gain = current_score - p* scoref(set1) - (1-p)*scoref(set2)
            if gain> best_gain and len(set1)>0 and len(set2)>0:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)
        if best_gain > 0:
            trueBranch = buildtree(best_sets[0])
            falseBranch = buildtree(best_sets[1])
            return decisionnode(col=best_criteria[0], value=best_criteria[1],\
                    tb=trueBranch, fb = falseBranch)
        else:
            return decisionnode(results = uniquecounts(rows))

        
                
    
   

