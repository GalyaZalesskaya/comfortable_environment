#!/usr/bin/env python
from __future__ import print_function
import sys
import os
#from argparse import ArgumentParser, SUPPRESS
import cv2
import numpy as np
import logging as log
from time import time
from openvino.inference_engine import IECore
import glob
from PIL import Image

Down_lock_in = 'pictures_in'

def class_size(road,sidewalk,building,wall,fence,pole,traffic_light,traffic_sign,vegetation,terrain,sky,
                   person,rider,car,truck,
                   bus,train,motorcycle,bicycle,ego_vehicle,cl21 , weight):
    sum_cl=road+sidewalk+building+wall+fence+pole+traffic_light+traffic_sign+vegetation+terrain+sky+person+rider+car+truck+bus+train+motorcycle+bicycle+ego_vehicle+cl21
    #print("Sum_cl",sum_cl)
    cl_size=[]
    cl_size.append(road/sum_cl)
    cl_size.append(sidewalk/sum_cl)
    cl_size.append(building/sum_cl)
    cl_size.append(wall/sum_cl)
    cl_size.append(fence/sum_cl)
    cl_size.append(pole/sum_cl)
    cl_size.append(traffic_light/sum_cl)
    cl_size.append(traffic_sign/sum_cl)
    cl_size.append(vegetation/sum_cl)
    cl_size.append(terrain/sum_cl)
    cl_size.append(sky/sum_cl)
    cl_size.append(person/sum_cl)
    cl_size.append(rider/sum_cl)
    cl_size.append(car/sum_cl)
    cl_size.append(truck/sum_cl)
    cl_size.append(bus/sum_cl)
    cl_size.append(train/sum_cl)
    cl_size.append(motorcycle/sum_cl)
    cl_size.append(bicycle/sum_cl)
    cl_size.append(ego_vehicle/sum_cl)
    cl_size.append(cl21/sum_cl)
    #print(cl_size)
    return comfort_level(cl_size, weight)

def comfort_level(cl_size, weight):
    weight_comf=[a*b for a,b in zip(cl_size,weight)]
    sum_comf=sum(weight_comf)
    return sum_comf

def imagesCoordinatesSegmentation(weight):
    model = "semantic-segmentation-adas-0001.xml"
    cpu_extension = None
    device = 'CPU'
    number_top = 10
    folders = glob.glob('pictures_in')
    input = []
    for file in folders:
        for f in glob.glob(file + '/*.png'):
            input.append(f)
    classes_color_map = {
        'road': (150, 150, 150),  # road (и вода тут) cl1
        'sidewalk': (58, 55, 169),  # sidewalk(бордюр,брусчатка) cl2
        'building': (211, 51, 17),  # building (и мосты тут) cl3
        'wall': (157, 80, 44),  # wall(ограждения, шлагбаум)cl4
        'fence': (23, 95, 189),  # fence(большой забор,ограждения мостов)cl5
        'pole': (210, 133, 34),  # pole(столбы,фонари)cl6
        'traffic light': (76, 226, 202),  # traffic light cl7
        'traffic sign': (101, 138, 127),  # traffic sign (очень плохо) cl8
        'vegetation': (223, 91, 182),  # vegetation(только деревья, без травы) cl9
        'terrain': (80, 128, 113),  # terrain(трава,снег)cl10
        'sky': (235, 155, 55),  # sky cl11
        'person': (44, 151, 243),  # person cl12
        'rider': (159, 80, 170),  # rider?? cl13
        'car': (239, 208, 44),  # car cl14
        'truck': (128, 50, 51),  # truck cl15
        'bus': (82, 141, 193),  # bus cl16
        'train': (9, 107, 10),  # train cl17
        'motorcycle': (223, 90, 142),  # motorcycle cl18
        'bicycle': (50, 248, 83),  # bicycle cl19
        'ego-vehicle': (178, 101, 130),  # ego-vehicle??? cl20
        'cl21': (71, 30, 204),  # ????? cl21
    }

    log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)

    log.info("Creating Inference Engine")
    ie = IECore()
    if cpu_extension and 'CPU' in device:
        ie.add_extension(cpu_extension, "CPU")
    # Read IR
    log.info("Loading network")
    net = ie.read_network(model, os.path.splitext(model)[0] + ".bin")

    if "CPU" in device:
        supported_layers = ie.query_network(net, "CPU")
        not_supported_layers = [l for l in net.layers.keys() if l not in supported_layers]
        if len(not_supported_layers) != 0:
            log.error("Following layers are not supported by the plugin for specified device {}:\n {}".
                      format(device, ', '.join(not_supported_layers)))
            log.error("Please try to specify cpu extensions library path in sample's command line parameters using -l "
                      "or --cpu_extension command line argument")
            sys.exit(1)
    assert len(net.inputs.keys()) == 1, "Sample supports only single input topologies"
    assert len(net.outputs) == 1, "Sample supports only single output topologies"

    log.info("Preparing input blobs")
    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.outputs))
    net.batch_size = len(input)

    # NB: This is required to load the image as uint8 np.array
    #     Without this step the input blob is loaded in FP32 precision,
    #     this requires additional operation and more memory.
    net.inputs[input_blob].precision = "U8"

    # Read and pre-process input images
    n, c, h, w = net.inputs[input_blob].shape
    images = np.ndarray(shape=(n, c, h, w))
    for i in range(n):
        image = cv2.imread(input[i])
        assert image.dtype == np.uint8
        if image.shape[:-1] != (h, w):
            log.warning("Image {} is resized from {} to {}".format(input[i], image.shape[:-1], (h, w)))
            image = cv2.resize(image, (w, h))
        image = image.transpose((2, 0, 1))  # Change data layout from HWC to CHW
        images[i] = image
    log.info("Batch size is {}".format(n))

    # Loading model to the plugin
    log.info("Loading model to the plugin")
    exec_net = ie.load_network(network=net, device_name=device)

    # Start sync inference
    log.info("Starting inference")
    res = exec_net.infer(inputs={input_blob: images})

    # Processing output blob
    log.info("Processing output blob")
    res = res[out_blob]
    if len(res.shape) == 3:
        res = np.expand_dims(res, axis=1)
    if len(res.shape) == 4:
        _, _, out_h, out_w = res.shape
    else:
        raise Exception("Unexpected output blob shape {}. Only 4D and 3D output blobs are supported".format(res.shape))

    n = 0
    marklist = []
    for batch, data in enumerate(res):
        if (n % 3 == 0):
            road = 0
            sidewalk = 0
            building = 0
            wall = 0
            fence = 0
            pole = 0
            traffic_light = 0
            traffic_sign = 0
            vegetation = 0
            terrain = 0
            sky = 0
            person = 0
            rider = 0
            car = 0
            truck = 0
            bus = 0
            train = 0
            motorcycle = 0
            bicycle = 0
            ego_vehicle = 0
            cl21 = 0
        n += 1
        classes_map = np.zeros(shape=(out_h, out_w, 3), dtype=np.int)
        for i in range(out_h):
            for j in range(out_w):
                if len(data[:, i, j]) == 1:
                    pixel_class = int(data[:, i, j])
                else:
                    pixel_class = np.argmax(data[:, i, j])
                classes_map[i, j, :] = classes_color_map[list(classes_color_map.keys())[min(pixel_class, 20)]]
                if min(pixel_class, 20) == 0:
                    road += 1
                elif min(pixel_class, 20) == 1:
                    sidewalk += 1
                elif min(pixel_class, 20) == 2:
                    building += 1
                elif min(pixel_class, 20) == 3:
                    wall += 1
                elif min(pixel_class, 20) == 4:
                    fence += 1
                elif min(pixel_class, 20) == 5:
                    pole += 1
                elif min(pixel_class, 20) == 6:
                    traffic_light += 1
                elif min(pixel_class, 20) == 7:
                    traffic_sign += 1
                elif min(pixel_class, 20) == 8:
                    vegetation += 1
                elif min(pixel_class, 20) == 9:
                    terrain += 1
                elif min(pixel_class, 20) == 10:
                    sky += 1
                elif min(pixel_class, 20) == 11:
                    person += 1
                elif min(pixel_class, 20) == 12:
                    rider += 1
                elif min(pixel_class, 20) == 13:
                    car += 1
                elif min(pixel_class, 20) == 14:
                    truck += 1
                elif min(pixel_class, 20) == 15:
                    bus += 1
                elif min(pixel_class, 20) == 16:
                    train += 1
                elif min(pixel_class, 20) == 17:
                    motorcycle += 1
                elif min(pixel_class, 20) == 18:
                    bicycle += 1
                elif min(pixel_class, 20) == 19:
                    ego_vehicle += 1
                else:
                    cl21 += 1
        if (n % 3 == 0):
            marklist.append(class_size(road, sidewalk, building, wall, fence, pole, traffic_light, traffic_sign, vegetation, terrain, sky,
               person, rider, car, truck, bus, train, motorcycle, bicycle, ego_vehicle, cl21, weight))
        out_img = os.path.join(os.path.dirname('__file__'), "pictures_out/out_{}.bmp".format(batch))
        cv2.imwrite(out_img, classes_map)
        log.info("Result image was saved to {}".format(out_img))
    return marklist
