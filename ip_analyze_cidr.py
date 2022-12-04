import traceback
import sys
infile = sys.argv[1]
outfile = sys.argv[1]
try:

    import bcrypt
    from passlib.hash import bcrypt

    def ip_to_binary(s):
        return ".".join(map(str,["{0:08b}".format(int(x)) for x in s.split(".")]))
    def binary_to_ip(s):
        return ".".join(map(str,[int(x, 2) for x in s.split(".")]))
    def separate(s, member_count):
        return ".".join([s[ii*member_count:(ii+1)*member_count] for ii in range(0,len(s)//member_count)]) #split every 8 char
    def generate_mask_bin(cidr, trailing_char="0"):
        mask_len = int(cidr)
        result = "".join(["1" for ii in range(0,mask_len)]) + (32-mask_len)*trailing_char
        result = separate(result, 8)
        return result
    def mask(ip,mask,trailing_char="0"):
        return "".join([(ii[0] if ii[1]=="1" or ii[1] == "." else trailing_char) for ii in zip(ip,mask)])
    def int_to_bin(x):
        return "{0:08b}".format(int(x))
    def ip_add(ip, addendum):
        result = int("".join(ip.split(".")), 2) + addendum
        result = int_to_bin(result)
        result = ("0"*(32-len(result))) + result
        return separate(result, 8)

    def analyze(s):
        ip = s.split('/')[0]
        cidr = s.split('/')[1]
        ip_bin = ip_to_binary(ip)
        mask_bin = generate_mask_bin(cidr)
        available_ip = generate_mask_bin(cidr, trailing_char="*")
        available_ip_cnt = (2**(32-int(cidr)))
        first_ip_bin=mask(ip_bin, mask_bin, trailing_char="0")
        first_ip=binary_to_ip(first_ip_bin)
        last_ip_bin=mask(ip_bin, mask_bin, trailing_char="1")
        last_ip=binary_to_ip(last_ip_bin)
        gateway_ip_bin = first_ip_bin[:-1]+"1"
        gateway_ip = binary_to_ip(gateway_ip_bin)
        next_block_ip_bin = ip_add(last_ip_bin, 1)
        next_block_ip=binary_to_ip(next_block_ip_bin)
        result = f'result\n'
        result += f'cidr notation:  {s}\n'
        result += f'ip:             {ip}\n'
        result += f'netmask:        {cidr}\n'
        result += f'ip_bin:         {ip_bin} ({ip})\n'
        result += f'mask_bin:       {mask_bin} ({cidr})\n'
        result += f'available_ip:   {available_ip} (avilable ip: {available_ip_cnt})\n'
        result += f'first_ip_bin:   {first_ip_bin} ({first_ip})\n'
        result += f'last_ip_bin:    {last_ip_bin} ({last_ip})\n'
        result += f'gateway_ip_bin: {gateway_ip_bin} ({gateway_ip})\n'
        result += f'next_block:     {next_block_ip_bin} ({next_block_ip})\n'
        return result

    def process(s):
        return analyze(s)

    result = []
    with open(infile,"r") as f :
        for line in f:
            # auto truncate last newline
            result.append(process(line[:-1]))
            # print(line, len(line))
            # print(line.decode('utf-32'))
            # result.append(line)
    f.closed
    with open(outfile,"w") as f :
        for line in result:
            f.write(line)
    f.closed
except Exception as e:
    msg = traceback.format_exc()
    with open(outfile,"w") as f :
        f.write(msg)
    f.closed
