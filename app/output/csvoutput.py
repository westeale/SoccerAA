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
        get_times_for_brand(brand, video_length, branddata)


def get_times_for_brand(brand, video_length, branddata):
    
    for frame in branddata:
        for brand_ in frame.keys():
            if brand is brand_:
                pass
                #print(brand)


if __name__ == "__main__":
    dicts = [{'wanda': 2}, {}, {'hyundai': 1, 'wanda': 1}]
    framerate = 24.0

    create_csv(dicts, framerate)
