import random
import cv2

class BoundingBox:
    def __init__(self, x, y, w, h, class_id, class_name):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.class_id = class_id
        self.class_name = class_name

class Image:
    def __init__(self, image):
        self.image = image

    def display_image(self):
        cv2.imshow("Image", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save_image(self, file_path):
        cv2.imwrite(file_path, self.image)

class BoxedImage(Image):
    def __init__(self, image, bounding_boxes):
        super().__init__(image)
        self.bounding_boxes = bounding_boxes

    def get_bounding_boxes(self, class_name=None):
        if class_name is None:
            return self.bounding_boxes
        else:
            return [box for box in self.bounding_boxes if box.class_name == class_name]

    def draw_bounding_boxes(self, class_name=None):
        image_copy = self.image.copy()
        for box in self.get_bounding_boxes(class_name):
            cv2.rectangle(image_copy, (box.x, box.y), (box.x + box.w, box.y + box.h), (0, 255, 0), 2)
            cv2.putText(image_copy, box.class_name, (box.x, box.y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        return Image(image_copy)

    def superimpose_image(self, superimpose_image, class_name=None):
        image_copy = self.image.copy()
        for box in self.get_bounding_boxes(class_name):
            resized_superimpose_image = cv2.resize(superimpose_image.image, (box.w, box.h))
            image_copy[box.y:box.y+box.h, box.x:box.x+box.w, :] = resized_superimpose_image
        return Image(image_copy)

    def superimpose_random_box(self, superimpose_image):
        image_copy = self.image.copy()
        if len(self.bounding_boxes) > 0:
            random_box = random.choice(self.bounding_boxes)
            resized_superimpose_image = cv2.resize(superimpose_image.image, (random_box.w, random_box.h))
            image_copy[random_box.y:random_box.y+random_box.h, random_box.x:random_box.x+random_box.w, :] = resized_superimpose_image
        return Image(image_copy)
