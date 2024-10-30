from concurrent import futures
import grpc
import calcul_pb2
import calcul_pb2_grpc
class CalculService(calcul_pb2_grpc. CalculServiceServicer):
    def add(self, request, context):
        res = calcul_pb2.numberRes(resultat=request.number1 + request.number2)
        return res
    
    def substract(self, request, context):
        res = calcul_pb2.numberRes(resultat=request.number1 - request.number2)
        return res

    def multiply(self, request, context):
        res = calcul_pb2.numberRes(resultat=request.number1 * request.number2)
        return res

    def divided(self, request, context):
        if request.number2 == 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Division by 0 is not supported.')
            return calcul_pb2.numberRes(resultat=0)
        res = calcul_pb2.numberRes(resultat=request.number1 / request.number2)
        return res



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calcul_pb2_grpc.add_CalculServiceServicer_to_server(CalculService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()
    
if __name__ == '__main__':
    serve()