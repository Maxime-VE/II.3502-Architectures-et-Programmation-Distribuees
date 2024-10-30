import grpc
import book_pb2
import book_pb2_grpc
def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = book_pb2_grpc.BookServiceStub(channel)

        # Get a single book by ID
        try:
            response = stub.GetBook(book_pb2.BookRequest(id=1))
            print(f"Book: {response.book.title} by {response.book.author}")
        except grpc.RpcError as e:
            print(f"Error: {e.details()}")
        
        # List all books
        books = stub.ListBooks(book_pb2.Empty())
        for book in books.books:
            print(f"Book: {book.title} by {book.author}")
        # Add a new book
        new_book_response = stub.AddBook(book_pb2.NewBookRequest(title="Brave New World", author="Aldous Huxley"))
        print(f"Added Book: {new_book_response.book.title} by {new_book_response.book.author}")
if __name__ == '__main__':
    run()