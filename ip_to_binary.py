import traceback
import sys
infile = sys.argv[1]
outfile = sys.argv[1]
try:

    import bcrypt
    from passlib.hash import bcrypt

    def process(s):
        return ".".join(map(str,["{0:08b}".format(int(x)) for x in s.split(".")]))

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
