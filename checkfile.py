import csv

class CSVanalyzer:

    def __init__(self, filename):
        """
        Just sets CSV file to be used by methods once.
        """
        self.csv = filename


    def checkSize(self):
        """
        Counts the number of rows and print it.
        """
        with open(self.csv, 'r') as csvfile:
            ROWS = csv.reader(csvfile, delimiter=',')
            
            count = 0
            for row in ROWS:
                count += 1

        return print(count)


    def getTitles(self):
        """
        Shows off the title of each column. (REFAZER DEPOIS)
        """
        with open(self.csv, 'r') as csvfile:
            l = csv.list_dialects()

        for title in l:
            print(title)

        return None


    def dIDs(self):
        """
        Shows off the difference between number of rows and its ID number.
        """
        rowNum = 0
        rowID = [['rowID','rowNum','falta(m)']]
        countDiffs = 0

        with open(self.csv, 'r') as csvfile:
            ROWS = csv.reader(csvfile, delimiter=',')
            for r in ROWS:                    
                if (rowNum > 0) and (r[0] != str(rowNum)):
                    countDiffs += 1
                    dif = abs(rowNum - int(r[0]))
                    rowID.append([r[0], rowNum, dif])
                    rowNum += 1 + dif
                else:
                    rowNum += 1

        print("diffs:", countDiffs, "rowNum:", rowNum-1)
        for k in rowID[0:10]: print(k)

        return None


    def dCods(self):
        """
        Shows off the difference between number of rows and the unique building codes.

        Returns a dictionary of building codes as keys, but with no values.
        """
        cod = []
        noNum = 0

        with open(self.csv, 'r') as csvfile:
            ROWS = csv.reader(csvfile, delimiter=',')
            for r in ROWS:
                try:
                    temp = int(r[5])
                    cod.append(temp)
                except:
                    noNum += 1
                    pass

        p = False # fast trick to pass print
        if p:
            misNum = []
            x = sorted(cod)
            for k in range(len(x)):
                if k > 1 and abs( x[k] - x[k-1] ) > 1:
                 misNum.append( x[k] - x[k-1] )

            print('Missing numbers:', len(misNum), '(buildings not considered on map)')
            print('No valid inputs:', noNum, '(not buildings)')
            print('Valid inputs:', len(cod), '(all types of roof surface)')

        dBuild0 = {}
        for n in cod:
            dBuild0[n] = 0
#            if n not in dBuild0:
#                dBuild0[n] = 1
#            else:
#                dBuild0[n] += 1

#        for j in dBuild0.values():
#            if j > 1:
#                print('Duplicated!')

        p = False # fast trick to pass print
        if p:
            c = 0
            for i in misNum:
                if c == 10:
                    print("\n")
                    c = 0
                print(i, "| ", end="")
                c += 1

        return dBuild0


    def fillBuild(self):
        """
        Populates the dictionary of building codes with height and area
        in the form of list values arranged by pairs.

        Returns a dictionary of buildings with unique code as key and a
        pair list of height and area as value.
        """
        dBuild = self.dCods()

        with open(self.csv, 'r') as csvfile:
            ROWS = csv.reader(csvfile, delimiter=',')
            for r in ROWS:
                try:
                    temp = int(r[5])
                    if temp in dBuild:
                        dBuild[temp] = [ int(r[4]), int(r[10]) ]
                except:
                    pass
        
        return dBuild


    # count = 1574073 --> diferença de 1203 com o arquivo base
    #                 --> o somatório das diferenças entre índices dá 1204
    #                 --> i.e. rowID é diferente do número de linhas

    # diffs1 = 1400451 --> com header
    # diffs2 = 1400450 --> sem header
    # diffs3 = 9 --> sem header e correção dos índices

    #rowNum = 1575276 --> com header e valores esquisitos (BASE)
    #rowNum = 1574052 --> com header e sem valores esquisitos
    #rowNum = 1574051 --> sem header e sem valores esquisitos

    #cod = 1574049 --> identificação de edifícios (número de linhas, menos header e linhas nulas)

    #      1574050

# inheritance class
class freqDist(CSVanalyzer):

    def rolH(self):
        """
        STEP 1

        returns:
                - max and min of a dataset
                - rol height
        """
        
        dataset = self.fillBuild()
        i = 0
        for x in dataset.values():
            if i == 5: break
            i += 1
            print(x)

        Heights = []
        Areas = []

#        for k in dataset.values():
#            Heights.append(k[0])
#            Areas.append(k[1])

        p = False # fast trick to pass print
        if p:
            print("[", min(Heights), "< h <", max(Heights), "]", "rol =", max(Heights)-min(Heights))
            print("[", min(Areas), "< A <", max(Areas), "]", "rol =", max(Areas)-min(Areas))

        return None#(max() - min())


# --------------------------------------------------------------
# Test Environment

f = freqDist('edific.csv')

# (1)
#f.checkSize()

# (2)
#f.getTitles()

# (3) Linhas faltantes
#f.dIDs()

# (4) Contagem de edificações
#f.dCods()

# (5) Distribuição de frequências
f.rolH()
