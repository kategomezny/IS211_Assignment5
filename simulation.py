#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simulation with One and multiple Servers"""

import urllib2
import csv

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

# Completed program for the printer simulation
    
class Server(object):
    def __init__(self, ppm):
        self.page_rate = ppm
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_process_time() * 60/self.page_rate

class Request:
    def __init__(self, time, processing_time):
        self.timestamp = time
        self.process_time = processing_time

    def get_stamp(self):
        return self.timestamp

    def get_process_time(self):
        return self.process_time

    def wait_time(self, current_time):
        return current_time - self.timestamp
def simulateOneServer(My_File):

    
    Main_Server = Server(60)
    print_queue = Queue()
    waiting_times = []
 
    for row in My_File:
        new_server_Request = Request(int(row[0]),int(row[2]))
            
        print_queue.enqueue(new_server_Request)

        if (not Main_Server.busy()) and (not print_queue.is_empty()):
            next_task = print_queue.dequeue()
            waiting_times.append(next_task.wait_time(int(row[0])))
            Main_Server.start_next(next_task)
        
        Main_Server.tick()
    
    average_wait = sum(waiting_times) / len(waiting_times)
    print("Single Server:Average Wait %6.2f secs %3d tasks remaining."%(average_wait, print_queue.size()))

def simulateManyServers(My_File, total_servers):

    Servers_List=[]
    for i in range(total_servers):
         Servers_List.append(Server(60))
         
    print_queue = Queue()
    waiting_times = []

    server_count=0
    
    for row in My_File:
        
        new_server_Request = Request(int(row[0]),int(row[2]))

            
        print_queue.enqueue(new_server_Request)

        if (not Servers_List[server_count].busy()) and (not print_queue.is_empty()):
            next_task = print_queue.dequeue()
            waiting_times.append(next_task.wait_time(int(row[0])))
            Servers_List[server_count].start_next(next_task)
        
        Servers_List[server_count].tick()
        if server_count==total_servers-1:
           server_count=0
        else:
           server_count=server_count+1 
            
    average_wait = sum(waiting_times) / len(waiting_times)
    print("Multiple Servers("+str(total_servers)+"): Average Wait %6.2f secs %3d tasks remaining."%(average_wait, print_queue.size()))

  

def main(__file, __servers=1):
    req = urllib2.Request(__file)
    response = urllib2.urlopen(req)
    reader= csv.reader(response)
    if __servers>1:
        simulateManyServers(reader, __servers)
    else:
        simulateOneServer(reader)
  

        
if __name__ == "__main__": 
    main('http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv',3)
