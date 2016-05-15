import numpy as np
import itertools
import matplotlib.pyplot as plt


def readData(fileName):
    '''
    Read data from input file, calculate p2p performance
    performace = (p2p download*100/(p2p download + cdn download))
    '''
    
    f = open(fileName,'r')
    data = [line.rstrip().split(",") for line in f][1:]
    f.close()

    for i in range(len(data)):
        performance = round(float(data[i][4])*100/(float(data[i][4])+float(data[i][5])),2)
        data[i].append(performance)
    return data

def outputFile(data,fileName,title):
    '''
    Output data to csv file
    '''
    
    file = open(fileName,"w")
    file.write(title)
    
    for i in range(len(data)):
        raw = ""
        for j in range(len(data[i])):
                raw = raw + str(data[i][j])
                if j!=len(data[i])-1:
                    raw = raw + ","
        raw = raw + "\n"
        file.write(raw)
    file.close()

def plotHistogram(data,respectColumn,dataColumn):
    '''
    Plot performance histogram according to repectComumn
    '''

    #Set chart title according to repectComumn 
               
    if respectColumn == 0:
            orignalTitle = "Performance of stream "
    elif respectColumn == 1:
        orignalTitle = "Performance of isp "
    elif respectColumn == 2:
        orignalTitle = "Performance of browser "
    else:
        orignalTitle = ""
         
    #Get disctinc value in respectColumn
    respectValues = list(set([da[respectColumn] for da in data]))
    respectValues.sort()

    #Plot performance histogram for each disctinc value in respect column.
    bins = np.linspace(0, 100, 10)
    NoOfFigure = 1
    NoOfSubFigure =0
    
    dataValues = [[] for i in range(len(respectValues))]

    for i in range(len(respectValues)):
        #Each figure includes 4 subplots
        NoOfSubFigure += 1
        if NoOfSubFigure == 1:
            NoOfFigure += 1
            plt.figure()
        splot = plt.subplot(2, 2, NoOfSubFigure)
    
        dataValues[i] =  [float(elem[dataColumn]) for elem in data if elem[respectColumn] == respectValues[i] ]
        n, bins, patches = plt.hist(dataValues[i], bins=10, weights=np.zeros_like(dataValues[i]) + 1. / len(dataValues[i]))
        bin_centers = 0.5 * (bins[:-1] + bins[1:])
        col = bin_centers - min(bin_centers)
        col /= max(col)
               
        #Set color for bars: 
        #red: performance < 50%,green: performance >= 50%
        for c, p in zip(col, patches):
            if c <= 0.5:
                plt.setp(p, 'facecolor', 'red')
            else:
                plt.setp(p, 'facecolor', 'green')
               
        title = orignalTitle + str(respectValues[i])
        plt.xlim(0,100)
        plt.ylim(0,1)
        plt.title(title)
        if NoOfSubFigure==4:
            NoOfSubFigure = 0

    #plt.show()
    
def createTable(data):
    '''
    Create Metric table per each streams
    '''
    #Get stream list
    streams = list(set([da[0] for da in data]))
    streams.sort()
    #Get isps list
    isps = list(set([da[1] for da in data]))
    isps.sort()
    #Get browser list
    browsers = list(set([da[2] for da in data]))    
    browsers.sort()
               
    row = [[] for i in range(len(streams))]
    count = 0
    for stream in streams:
        #Number of users
        noOfSession=(len([da for da in data if da[0]==stream]))
               
        #User percentage for each isp
        isp = [0 for i in range(len(isps))]
        for i in range(len(isps)):
            isp[i] = round(len([da for da in data if da[0]==stream and da[1]== isps[i]])*100/noOfSession,2)

        #User percentage for each browser
        browser = [0 for j in range(len(browsers))]
        for i in range(len(browsers)):
            browser[i] = round(len([da for da in data if da[0]==stream and da[2]== browsers[i]])*100/noOfSession,2)

        #Total exchanged data
        totalExchange = round(sum((float(da[4])+ float(da[5])) for da in data if da[0]==stream ),2)
               
        # Average performance
        pAverage = round(np.mean([da[6] for da in data if da[0]==stream]),2)

        # Number of false connection     
        unConnected = (len([da for da in data if da[0]==stream and da[3]=='FALSE']))

        row[count].append(stream)
        row[count].append(noOfSession)
        row[count].extend(isp)
        row[count].extend(browser)
        row[count].append(unConnected)
        row[count].append(totalExchange)
        row[count].append(pAverage)
        count +=1
        
    return row
    


if __name__=='__main__':
               
               #Read data from input file
               data = readData('data.csv')
               #Create summary metric
               metric = createTable(data)
               fileTitle = "stream,No of session, isp_arrange,isp_btp,isp_datchTelecom,isp_Fro,isp_olga,browser_earthworf,browser_iron,browser_swamp,browser_vectrice,un connected,total exchange,performance average \n"
               outputFile(metric,'summary.csv',fileTitle)
               #Plot performance histogram respect to stream
               plotHistogram(data,0,6)
               #Plot performance histogram respect to internet service provider
               plotHistogram(data,1,6)
               #Plot performance histogram respect to browser
               plotHistogram(data,2,6)
               plt.show()
               
