import datetime


def create_csv(branddata, framerate):
    if not isinstance(framerate, int) and not isinstance(framerate, float):
        print("Framerateparameter not int or float. Type of framerate: " + str(type(framerate)))
        exit(-1)

    if (len(branddata)) is 0:
        print("No framedata provided. Length of data: " + str(len(branddata)))
        exit(-1)

    frames = len(branddata)
    video_length_seconds = frames / framerate
    video_length = datetime.timedelta(seconds=video_length_seconds)

    brands = set().union(*(frame.keys() for frame in branddata))

    survey = []

    for brand in brands:
        get_times_for_brand(brand, video_length, branddata, framerate)


def get_times_for_brand(brand, video_length, branddata, framerate):
    frame_number = 0

    for frame in branddata:
        frame_number += 1
        for brand_ in frame.keys():
            if brand in brand_:
                video_time = datetime.timedelta(seconds=frame_number / framerate)
                occurences = frame.get(brand)
                #print(str(video_time) + ": " + str(occurences))


if __name__ == "__main__":
    dicts = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {'wanda': 4}, {'wanda': 5}, {'wanda': 6}, {'wanda': 6}, {'wanda': 6}, {'wanda': 6}, {'wanda': 6}, {'wanda': 6}, {'wanda': 6}, {'wanda': 6}, {'wanda': 6}, {'wanda': 6}, {'wanda': 6}, {'wanda': 6}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 4}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 5}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 2}, {'wanda': 2}, {'wanda': 2}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 3}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}, {'wanda': 4}]
    framerate = 25.0

    create_csv(dicts, framerate)
