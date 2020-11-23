import json, time
from control import *

def convertTimeToSecond(t):
    ls = t.split(":")
    if len(ls) == 3:
        return int(ls[0])*3600 + int(ls[1])*60 + int(ls[2])
    else:
        return int(ls[0])*3600 + int(ls[1])*60

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

def sort_dict_by_time(a):
	times_text = list(a.keys())
	n = len(times_text)
	times = n*[0]
	# Get all times type number ----
	for i in range(n):
		time_text = times_text[i].split("-")[0]
		times[i] = convertTimeToSecond(time_text)

	missions = list(a.values())
	for i in range(n):
		for j in range(i+1,n):
			if times[i] > times[j]:
				(times[i], times[j]) = swap(times[i], times[j])
				(times_text[i], times_text[j]) = swap(times_text[i], times_text[j])

	result = {}
	for time_text in times_text:
		result[time_text] = a[time_text]

	return result

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
    current = convertTimeToSecond(current_time)
    start   = convertTimeToSecond(time_line[0])
    end     = convertTimeToSecond(time_line[1])

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


def remind_user(currentTime, TODO, remind):
    ls = []
    result = ""

    i = 0
    for (time_line, work) in TODO["list"].items():
        if TODO["status"][i] == NOT_YET:
            detail = convertTimeToSecond(time_line.split("-")[0]) - convertTimeToSecond(currentTime)
            if detail == 30*60: # next 30m
                ls.append(work + " in next 30 minutes")
            elif detail == 15*60: # next 15m
                ls.append(work + " in next 15 minutes")
            elif detail == 10*60: # next 10m
                ls.append(work + " in next 10 minutes")
            elif detail == 5*60: # next 5m
                ls.append(work + " in next 5 minutes")
            elif detail == 0: # next 5m
                ls.append(work + " now")
        i += 1

    i = 0
    for (time_line, work) in remind["list"].items():
        if remind["status"][i] == NOT_YET:
            detail = convertTimeToSecond(time_line.split("-")[0]) - convertTimeToSecond(currentTime)
            if detail == 30*60: # next 30m
                ls.append(work + " in next 30 minutes")
            elif detail == 15*60: # next 15m
                ls.append(work + " in next 15 minutes")
            elif detail == 10*60: # next 10m
                ls.append(work + " in next 10 minutes")
            elif detail == 5*60: # next 5m
                ls.append(work + " in next 5 minutes")
            elif detail == 0: # next 0m
                ls.append(work + " now")
        i+=1

    if len(ls) > 0:
        result = "Sir, you have to " + ls[0]
        for i in range(1, len(ls)):
            result += ", and " + ls[i]

    return result

def assemble():
    num_todo = 0
    for status in TODO["status"]:
        if status == NOT_YET:
            num_todo += 1

    num_remind = 0
    for status in remind["status"]:
        if status == NOT_YET:
            num_remind += 1

    if (num_todo != 0) and (num_remind != 0):
        result = "Today you have " + str(num_todo) + " works and " + str(num_remind) + " missions."
    elif num_todo == 0:
        result = "Now you have " + str(num_remind) + " missions."
    elif num_remind == 0:
        result = "Now you have " + str(num_todo) + " works."
    if (num_todo == 0) and (num_remind == 0):
        result = "You don't have any mission to do now. Take a rest and enjoy yourself, Sir!"

    if num_remind + num_todo > 12:
        result += " It's going to be busy day."
    return result


# ---------------------------- RENEW
def get_missions_appearence_by_current_line(line):
    missions = list(a.values())
    show_texts = ["$NONE"]*5
    current_line = line
    index_in_missions = [current_line-2, current_line-1, current_line, current_line+1, current_line+2]
    for i in range(5):
    	index = index_in_missions[i]
    	if (index < 0) or (index >= len(missions)):
    		pass
    	else:
    		show_texts[i] = missions[index]

    return show_texts
