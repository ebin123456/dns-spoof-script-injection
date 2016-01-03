import socket
import dns.resolver
resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8']

class DNSQuery:
    def __init__(self, data):

        self.data=data
        self.domain=''

        tipo = (ord(data[2]) >> 3) & 15   
        if tipo == 0:                     
            ini=12
            lon=ord(data[ini])
            while lon != 0:
                self.domain+=data[ini+1:ini+lon+1]+'.'
                ini+=lon+1
                lon=ord(data[ini])

    def make_packet(self, ip):
        packet=''
        if self.domain:
            packet+=self.data[:2] + "\x81\x80"
            packet+=self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'   
            packet+=self.data[12:]                                         
            packet+='\xc0\x0c'                                             
            packet+='\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'             
            packet+=str.join('',map(lambda x: chr(int(x)), ip.split('.'))) 
        return packet

    def solve(self,query, spoofed_names):
        query = query.strip(".")
        if query in spoofed_names:
            return spoofed_names[query]
        answer = resolver.query(query)
        for rdata in answer:
            return str(rdata)


def main():
    spoofed_names = {"example.com":"127.0.0.1"}
    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.bind(('',53))
    try:
        while 1:
            data, addr = udps.recvfrom(1024)
            dns_query = DNSQuery(data)
            ip = dns_query.solve(dns_query.domain, spoofed_names)
            udps.sendto(dns_query.make_packet(ip), addr)
            print 'log: %s -> %s' % (dns_query.domain, ip)
    except KeyboardInterrupt:
        print 'Error'
        udps.close()


if __name__ == '__main__':

    while 1:
        try:
            main()
        except:
            pass  
    
  
  


# netsh interface ip set dns name="Local Area Connection" source=static addr=none

# netsh interface ip add dns name="Wi-Fi" addr=8.8.4.4 index=1
# netsh interface ip add dns name="Wi-Fi" addr=8.8.8.8 index=2

#netsh interface ip set dns name="Local Area Connection" source=static addr=none

# netsh interface ip add dns name="Wi-Fi" addr=192.168.100.4 index=1
# netsh interface ip add dns name="Wi-Fi" addr=127.0.0.1 index=2
