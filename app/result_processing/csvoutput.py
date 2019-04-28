import datetime
import csv
import os

from termcolor import colored

from app import config


def create_csv(branddata, framerate):
    filename = config.DIR_REPORT + config.REPORT_OUT_NAME
    i = 1
    while os.path.isfile(filename.format(i)):
        i += 1
    filename = filename.format(i)

    brands = set().union(*(frame.keys() for frame in branddata))

    clear_csv_file(filename)

    for brand in brands:
        times, occurences = get_times_and_occurences_for_brand(brand, branddata, framerate)
        if len(times) != len(occurences):
            print(colored('\nError: Number of frame data times and frame data occurences mismatches.', 'red'))
            exit(-1)
        add_brand_to_csv(brand, times, occurences, filename)


def get_times_and_occurences_for_brand(brand, branddata, framerate):
    times = []
    occurences = []

    frame_number = 0
    for frame in branddata:
        keys = list(frame.keys())

        if len(keys) == 0:
            keys.append("None")

        for _ in keys:
            video_time = datetime.timedelta(seconds=(frame_number / framerate))
            times.append(video_time)

            occurence = frame.get(brand)
            occurences.append(occurence)

        frame_number += 1

    return times, occurences


def add_brand_to_csv(brand, times, occurences, filename):
    csv_ = {brand: {}}
    dict_ = {}
    dict = {}
    length = len(times)

    for i in range(1, length):
        if occurences[i-1] != occurences[i]:
            dict.update({i: occurences[i]})

        if i == (length - 1) and len(dict) == 0:
            dict.update({0: occurences[0]})

    sorted_ = sorted(dict)
    if sorted_[0] != 0:
        elems = occurences[:sorted_[0]]
        dict_ = {0: elems[0]}
        sorted_.insert(0, 0)

    dict_.update(dict)

    if sorted_[len(sorted_) - 1] != length:
        sorted_.append(length - 1)

    i = sorted_[0]
    for key in sorted_:
        if key == 0:
            continue
        start = str(times[i])
        end = str(times[key])

        if len(end) == 14:
            end = end[:10]
        if len(start) == 14:
            start = start[:10]

        time = start + " - " + end

        dict_[time] = dict_.pop(i)

        i = key

    csv_[brand].update(dict_)

    with open(filename, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, time_occurences in csv_.items():
            writer.writerow([key])
            for time, value in time_occurences.items():
                writer.writerow([";" + time + ";" + str(value)])


def clear_csv_file(filename):
    f = open(filename, 'w+')
    f.close()


if __name__ == "__main__":
    data = [{'wanda': 1}, {'wanda': 1}, {'wanda': 1},{'wanda': 1}]
    fps = 25.0

    create_csv(data, fps)