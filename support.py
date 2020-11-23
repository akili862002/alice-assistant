def sub_string_inside(s, start, end, get_bracket=False):
    if (start in s) and (end in s):
        start_pos = 0
        end_pos = len(s)-1
        while s[start_pos] != start: start_pos += 1
        while s[end_pos] != end: end_pos -= 1
        if get_bracket:
            return s[start_pos:end_pos+2]
        else:
            return s[start_pos+1:end_pos]
    else:
        return "[EMPTY]"

def delete_wrong_spaces_in_text(s):
    if s != "":
        while (len(s) > 1) and (s[0] == " "): s = s[1:]
        while (len(s) > 1) and s[len(s)-1] == " ": s = s[:len(s)-1]
        while "  " in s: s = s.replace("  ", " ")
    return s

def swap(a,b):
    return b,a

def get_code_systems(text):
    if ("{" in text) and ("}" in text):
        return sub_string_inside(text, "{", "}")
    else:
        return ""


def is_exit_in_string(ls, string):
    for index in ls:
        if index in string:
            return True
    return False

def is_user_accept(user):
    if is_exit_in_string(["good idea","yes","why not", "of course", "ok", "do it", "open it", "as you want", "whatever", "now"], user):
            return True
    return False

def is_user_refuse(user):
    if is_exit_in_string(["no", "negative", "cancel", "don't want", "never", "don't do it", "stop", "kidding"], user):
        return True
    return False

def split_text(s, bracket=';'):
    start = 0
    ls = []
    check_bracket = 0
    for i in range(len(s)):
        if s[i] == '[': check_bracket += 1
        elif s[i] == ']': check_bracket -= 1
        if ((s[i] == bracket) and (check_bracket == 0)):
            ls.append(s[start:i])
            start = i+1
        elif (i == len(s) -1):
            ls.append(s[start:])
    return ls

def get_code(s, start, end, get_bracket=False):
    if (start in s) and (end in s):
        if not get_bracket:
            return s[s.index(start)+1:s.index(end)]
        else:
            return s[s.index(start):s.index(end)+1]
    return ""

def get_all_code(s):
    codes = []
    while '{' in s:
        code = get_code(s, '{', '}',get_bracket=True)
        codes.append(code)
        s = s.replace(code,"")
    return codes

def remove(arr, i):
    return arr[:i] + arr[i+1:]

def beautiful_text(s, for_display=True):
    if s != "":
        while s[0] == " ": s = s[1:]
        while s[len(s)-1] == " ": s = s[:len(s)-1]
        while "  " in s: s = s.replace("  ", " ")
        if for_display:
            s = s[0].upper() + s[1:]
        else:
            s = s.lower()
    return s

def convertTimeToSecond(t):
    ls = t.split(":")
    if len(ls) == 3:
        return int(ls[0])*3600 + int(ls[1])*60 + int(ls[2])
    else:
        return int(ls[0])*3600 + int(ls[1])*60

def convertSecondToTime_text(s):
    hour = s//3600
    minute = (s - hour*3600)//60
    second = s - hour*3600 - minute*60
    res = ""
    if hour > 0:
        h_text = str(hour) + ":"
    else: h_text = ""
    if (minute > 0) or (hour > 0):
        m_text = str(minute) + ":"
    else: m_text = ""
    s_text = str(second)
    return h_text + m_text + s_text

def compare_time(a,b):
    t1 = convertTimeToSecond(a)
    t2 = convertTimeToSecond(b)

    if t1 > t2:
        return 1 # GREATER
    elif t1 < t2:
        return -1 # LESS_THAN
    else:
        return 0  # EQUAL

def get_perfect_time(t):
    (h,m) = t.split(':')[:2]
    tail = "AM"
    if 12 <= int(h) <= 24:
        tail = "PM"
    # f.e: t = "23:21:00" --> "23:21"
    return (":".join([h,m]) + " " + tail)
