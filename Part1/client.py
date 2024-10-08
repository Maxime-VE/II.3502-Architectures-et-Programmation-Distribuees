import xmlrpc.client
try :
    with xmlrpc.client.ServerProxy("http://localhost:5080/") as proxy:
        x = 6
        y = 0
        X = [[2,5,7],
             [5,7,3],
             [1,2,3]]
        Y = [[11,4,5],
             [3,5,7],
             [4,2,21]]
        print(f"sum of {x} + {y}: %s" % str(proxy.add(x, y)))
        print(f"sub of {x} - {y} is: %s" % str(proxy.sub(x, y)))
        print(f"multiple of {x} * {y} is: %s" % str(proxy.multiply(x, y)))
        print(f"division of {x} / {y} is: %s" % str(proxy.divide(x, y)))
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in X]))
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in Y]))
        Z = proxy.matrixmul(X,Y)
        print("alors : ",len(Z[0]))
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in Z]))

except:
    print("cannot connect to server")
