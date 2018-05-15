import csv
import statistics as st


def goodData(filename):
        """
        Returns a dictionary of building codes as keys with height and area as values.
        """
        dBuild = {}
        countNull = {'nC':[], 'nH':[], 'nA':[], 'n3':[]}
        highIssues = {'neg':[], 'pos':[], 'eq':[]}
        count_Error = 0

        with open(filename, 'r') as csvfile:
            ROWS = csv.reader(csvfile, delimiter=',')
            for r in ROWS:

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
                    count_Error += 1
                    pass

        if True: # fast trick to pass print
            print("# of blank values:")
            for k in countNull: print("\t" + str(k) + ":", len(countNull[k]))
            print('# of height "blank" values:')
            for k in highIssues: print("\t" + str(k) + ":", len(highIssues[k]))
            print("# of errors:", count_Error, "\nsize of dataset:", len(dBuild))

            x = 5
            for k in dBuild:
                if x == 5: break
                x += 1
                print(k, ":", dBuild[k])

        return dBuild


def get_sample(dBuild, i):
    """
    extract sample data from dictionary accordingly with indice i
    """
    samp = []

    for s in dBuild.values():
        samp.append( s[i] )

    return samp
    

def lims(sample):
    """
    min and max of a sample
    """
    return  min(sample), max(sample)


def centrals(sample):
    """
    mean (average), median and mode
    """
    return st.mean(sample), st.median(sample), st.mode(sample)


def spreads(sample, mean):
    """
    variance and deviation
    """
    return st.variance(sample, mean), st.stdev(sample, mean)
    

#----------------------------------------------------------------

# extract vauable data
y = goodData("edific.csv")


lib = []#{"HEIGHT":0, "AREA":1}
for k in lib:

    sample = get_sample(y,lib[k])
    
    # analyzing the need of stratification
    centValues = centrals(sample)
    sprValues = spreads(sample, centValues[0])

    # defining limits
    limtValues = lims(sample)

    statValues = centValues + sprValues + limtValues
    print( k, "\n\taverage: %5.3f,\n\tmedian: %5.3f,\n\tmode: %5.3f,\n\tvariance: %5.3f,\n\tdeviation: %5.3f,\n\tlimits = ( %5.3f , %5.3f )\n" % statValues )

#    print( k, "-->", "average: {}, median: {}, and mode: {}" .format(centrals(y,lib[k])) ) % best way to print out, but not working... :(
