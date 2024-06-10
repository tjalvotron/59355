# Made by tjalvotron
print('Made by tjalvotron')

import datetime

# reads a file and returns list of lists of lines in the file
def read(file_path): 
    try:
        l = []
        with open(file_path, 'r') as file:
            for line in file:
                x = line.strip().split('|')
                l.append(x)
        return l
    except Exception as e:
        print('not reading: ', e)
    
# takes list and saves it in a file
def save(m,file_path):
    n=s(m)
    with open(file_path, 'a') as file:
        file.write(n)

# takes varible and makes str to save in file
def s(m):
    n = ''
    t=type(m)
    print(t)
    if isinstance(m,list) or isinstance(m,tuple):
        n = str(m[0])
        try:
            for i in range(len(m)-1):
                n = n + ('|' + str(m[i+1]))
        except:
            pass
        n = n + ('\n')
    elif isinstance(m,str) or isinstance(m,int) or isinstance(m,float) or isinstance(m,bool):
        n = m
    print(n)
    return n

# uses list of lists/info and makes a new file whith it (if file already exists it gets owerwriten)
def save_man(m,file_path):
    with open(file_path, 'w') as file:
        for i in m:
            n = s(i)
            print(n)
            file.write(n)

# returns the Name of the RFID number refrencing a file
def read_man(id,file_path): 
    try:
        with open(file_path, 'r') as file:
            for line in file:
                x = line.strip().split('|')
                if str(x[1]) == str(id):
                    return x[0]
    except Exception as e:
        print('not reading: ', e)
        
# looks if the RFID number is in the file and returns 1(True) if found
def in_man(id,file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                x = line.strip().split('|')
                if str(x[1]) == str(id):
                    return 1
    except Exception as e:
        print('not reading: ', e)
    
# returns if the RFID number is going to check ind or ud next
def next_Ind_Ud(id,file_path):
    try:
        l = read(file_path)
        c = 1
        ind = 0
        ud = 0
        x = 'Ind'
        v = ""
        for i in l:
            if str(i[1]) == str(id):
                # saves first Ind/Ud for id
                if c:
                    c = 0
                    v = i[2]
                if i[2] == "Ind":
                    ind += 1
                elif i[2] == "Ud":
                    ud += 1
        # use saved first Ind/Ud to select right prosidure 
        if v == "Ind":
            if ind>ud:
                x = "Ud"
            else:
                x = "Ind"
        elif v == "Ud":
            if ind>=ud:
                x = "Ud"
            else:
                x = "Ind"
        return x
    except Exception as e:
        print('no last:',e)
        return 'Ind'

# controls that all RFID number in the files have "Ud" as their last log and sets all remaining RFID numbers to "Ud"
def all_out(file_path,file_path_old):
    l = read(file_path)
    j = read(file_path_old)
    n = []
    for i in l:
        if i[1] not in n:
            n.append(i[1])
    for i in j:
        if i[1] not in n:
            n.append(i[1])
    print("all_out:",n)
    for i in n:
        now_time = str(datetime.datetime.now())
        if next_Ind_Ud(i,file_path) == "Ud":
            save((now_time,i,"Ud"),file_path)
        if next_Ind_Ud(i,file_path_old) == "Ud":
            save((now_time,i,"Ud"),file_path)
            save((now_time,i,"Ud"),file_path_old)

# clears the file
def clear_file(file_path):
    open(file_path, 'w').close()

# shows file content
def show(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                x = line.strip().split('|')
                print('Time:',x[0],'ID:',x[1],x[2])
    except Exception as e:
        print('not showing: ', e)

# used to test code on its own and manual controal
def test(id=0,i_o=0):
    file_path = '/home/test/Desktop/ProjektB/Logs/Brandtest.txt' #put your file path here
    while True:
        m = []
        try:
            x = int(input('Enter a number (#1 to show, #9 to clear, other to save, #0 to exit): '))
            if x == 1:
                show(file_path)
            elif x == 9:
                clear_file(file_path)
                print("File cleared.")
            elif x == 0:
                print("Exiting...")
                break
            else:
                now_time = str(datetime.datetime.now())
                now_time = now_time[:now_time.find('.')]
                m.append(now_time)
                if id:
                    m.append(id)
                else:
                    m.append(input('id: '))
                if i_o:
                    m.append(i_o)
                else:
                    m.append(input('Ind/Ud: '))
                save(m)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == '__main__': test()
