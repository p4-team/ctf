import string
import re
import sys

cmd = sys.argv[1]

# Encode using $'\123\234'
def stage1(cmd):
    return "echo $'" + "".join("\\%o" % ord(d) for d in cmd) + "'"

def escape(cmd):
    def enc(c):
        if c in "\\$()';":
            return "\\" + c
        return c

    return "".join(enc(c) for c in cmd)

# Encode digits using bash arithmetics.
def stage2(cmd):
    cmd = escape(cmd)
    def enc(c):
        if c not in string.digits:
            return c

        if c == "0":
            return "$(($$==$echo))"
        else:
            return "$((" + "+".join("$echo" for _ in range(int(c))) + "))"

    cmd = "".join(enc(c) for c in cmd)
    return "echo=$(($$==$$)); echo " + cmd


# Encode '
def stage3(cmd):
    cmd = escape(cmd)
    return "echo=\\'; echo " + cmd.replace("\\'", "$echo")

# Encode (
def stage4(cmd):
    cmd = escape(cmd)
    return "echo=\\(; echo " + cmd.replace("\\(", "$echo")

# Encode )
def stage5(cmd):
    cmd = escape(cmd)
    return "echo=\\); echo " + cmd.replace("\\)", "$echo")

# Encode +
def stage6(cmd):
    cmd = escape(cmd)
    return "echo=\\+; echo " + cmd.replace("+", "$echo")

# Encode ;
def stage7(cmd):
    cmd = escape(cmd)
    return "echo=\\;; echo " + cmd.replace("\\;", "$echo")

# Encode =
def stage8(cmd):
    cmd = escape(cmd)
    return "echo=\\=; echo " + cmd.replace("=", "$echo")



p = cmd
p = stage1(p)
p = stage2(p)
p = stage3(p)
p = stage4(p)
p = stage5(p)
p = stage6(p)
p = stage7(p)
p = stage8(p)

for c in set(p):
    print >>sys.stderr, c, p.count(c)
print p




