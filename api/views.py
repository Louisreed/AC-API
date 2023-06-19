# import os
# from django.shortcuts import render
# from rest_framework.decorators import api_view
from .serializers import ErrorLogSerializer, UpdateCheckSerializer, FirmwareSerializer, UserSerializer, GroupSerializer
from django.contrib.auth.models import User, Group
from .models import ErrorLog, UpdateCheck, Firmware
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
import re, os, zlib, csv, math
from .serializers import UserSerializer, GroupSerializer, ErrorLogSerializer, UpdateCheckSerializer, FirmwareSerializer

"""
Variables
"""

chunk_size = int(settings.CHUNK_SIZE)
filename = settings.FILENAME
filename_rollback = settings.FILENAME_ROLLBACK
header = settings.HEADER


"""
Helpers
"""

def get_file_size(size_bytes):
    """
    Convert the given number of bytes to a human-readable format (e.g., KB, MB, GB).
    """
    if size_bytes == 0:
        return "0B"  # Special case

    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return "{:.2f} {}".format(size_bytes, size_names[i])


def get_file_chunks(firmware_file, chunk_size):
    """
    Returns a list of chunks from the given firmware file, where each chunk
    is chunk_size bytes long (except possibly the last one).
    """
    chunk_list = []
    firmware_file_path = firmware_file.path
    
    with open(firmware_file_path, mode='rb') as f:
        chunk = f.read(chunk_size)
        chunk_list.append(chunk)
        while chunk:
            chunk = f.read(chunk_size)
            if chunk:
                chunk_list.append(chunk)
    return chunk_list


def get_number_of_chunks(firmware_file, chunk_size):
    file_size = get_file_size(firmware_file)
    
    num_chunks = file_size / chunk_size
    
    return num_chunks


def add_checksum_to_packet(packet):
    numbers = [packet[i] for i in range(0, len(packet))]
    checksum = zlib.crc32(packet).to_bytes(4, 'little')
    checksum_list = [checksum[i] for i in range(0, len(checksum))]
    for item in checksum_list:
        numbers.append(item)
    packet_w_checksum = bytes(numbers)
    return packet_w_checksum


def get_file_chunks_with_checksums(firmware_file, chunk_size):
    byte_list = []
    byte_list = get_file_chunks(firmware_file, chunk_size)
    packet_n_checksum = []
    for packet in byte_list:
        packet_n_checksum.append(add_checksum_to_packet(packet))
        
    return packet_n_checksum


def create_file(directory, datafile):
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    with open(datafile, "w+", newline='\n', encoding='utf-8', buffering=1) as f:
        f.write(header)
        f.write('\n')
        f.flush()
        
    return {
        'directory_created': directory,
        'file_created': datafile
    }
        
        
def update_file(datafile,line):
    with open(datafile, "a", newline='\n', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(line)
        f.write('\n')
        f.flush()
        
    return {
        'file_updated': datafile,
        'line_added': line
    }

"""
API Endpoint Views
"""

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]


class logError(viewsets.ModelViewSet):
    """
    API endpoint that allows error logs to be viewed or edited.
    """
    queryset = ErrorLog.objects.all()
    serializer_class = ErrorLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # def logError():
    #     if not os.path.isfile(LOG_FILE):
    #         create_file('error', LOG_FILE)
    #     if request.method == 'POST':
    #         values = []
    #         for element in request.form:
    #             print(f'{element}, {request.form[element]}')
    #             values.append(request.form[element])
    #     return 'Error logged'


class checkUpdateAvailable(viewsets.ModelViewSet):
    """
    API endpoint that allows updates to be viewed or edited.
    """
    queryset = UpdateCheck.objects.all()
    serializer_class = UpdateCheckSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def retrieve(self, request, pk=None):
        
        update_check = self.get_object()
        version = update_check.version
        checked_date = update_check.checked_date
        
        # print("updated")
        
        if float(settings.APP_VERSION) > float(version):
            data = [
                'version: ' + version, 
                'checked_date: ' + str(checked_date), 
                'status: ' + 'update_available'
            ]
        else:    
            data = [
                'version: ' + version, 
                'checked_date: ' + str(checked_date), 
                'status: ' + 'system_upto_date'
            ]
        
        return Response(data)
    
    
class getFirmware(viewsets.ModelViewSet):
    """
    API endpoint that allows firmware to be viewed or edited.
    """
    queryset = Firmware.objects.all()
    serializer_class = FirmwareSerializer
    permission_classes = [permissions.IsAuthenticated]
            
    def retrieve(self, request, *args, **kwargs):
        
        # Args
        args = request.GET
        
        # Object
        instance = self.get_object()
        
        # Id
        firmware_id = instance.id
        
        # Checked date
        checked_date = str(instance.checked_date)
        
        # Filename
        if instance.filename:
            filename = instance.filename
        else:
            if filename:
                filename = filename
            else:
                filename = filename_rollback 
            
        # Firmware File
        firmware_file = str(instance.firmware_file.path)
        # firmware_file_size = os.stat(instance.file).st_size
        
        # Chunks
        with instance.firmware_file.open(mode='rb') as file:
            chunk_list = get_file_chunks(instance.firmware_file, chunk_size)
        num_chunks = len(chunk_list)
        
        # Add Checksum to Packet
        with instance.firmware_file.open(mode='rb') as file:
            packet = file.read()
        packet_w_checksum = add_checksum_to_packet(packet)
        
        # File Chunks with Checksums
        packet_n_checksum = get_file_chunks_with_checksums(instance.firmware_file, num_chunks)

        # Call create_file() function and get output data
        create_file_data = create_file(directory='data', datafile='datalog_coffee_n_tea_experiment.csv')
        
        # Call update_file() function and get output data
        line_to_add = ['value1', 'value2', 'value3']
        update_file_data = update_file(datafile='data/datalog_coffee_n_tea_experiment.csv', line=line_to_add)

        print("getting update")
        
        get_size_flag = int(args.get('gsf', 0))
        if get_size_flag == 1:
            num_requests = get_number_of_chunks(instance.firmware_file, chunk_size)
            return f"{str(math.ceil(num_requests))},{chunk_size+4}"

        get_data_flag = int(args.get('gdf', 0))
        if get_data_flag == 1:
            chunk = int(args.get('chunk', 0))
            file_chunks = get_file_chunks_with_checksums(instance.firmware_file, chunk_size)
            print(f"downloading {chunk+1} of {len(file_chunks)}")
            return file_chunks[chunk]

        data = [
            'Data for testing:',
            'id: ' + str(firmware_id),
            'filename: ' + filename,
            'checked_date: ' + checked_date,
            'firmware_file: ' + firmware_file,
            'file_size: ' + get_file_size(instance.firmware_file.size),
            'chunks: ' + str(num_chunks),
            'packet: ' + str(packet),
            'checksum_packet: ' + str(packet_w_checksum),
            'chunks_checksums: ' + str(packet_n_checksum),
            'create_file_output: ' + str(create_file_data),
            'update_file_output: ' + str(update_file_data),
            'args: ' + str(args),
            'get_size_flag: ' + str(get_size_flag),
            'get_data_flag: ' + str(get_data_flag)
        ]
        
        return Response(data)
    

