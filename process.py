def detect_objects(net, image):
    height, width, _ = image.image.shape
    blob = cv2.dnn.blobFromImage(image.image, 1/255, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(output_layers)
    return outputs

def process_detections(outputs, image, class_names):
    height, width, _ = image.image.shape
    bounding_boxes = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = max(0, int(center_x - w / 2))
                y = max(0, int(center_y - h / 2))
                w = min(width - x, w)
                h = min(height - y, h)

                bounding_box = BoundingBox(x, y, w, h, class_id, class_names[class_id])
                bounding_boxes.append(bounding_box)

    boxed_image = BoxedImage(image.image, bounding_boxes)
    return boxed_image
