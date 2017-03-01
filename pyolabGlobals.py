"""
global variables used by the pyolab library go here

"""

class G(object):

    # control varialbles
    sleepTimeRead = 0.05 # time to sleep each read loop
    sleepTimeAnal = 0.11 # time to sleep each read loop
    sleepCommand  = 0.10 # time to sleep after a command is sent
    dumpData = True      # if True the base analysis code dumps data to a file
    running  = True      # used to signal treads to quit
    configIsSet = False  # is it?

    # ports & files & threads
    serialPort = None    # pointer to the virtual com port
    outputFile = None    # file handle for output
    readThread = None    # pointer to data reading thread
    analThread = None    # pointer to data analysis thread

    # raw data retrieval and analysis - don't mess with these
    dataList = []        # data received from the serial port
    dataPointer = 0      # pointer to the next raw byte to be analyzed
    nextData = 0        # used by findRecords() - 
    
    #  Here is a description of the various record types along with their format.
    #  These are described in detail in the USB Interface Specification document 
    #  http://www.iolab.science/Documents/IOLab_Expert_Docs/IOLab_usb_interface_specs.pdf
    #
    recType_ACK = 0xaa
    #   0xaa = 170 (ACK)
    recType_NACK = 0xbb
    #   0xbb = 187 (NACK)
    #
    recType_getFixedConfig = 0x27
    #   0x27 =  39 (response to getFixedConfig() )
    #   Record: 0x02 : 0x27 : 0x01 : Config : 0xa
    #   
    recType_getPacketConfig = 0x28
    #   0x28 =  40 (response to getPacketConfig() )
    #   Record: 0x02 : 0x28 : Nbytes : Remote : Nsens : sens1 : len1 :...: sensN : lenN : 0xa
    #
    recType_getDongleStatus = 0x14
    #   0x14 =  19 (response to getDongleStatus() )    
    #   Record: 0x02 : 0x14 : 0x06 : Dongle FW (2) : Mode : ID (3) : 0xa
    #
    recType_getRemoteStatus = 0x2a
    #   0x2a =  42 (response to getRemoteStatus() )
    #   Record: 0x02 : 0x2a : 0x07 : Remote : Sens FW (2) : RF FW (2) : Battery (2) : 0xa
    #
    recType_rfStatusFromRemote = 0x40
    #   0x40 =  64 (asynchronous RF status records when RF signal lost or re-acquired)
    #   Record: 0x02 : 0x40 : 0x02 : Remote : RFstatus : 0xa
    #   
    recType_dataFromRemote = 0x41
    #   0x41 =  65 (asynchronous data records sent during actual data acquisition)
    #   Record: 0x02 : 0x41 : Nbytes : Remote : Frame# : RFinfo : Data Packet : RSSI : 0xa

     
    # this is a list of the record types that findRecords() will look for
    recTypeList = [recType_dataFromRemote, 
                   recType_getFixedConfig, 
                   recType_getPacketConfig, 
                   recType_rfStatusFromRemote, 
                   recType_getDongleStatus, 
                   recType_getRemoteStatus, 
                   recType_ACK, 
                   recType_NACK]

    # dictionary that stores received records, keyed by types outlined below
    recDict   = {}  

