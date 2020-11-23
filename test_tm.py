import support as sp
import json
a = {
	"6:30-11:45": "Go to School",
    "14:00-16:30": "Study physics in private tuition",
    "16:30-20:00": "Study English in NewStart",
    "20:00-22:00": "Do English homework of NewStart",
    "22:00-23:00": "Do Homework",
    "6:00": "Do physical exercise",
    "11:30": "take a rest",
    "21:30": "Charge your bike",
    "21:30:1": "Go to sleep"
    }

def sort_dict_by_time(a):
	times_text = list(a.keys())
	n = len(times_text)
	times = n*[0]
	# Get all times type number ----
	for i in range(n):
		time_text = times_text[i].split("-")[0]
		times[i] = sp.convertTimeToSecond(time_text)

	missions = list(a.values())
	for i in range(n):
		for j in range(i+1,n):
			if times[i] > times[j]:
				(times[i], times[j]) = sp.swap(times[i], times[j])
				(times_text[i], times_text[j]) = sp.swap(times_text[i], times_text[j])

	result = {}
	for time_text in times_text:
		result[time_text] = a[time_text]

	return result


missions = list(a.values())
location = [100, 200, 300, 400, 500]
show_texts = ["$NONE"]*5
current_stay = int(input("Pos ="))
index_in_missions = [current_stay-2, current_stay-1, current_stay, current_stay+1, current_stay+2]
for i in range(5):
	index = index_in_missions[i]
	if (index < 0) or (index >= len(missions)):
		pass
	else:
		show_texts[i] = missions[index]

print("Ls: ",show_texts)
