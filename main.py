import getpass,hashlib,base64

def hasher(text,length,key):
    if length > 64:
       raise ValueError("hash length should be lower than 64")
    result = hashlib.sha256(text.encode("utf-8")+key.encode("utf8")+text.encode("utf8")).hexdigest()[:length][::-1]
    return result

def separator(text,length):
    return [text[i:i+length] for i in range(0,len(text),int(length))]

def decrypt(text,key):
    textsplit = text.split("!-!")
    encrypted,shuffled,hash_length,separate_length = textsplit[0].split("|")
    encrypted = separator(encrypted,int(hash_length))
    encrypted2 = separator("".join(encrypted),int(hash_length))
    shuffled = separator(shuffled,int(separate_length))
    primary_key_is_true = True
    for i in shuffled:
        hashed = hasher(i,int(hash_length),key)
        if hashed in encrypted:
           encrypted[encrypted.index(hashed)] = i

    for i in encrypted:
        if i in encrypted2 and len(textsplit) == 1:
           raise KeyError("Wrong Key")
        elif i in encrypted2:
           primary_key_is_true = False
           break

    if primary_key_is_true:
       result = base64.b64decode("".join(encrypted)[::-1])

    if len(textsplit) >= 2 and primary_key_is_true == False:
       master_key = separator(textsplit[1],int(hash_length))
       master_key2 = separator("".join(master_key),int(hash_length))
       for i in shuffled:
           hashed = hasher(i,int(hash_length),key)
           if hashed in master_key:
              master_key[master_key.index(hashed)] = i

       for i in master_key:
           if i in master_key2:
              raise KeyError("Wrong Key")
       result = base64.b64decode("".join(master_key)[::-1])
    return result

def unlock(key):
    exec (decrypt("bb12f80aa75c97fd7003fba1880536f935abcee3a7fbc86372322f6ee1faef9e566266ca48a0b55bd99bbd765269c1a62e313f8f5eeac39bf1158bc5|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|30|1098!-!d73e73b0dc06171f638fce75e68b20b3d64aedecac6d29d49cb81436d61ecd73ae1037c60b6737c865421087b2cfff0d10d8e69466aea68a002f58a8",key),globals())

if "__main__" == __name__:
   print("\n Download key ⟨ https://rotf.lol/GetKey ⟩")
   unlock(getpass.getpass(" Key : "))
