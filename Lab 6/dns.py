import socket
import datetime
import bitstring
import time


def dns_query(domain):

    # prepare the messages that won't change
    # flag is 0b0000001110000000 -> 0x0380
    DNS_QUERY = {
        "id": "0x0001", "flags": "0x0380", "ques": "0x0001", "rrs": "0x0000",  "authrr": "0x0000", "addrr": "0x0000"
    }

    keys = ['id', 'flags', 'ques', 'rrs', 'authrr', 'addrr']

    # prepare the whole message to send to the server
    msg = "0x"
    for i in keys:
        msg += DNS_QUERY[i][2:]

    msg += question_query(domain)

    return msg


def question_query(domain):
    # split the domain into labels
    labels = domain.split(".")

    # get the QNAME
    QNAME = ""
    for i in labels:
        length = str(hex(len(i)))
        if len(length) == 3:
            length = "0" + length[2]
        else:
            length = length[2:]

        QNAME += length

        for j in i:
            digits = str(hex(ord(j)))
            if len(digits) == 3:
                digits = "0" + digits[2]
            else:
                digits = digits[2:]
            QNAME += digits

    # combine QNAME and QTYPE QCLASS
    rsl = QNAME + "0000010001"

    return rsl


# domain = "www.dp-and-the-science-anthropocene.netlify.app"
# domain = "www.google.com"
domain = input("which website do you want?\n")
# buidling up the server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# use bitstring to convert into bytes
msg = {'msg': dns_query(domain)}
data = bitstring.pack("hex=msg", **msg)

# bind the server to local address and port numer and send the data
sock.sendto(data.tobytes(), ('8.8.8.8', 53))

# receive and convert the message
data, _ = sock.recvfrom(512)
data = bitstring.BitArray(bytes=data)

response_code = str(data[28:32].hex)

result = {'domain_name': domain, 'ip_address': None,
          'ttl': None, "error": "Code 0: Success"}

# Check for errors
if (response_code == "0"):
    result['ip_address'] = ".".join([
        str(data[-32:-24].uintbe), str(data[-24:-
                                            16].uintbe), str(data[-16:-8].uintbe), str(data[-8:].uintbe)
    ])

    seconds = data[-80:-48].int
    days, seconds = divmod(seconds, 86400)  # 1 day = 86400 seconds
    hours, seconds = divmod(seconds, 3600)   # 1 hour = 3600 seconds
    minutes, seconds = divmod(seconds, 60)   # 1 minute = 60 seconds

    # Format the result into DD:HH:MM:SS
    result["ttl"] = f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"
    # result['ttl'] = str(datetime.datetime.fromtimestamp(
    #     data[-80:-48].int + int(time.time())))

elif (response_code == "1"):
    result['error'] = "Error 1 occured: Format error. Unable to interpret query."

elif (response_code == "2"):
    result['error'] = "Error 2 occured: Server failure. Unable to process query."

elif (response_code == "3"):
    result['error'] = "Error 3 occured: Name error. Domain name does not exist."

elif (response_code == "4"):
    result['error'] = "Error 4 occured: Query request type not supported."

elif (response_code == "5"):
    result['error'] = "Error 5 occured: Server refused query."

print(result)
