import csv
import statistics as st


def goodData(filename):
        """
        Analizes the input CSV file accordingly with correct values and counts null and error values.
        
        The first iteration shows all titles on header and waits for user answer about which
        title must be used for a dictionary key and which ones for respective values.
        
        Returns a dictionary on the form {key:[values]}.
        """
        dBuild = {}
        
        # User interface to define which data must be handled with
        with open(filename, 'r', newline='') as csvfile:
            rows = csv.DictReader(csvfile, delimiter=',')
            header = rows.fieldnames

        print(" The current file has the following names as headers:")
        for k in range(0, len(header)):
            print("\t({}) {}".format(k, header[k]))
        
        try:
            key = int(input("\n Type the value that you'd like to use as key: "))
        except ValueError:
            print ("Check if you have typed only numbers.")

      
        values = []
        while values == []:
            val = input("\n Type the values that you'd like to correlate with a key separated by commas: ")
            
            for v in val:
                try:
                    saV = int(v)
                    if (saV != key) and (saV not in values) and (saV < len(header)-1):
                        values.append(saV)
                    if saV > len(header)-1 :
                        print(v, "must be lesser than or equal to", len(header)-1)
                except ValueError:
                    pass

        print(values,"\n")
        
        countNull = {'nC':[], 'nH':[], 'nA':[], 'n3':[]}
        highIssues = {'neg':[], 'pos':[], 'eq':[]}
        count_Errors = 0

        with open(filename, 'r') as csvfile:
            ROWS = csv.reader(csvfile, delimiter=',')
            for r in 0:#ROWS:

                # checking blank data
                if r[5] == '':
                    countNull['nC'].append(r[0])
                if r[4] == '':
                    countNull['nH'].append(r[0])
                if r[10] == '':
                    countNull['nA'].append(r[0])
                if (r[4] == '') and (r[5] == '') and (r[10] == ''):
                    countNull['n3'].append(r[0])

                try:
                    key = int(r[5])

                    if r[4] == '':
                        # check if 'base' > 'topo' --> raise ValueError if convertion to float doesn't work --> but WHY?
                        if float(r[2]) > float(r[3]):
                            highIssues['neg'].append(r[0])
                        elif float(r[2]) < float(r[3]):
                            highIssues['pos'].append(r[0])
                        else:
                            highIssues['eq'].append(r[0])
                        height = 0

                    else: height = float(r[4])

                    if r[10] == '': area = 0
                    else: area = float(r[10])

                    dBuild[ key ] = [ height, area ]

                except ValueError:
                    # values that we don't care
                    # if r[5], r[4] or r[10] is the header
                    # if r[5] is empty
                    count_Errors += 1
                    pass

        if True: # fast trick to pass print
            print("# of blank values:")
            for k in countNull: print("\t" + str(k) + ":", len(countNull[k]))
            print('# of height "blank" values:')
            for k in highIssues: print("\t" + str(k) + ":", len(highIssues[k]))
            print("# of errors:", count_Errors, "\nsize of dataset:", len(dBuild))

            x = 5
            for k in dBuild:
                if x == 5: break
                x += 1
                print(k, ":", dBuild[k])

        return dBuild


class Stats():
    def __init__(self, dBuild):
        """
        Initializes the class Statistics.

        Returns nothing.
        """
        self.dBuild = dBuild

        return None


    def get_sample(self, i):
        """
        Extracts sample data from dictionary accordingly with indice 'i'.

            - 'dBuild' has the form {key:[value1, value2, ..., valueN]}
            - the parameter 'i' indicates the position of a value on each
            key list, varying from 0 to N-1

        Returns a list of floats.
        """
        sample = []

        for s in self.dBuild.values():
            sample.append( s[i] )

        return sample


    def limits(self, sample):
        """
        Returns a tuple with minimum and maximum of a sample.
        """
        return  min(sample), max(sample)


    def centrals(self, sample):
        """
        Returns central values of a sample, i.e. mean(average), median and mode.
        """
        return st.mean(sample), st.median(sample), st.mode(sample)


    def spreads(self, sample, mean):
        """
        Returns distribution values of a sample, i.e. variance and deviation.
        """
        return st.variance(sample, mean), st.stdev(sample, mean)


    def summary(self):
        """
        Shows a summary of the corresponding file.
        
        Returns nothing.
        """        
        for k in range( 0, len( list( self.dBuild.values() )[0] ) ):

            sample = self.get_sample(k)
            centValues = self.centrals(sample)
            sprValues = self.spreads(sample, centValues[0])
            limtValues = self.limits(sample)
            statValues = centValues + sprValues + limtValues

            print( k, "\n\taverage: %5.3f,\n\tmedian: %5.3f,\n\tmode: %5.3f,\n\tvariance: %5.3f,\n\tdeviation: %5.3f,\n\tlimits = ( %5.3f , %5.3f )\n" % statValues )
        #    print( k, "-->", "average: {}, median: {}, and mode: {}" .format(centrals(y,lib[k])) ) % best way to print out, but not working... :(
        
        return None
        
        
#----------------------------------------------------------------

# extract valuable data
y = goodData("edific.csv")

#analize = Stats(y)
#analize.summary()
