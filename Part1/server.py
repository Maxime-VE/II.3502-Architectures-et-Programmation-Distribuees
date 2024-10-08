from xmlrpc.server import SimpleXMLRPCServer

def add(x, y):
	return x + y

def sub(x, y):
    return x - y

def multiply(x,y):
    return x*y

def divide(x,y):
    try:
        return x / y
    except:
        return "error"
        print("error while using substract function")

def matrixmul(X,Y):
    for i in range(len(X)):
        for j in range(len(Y[0])):
            for k in range(len(Y)):
                result[i][j] += X[i][k] * Y[k][j]
    return result

try:
    print("hello start")
    server = SimpleXMLRPCServer(("localhost", 5080))
    server.register_function(add, 'add')
    server.register_function(sub, 'sub')
    server.register_function(multiply, 'multiply')
    server.register_function(divide, 'divide')
    server.register_function(matrixmul,'matrixmul')
    server.serve_forever()

except:
    print("end of the server, he knew too much")