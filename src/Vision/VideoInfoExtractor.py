# Author: Gabriel Dinse
# File: ProductInfoExtractor
# Date: 11/1/2020
# Made with PyCharm

# Standard Library
from queue import Queue
from threading import Thread

# Third party modules
import cv2

# Local application imports
from Helper import WorkerQueue, ProductType
from Events import VideoInfoEvents
from Vision.SyncedVideoStream import SyncedVideoStream
from Errors import FrameReadingError


class VideoInfoExtractor:
    def __init__(self, frames_reader):
        self.events = VideoInfoEvents()
        self.frames_reader = frames_reader

        self.running = False

    def bind(self, **kwargs):
        self.events.bind(**kwargs)

    def load_product_type(self, product_type : ProductType):
        pass

    def get_centroids(self):
        """ Extrai da imagem os diametros e centroides da cada laranja. """

        contours = cv2.findContours(self.segment_mask.copy(),
                                    cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        self.diameters = []
        self.centroids = []
        self.contours = []
        for contour in contours:
            # Obtem os momentos do contorno:
            # m00 = area em pixels
            # m10 = momento de ordem 1 em x
            # m01 = momento de ordem 1 em y
            # m10/m00 = posicao x do centroide
            # m01/m00 = posicao y do centroide
            mom = cv2.moments(contour)

            # Filtra os contornos obtidos por metrica circular e area
            if (4*pi*mom['m00']/cv2.arcLength(contour, True)**2 > 0.8 and
                    mom['m00'] > 300):
                # Se o objeto eh aproximadamente circular, o diametro pode ser
                # estimado pela formula abaixo
                diameter = 2*sqrt(mom['m00']/pi)
                # Eh de interesse apenas a posicao do centroide em x
                centroid = (int(mom['m10'] / mom['m00']),
                            int(mom['m01'] / mom['m00']))
                self.diameters.append(diameter)
                self.centroids.append(centroid)
                self.contours.append(contour)

    def segment_frame(self):
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        # Corta o frame de acordo com os parametros de maximo e minimo de
        # largura e altura
        cropped_frame = np.zeros(self.frame.shape, dtype=np.uint8)
        cropped_frame[self.min_frame_height:self.max_frame_height,
                      self.min_frame_width:self.max_frame_width] = \
            self.frame[self.min_frame_height:self.max_frame_height,
                       self.min_frame_width:self.max_frame_width]
        self.frame = cropped_frame

        # Filtro gaussiano para suavizar ruidos na imagem
        blur = cv2.GaussianBlur(cropped_frame, (self.gaussian_kernel_size,
                                self.gaussian_kernel_size), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_RGB2HSV)

        # Segmentacao de acordo com o invervalo de cores HSV
        in_range_mask = cv2.inRange(
            hsv, (self.min_h, self.min_s, self.min_v),
                 (self.max_h, self.max_s, self.max_v))
        self.segment_mask = cv2.morphologyEx(in_range_mask, cv2.MORPH_OPEN,
                                             self.opening_kernel)
        self.processed_frame = cv2.bitwise_and(cropped_frame, cropped_frame,
                                               mask=self.segment_mask)

    def verify_frame(self):
        if self.identifier_running:
            if (time.time() - self.capture_timer) >= self.capture_timer_delay:
                for diameter, centroid in zip(self.diameters, self.centroids):
                    if (self.capture_line_position <= centroid[0]
                            <= self.capture_box_right_position):
                        self.create_capture_mask()

                        # cv2.mean retorna np.ndarray([R, G, B, alpha]), onde
                        # alpha eh a transparencia, nao utilizada neste caso
                        rgb_mean = np.array(cv2.mean(
                            self.processed_frame, mask=self.capture_mask)[0:3],
                                            dtype=np.uint8)
                        self.data_writer.add(
                            diameter * self.diameter_prop, rgb_mean)
                        self.capture_timer = time.time()
                        return

    def create_capture_mask(self):
        """ Cria uma mascara de captura baseada nos parametros de captura. """

        self.capture_mask = np.zeros(
            (int(self.camera.height), int(self.camera.width)), dtype=np.uint8)

        self.capture_mask[
            self.min_frame_height:
            self.max_frame_height + 1,
            self.capture_box_left_position:
            self.capture_box_right_position + 1
        ] = np.ones((
            self.max_frame_height - self.min_frame_height + 1,
            self.capture_box_left_width + 1 +
            self.capture_box_right_width),
            dtype=np.uint8)

        self.capture_mask = cv2.bitwise_and(
            self.capture_mask, self.capture_mask,
            mask=self.segment_mask)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = Thread(target=self.run, args=())
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            self.thread.join()

    def run(self):
        while self.running:
            try:
                self.frame = self.frames_reader.read()
            except FrameReadingError:
                pass
            else:
                self.get_convex_package()  # Convex hull
                self.calculate_package_centroid()
                self.calculate_cover_centroid()  # Template matching
                self.calculate_offset()

            # self.grabbed, self.frame = self.camera.read()
            # if self.grabbed:
            #     self.segment_frame()
            #     self.events.emit('new_frame', self.frame, self.mask)
            #     self.get_centroids()
            #     self.verify_frame()
            #     self.events.emit('new_product', self.last_product_info)

    def get_convex_package(self):
        gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        blurred_gray_frame = cv2.GaussianBlur(
            gray_frame,
            (self.gaussian_kernel_size, self.gaussian_kernel_size), 0)

        self.calculate_canny_threshold(blurred_gray_frame)
        canny_edges = cv2.Canny(
            blurred_gray_frame, self.lower_canny, self.upper_canny)
        self.convex_hull = convex_hull_image(canny_edges)

    def calculate_package_centroid(self):
        count = (self.convex_hull == 1).sum()
        self.x_center, _ = np.argwhere(self.convex_hull == 1).sum(0) / count

    def calculate_cover_centroid(self):
        found = None
        method = eval('cv2.TM_SQDIFF_NORMED')
        for scale in np.linspace(0.8, 1.2, 9):
            for orientation in ["0", "180"]:
                resized = imutils.resize(template,
                                         width=int(template.shape[1] * scale))
                # r = template.shape[1] / float(resized.shape[1])
                h, w = resized.shape
                if orientation == "180":
                    center = (w / 2, h / 2)
                    M = cv2.getRotationMatrix2D(center, 180, 1.0)
                    resized = cv2.warpAffine(resized, M, (h, w))

                method = eval(meth)

                res = cv2.matchTemplate(frame, resized, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

                if found is None or min_val < found[0]:
                    found = (min_val, min_loc, scale, max_loc)

                if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                    top_left = min_loc
                else:
                    top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
        h, w = template.shape
        centroide = (found[1][0] + found[2] * w / 2, found[1][1] + found[2] * h / 2)