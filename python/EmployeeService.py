from concurrent import futures
import logging

import grpc
import EmployeeService_pb2
import EmployeeService_pb2_grpc

class EmployeeServer(EmployeeService_pb2_grpc.EmployeeServiceServicer):
  
  value=[]

  def InsertValue(self, request, context):
    data = request.number
    self.value = self.value + [data]
    return EmployeeService_pb2.StatusReply(status="OK")

  def SearchValue(self, request, context):
    data = request.number
    if data in self.value: 
      return EmployeeService_pb2.StatusReply(status="OK")
    else:
      return EmployeeService_pb2.StatusReply(status="NOK")

  def RemoveValue(self, request, context):
    data = request.number
    self.value.remove(data)
    return EmployeeService_pb2.StatusReply(status="OK")

  def ReturnList(self, request, context):
    list = EmployeeService_pb2.ValueList()
    for item in self.value:
      value_data = EmployeeService_pb2.Value(number=item) 
      list.number_data.append(value_data)
    return list

  def SortAscending(self, request, context):
    self.value.sort()
    return EmployeeService_pb2.StatusReply(status="OK")

  def SortDescending(self, request, context):
    self.value.sort(reverse=True)
    return EmployeeService_pb2.StatusReply(status="OK")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    EmployeeService_pb2_grpc.add_EmployeeServiceServicer_to_server(EmployeeServer(), server)
    server.add_insecure_port('[::]:5678')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()