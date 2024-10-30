import grpc
import calcul_pb2
import calcul_pb2_grpc
def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calcul_pb2_grpc.CalculServiceStub(channel)

        try:
            #Add
            response = stub.add(calcul_pb2.numbersReq(number1=1,number2=18))
            print(f"add: {response}")
            #Substract
            response2 = stub.substract(calcul_pb2.numbersReq(number1=1,number2=18))
            print(f"sub: {response2}")
            #Multiply
            response3 = stub.multiply(calcul_pb2.numbersReq(number1=3, number2=3))
            print(f"multiply: {response3.resultat}")
            #Divide
            response4 = stub.divided(calcul_pb2.numbersReq(number1=10, number2=3))
            print(f"divide: {response4.resultat}")

            try:
                # Division by 0 try
                response4 = stub.divided(calcul_pb2.numbersReq(number1=10, number2=0))
                print(f"divide: {response4.resultat}")

            except grpc.RpcError as e:
                print(f"Error in division: {e.details()}")
            
        except grpc.RpcError as e:
            print(f"Error: {e.details()}")
        
if __name__ == '__main__':
    run()