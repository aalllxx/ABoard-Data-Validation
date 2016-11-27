#create a sheet reader

def validateRA(raList):
    output = ""
    count = 0 #keeps track of all whole RA things
    
    raDenied = 0
    raComment = 0  
    request = 0
    for row in raList:
        count = count + 1    
        
        if row[13] == 'request': #lump sum
            request = request + 1
        if not row[17] == '': #RA Comment in middle of RA
            raComment = raComment + 1
        if row[5] == 'TRUE': #RA Denied in middle of RA
            raDenied = raDenied + 1    
            
        if row[5] == 'TRUE' and row[6] == '': #has denied reason RA
            output += "RA: {} - no RA Denied reason\n".format(row[3])
        if row[7] == 'TRUE' and row[8] == '': #has denied reason RAItem
            output += "RA: {} - no RA Denied item reason\n".format(row[3])
        if (row[5] == 'TRUE' or row [7] == 'TRUE') and float(row[15]) > 0: #denied raItem value is set to 0
            output += "RA: {} - RA denied, but amount not set to zero\n".format(row[3])
            
        if row[11] != row [15]: #if partially denied
            if row[17] == '' and row[18] == '': #check for comment
                output += "RA: {} - item denied and no comment\n".format(row[3])
            if row[15] == 0 and not(row[5] or row[7] or row[13] == "request"): #if value is zero, check for denied
                output += "RA: {} - item is zero but not denied\n".format(row[3])
                
        if request > 0 and float(row[15]) != 0: #lump sum zero's raItem
            if count != len(raList):
                output += "RA: {} - lump sum, but RA Item not set to 0\n".format(row[3])
        
        if row[13] == 'request item':
            if row[14] != row[16]:
                output += "RA: {} - not lump sum but RA Allocated not full\n".format(row[3])
        elif row[17] == '': #lump sum
            output += "RA: {} - lump sum but missing comment\n".format(row[3])

            
    if raDenied > 0 and raDenied != len(raList):
        output += "RA: {} - RA Denied on some items but not all\n".format(row[3])
    
    if raComment > 0 and raComment != len(raList):
        output += "RA: {} - RA comment on some items but not all\n".format(row[3])
    
    if request > 0 and request != len(raList):
        output += "RA: {} - Lump sum on some items but not all\n".format(row[3])
        if float(row[15]) != float(row[14]):
            output += "RA: {} - Lump sum amount not in raItem column\n".format(row[3])
        
    return output

def main():
    with open('/Users/Alex/Desktop/SampleCSV.csv', encoding='UTF-8') as csvFile:
        spreadRead = csvFile.readlines()
        writeLocation = '/Users/Alex/Desktop/errors.txt'
        spreadWrite = open(writeLocation, 'w')
        count = 0
        numInRA = 0
        curRA = 0
        raList = list()
        for row in spreadRead:
            if count > 0:
                rowList = row.split(',')
                if rowList[3] == curRA:
                    raList.append(rowList) #add row to RA List
                    numInRA += 1
                else: #new RA
                    #send old RA to validation
                    if numInRA > 0:
                        erMessage = validateRA(raList)
                        spreadWrite.write(erMessage)

                    #write errors which return
                    
                    #start new RA List

                    numInRA = 1
                    curRA = rowList[3]
                    raList = list()
                    raList.append(rowList)
                                          
            count = count + 1
        spreadWrite.close()
        print ("Validation done. Report at {}".format(writeLocation))

main()