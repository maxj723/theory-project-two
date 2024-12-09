from traceTM_MJ import NTM, process_csv

def __main__():
    aplus = process_csv('check_MJ/a_plus.csv')

    #TEST 1 - basic input and working capabilities
    print('TEST 1')
    aplus.process_input('a', 5) #accept
    print()
    print()

    #TEST 2 - invalid input
    print('TEST 2')
    aplus.process_input('b', 5) # reject
    print()
    print()
    
    #TEST 3 - max depth exceeded
    print('TEST 3')
    aplus.process_input('aaaaaa', 5) # max depth exceeded
    print()
    print()
    
    #TEST 4 - longer input
    print('TEST 4')
    aplus.process_input('aaaaaaaaaaaa', 50) # accept
    print()
    print()
    
    # TEST 5 - other
    print('TEST 5')
    aplus.process_input('aaaabaa', 50)
    print()
    print()
    
if __name__ == '__main__':
    __main__()