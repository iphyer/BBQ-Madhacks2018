# BBQ_Madhacks2018
The bounding box quality checking web service for Madhacks 2018

## Introduction

This is the code repository for [Madhacks 2018](https://www.madhacks.io/). Madhacks is the University of Wisconsin's twice-annual hackathon, bringing together participants from all over the US and Canada for 24 hours of hacking.

BBQ standing bounding box qualifier which is a web service that examines the matching between ground truth bounding boxes and the predicted bounding boxes and produces a prediction quality report and debugging tools for object detection algorithm.

A lot of work of object detection methods are focusing on how to generate bounding box annotations like [Crowdsourcing Annotations for Visual Object Detection](https://www.aaai.org/ocs/index.php/WS/AAAIW12/paper/view/5350),[Quanti.us: a tool for rapid, flexible, crowd-based annotation of images](https://www.nature.com/articles/s41592-018-0069-0.epdf?author_access_token=peMhy5KSdgrSAGSfL8MUj9RgN0jAjWel9jnR3ZoTv0MnaAwHfA480_WbrLsTyrf6Qh6XRwtU2XRrYgJxeQPIsjUlh3Szynwft2k_VerLS8Bw2R-WfjMsCopQ1wDRpFg6mja_Ndv4Rc75h2Wf-ODxJw%3D%3D) and exploer why the object detection algorithm fails like [HOGgles: Visualizing Object Detection Features](https://ieeexplore.ieee.org/document/6751109). However, few have talked about how to debug or check where the object detection model fails. This hackathon project is a tool that can help people actually see where the object detection algorithm fails.

## Problem Define



### Input 

Basic

