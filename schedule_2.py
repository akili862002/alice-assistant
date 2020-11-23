import json, time
from control import *
import support as sp

def getTime(TYPE):
    imfor = time.ctime().replace("  ", " ")
    imformation = imfor.split()
    timeToday = imfor.replace(imformation[3]+ " ", "")
    ls = timeToday.split()
    result = {
        "time-now": imformation[3],
        "time-today": timeToday,
        "day-of-week": ls[0]
    }
    return result[TYPE]

def sort_schedule(missions, times_text, status): # simple sort
    n = len(times_text)
    times = n*[0]
    # Get all times type number ----
    for i in range(n):
        time_text = times_text[i].split("-")[0]
        times[i] = sp.convertTimeToSecond(time_text)

    for i in range(n):
        for j in range(i+1,n):
            if times[i] > times[j]:
                (times[i], times[j]) = sp.swap(times[i], times[j])
                (times_text[i], times_text[j]) = sp.swap(times_text[i], times_text[j])
                (missions[i], missions[j]) = sp.swap(missions[i], missions[j])
                (status[i], status[j]) = sp.swap(status[i], status[j])

    return missions, times_text, status

def save_schedule_to_timeTable(week, today, tomorrow):
    i = 0
    # Add status of work to list ToDo
    for (key, work) in today["list"].items():
        # Clear list ----
        today["list"][key] = today["list"][key].replace("[DONE]", "")
        today["list"][key] = today["list"][key].replace("[NOT_YET]", "")

        if today["status"][i] == DONE:
            today["list"][key] += "[DONE]"
        else:
            today["list"][key] += "[NOT_YET]"
        i += 1

    data = {
             "week":week,
             "today":today["list"],
             "tomorrow":tomorrow,
             "time-save": getTime("time-today")
    }


    file = open(PATH_SCHEDULE, "w")
    json.dump(data, file, indent=4)
    file.close()

def is_during_time(current_time, time_line):
    # Convert every string to number to compare easily
    current = sp.convertTimeToSecond(current_time)
    start   = sp.convertTimeToSecond(time_line[0])
    end     = sp.convertTimeToSecond(time_line[1])

    # if start Time is evening and end time is morning
    if start > end:
        if current < end:
            return True
    else: # normal
        if start < current < end:
            return True
    return False

def get_schedule_from_timeTable(path):
    file = open(path, "rb")
    data = json.load(file)
    file.close()
    currentTime = getTime("time-now")

    week = data["week"]

    toDo_today = data["week"][getTime("day-of-week")]
    status = len(toDo_today)*[NOT_YET]
    i = 0
    for (time_line, work) in toDo_today.items():
        # Check: did the mission pass?
        if not is_during_time(currentTime, ["0:00", time_line.split("-")[0]]):
            status[i] = DONE
        i += 1
    toDo_today = {"list": toDo_today, "status": status}

    remind = data["today"]
    status = len(remind)*[NOT_YET]

    if getTime("time-today") == data["time-save"]:
        # if current day and day in data are SAME: get data status from it.
        # else: renew all status
        i = 0
        for (t, work) in remind.items():
            if "[DONE]" in work:
                status[i] = DONE
                remind[t] = remind[t].replace("[DONE]","")
            else:
                status[i] = NOT_YET
                remind[t] = remind[t].replace("[NOT_YET]","")
            i += 1
    else:
        for (t, work) in remind.items():
            remind[t] = remind[t].replace("[NOT_YET]","")


    remind = {"list": remind, "status": status}


    return week, toDo_today, remind
week, TODO, remind = get_schedule_from_timeTable(PATH_SCHEDULE)

list_TODO = list(TODO["list"].values())
list_remind = list(remind["list"].values())

missions = list_TODO + list_remind
times = list(TODO["list"].keys()) + list(remind["list"].keys())
status = TODO["status"] + remind["status"]

missions, times, status = sort_schedule(missions, times, status)

def remind_user(currentTime):
    ls = []
    result = ""

    for i in range(len(missions)):
        (time_line, work) = (times[i], missions[i])
        if status[i] == NOT_YET:
            t = sp.convertTimeToSecond(time_line.split("-")[0]) - sp.convertTimeToSecond(currentTime)
            if t == 30*60: # next 30m
                ls.append(work + " in next 30 minutes")
            elif t == 10*60: # next 10m
                ls.append(work + " in next 10 minutes")
            elif t == 5*60: # next 5m
                ls.append(work + " in next 5 minutes")
            elif t == 0: # next 5m
                ls.append(work + " now")

    if len(ls) > 0:
        result = "Sir, you have to " + ls[0]
        for i in range(1, len(ls)):
            result += ", and " + ls[i]

    return result

# ---------------------------- RENEW
def get_missions_appearence_by_current_line(line, missions):
    show_texts = [HIDE_TEXT]*5
    current_line = line
    index_in_missions = [current_line-2, current_line-1, current_line, current_line+1, current_line+2]
    for i in range(5):
    	index = index_in_missions[i]
    	if (index < 0) or (index >= len(missions)):
    		pass
    	else:
    		show_texts[i] = missions[index]

    return show_texts

def get_current_line(currentTime="now"):
    line = 0
    if currentTime == "now":
        currentTime = getTime("time-now")
    for t in times:
        time_line = t.split("-")
        if sp.convertTimeToSecond(currentTime) < sp.convertTimeToSecond(time_line[0]):
            break
        elif len(time_line) == 2: # If startTime < currentTime < endTime
            if sp.convertTimeToSecond(currentTime) < sp.convertTimeToSecond(time_line[1]):
                break
        line += 1
    return line

def get_status(time):
    time_line = times[get_current_line(time)].split('-')
    if (sp.compare_time(time, time_line[0]) == LESS_THAN):
        return "[WAITING]"
    else:
        if len(time_line) == 2 and (sp.compare_time(time, time_line[1]) == LESS_THAN):
            return "[HAPPENING]"
        else:
            return "[DONE]"

def get_next_plan():
    currentTime = getTime("time-now")
    current_line = get_current_line(currentTime)
    if current_line < len(missions):
        if get_status(currentTime) == "[HAPPENING]":
            next = current_line + 1
        else: next = current_line
        answer = missions[next] + " in " + sp.get_perfect_time(times[next].split("-")[0])
    else:
        answer = "You don't have any mission left"
    return answer
