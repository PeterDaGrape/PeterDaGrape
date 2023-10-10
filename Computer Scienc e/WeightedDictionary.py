weightedGraph = {'A' : {'B' : 5, 'D' : 8, 'E' : 4},
                 'B' : {'A' : 5, 'C' : 4},
                 'C' : {'B' : 4, 'D' : 5, 'G' : 2},
                 'D' : {'A' : 8, 'C' : 5, 'E' : 7, 'F' : 6},
                 'E' : {'A' : 4, 'D' : 7},
                 'F' : {'D' : 6},
                 'G' : {'C' : 2}


                 }

print(list(weightedGraph['C']))