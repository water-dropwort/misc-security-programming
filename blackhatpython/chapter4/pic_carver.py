import re
import zlib
import cv2

from scapy.all import *

pictures_directory = "pictures"
faces_directory    = "faces"
pcap_file          = "bhp.pcap"

def get_http_headers(http_payload):
    try:
        # HTTPのヘッダーを抽出
        headers_raw = http_payload[:http_payload.index(b"\r\n\r\n")+2]
        # ヘッダーの各要素を辞書化
        headers = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", headers_raw.decode()))
    except ValueError:
        return None

    if "Content-Type" not in headers:
        return None

    return headers

def extract_image(headers, http_payload):
    image_type = None
    image      = None

    try:
        if "image" in headers["Content-Type"]:
            # 画像種別と画像本体の取得
            image_type = headers["Content-Type"].split("/")[1]
            image      = http_payload[http_payload.index(b"\r\n\r\n")+4:]

            # 画像が圧縮されている場合は解凍
            try:
                if "Content-Encoding" in headers.keys():
                    if headers["Contnet-Encoding"] == "gzip":
                        image = zlib.decompress(image, 16+zlib.MAX_WBITS)
                    elif headers["Content-Encoding"] == "deflate":
                        image = zlib.decompress(image)
            except:
                pass
    except Exception as e:
        print("[ERR] extract_image:",e)
        return None,None

    return image, image_type

def face_detect(path, file_name):
    img     = cv2.imread(path)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    rects   = cascade.detectMultiScale(img, 1.3, 4, cv2.CASCADE_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return False

    rects[:, 2:] += rects[:, :2]

    # 画像中のすべての顔をハイライト
    for x1,y1,x2,y2 in rects:
        cv2.rectangle(img, (x1,y1), (x2,y2), (127,255,0), 2)

    cv2.imwrite("%s/%s-%s" % (faces_directory, pcap_file, file_name), img)

    return True

def http_assembler(pictures_directory, faces_directory, pcap_file):
    carved_images  = 0
    faces_detected = 0

    # pcapファイルを開く
    pcap = rdpcap(pcap_file)
    # 各TCPセッションを辞書型データに格納
    sessions = pcap.sessions()
    
    for session in sessions:
        http_payload = b""
        for packet in sessions[session]:
            try:
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    # ストリームの再構築
                    http_payload += bytes(packet[TCP].payload)
            except:
                pass
        # HTTPヘッダーのパース
        #print(http_payload)
        
        headers = get_http_headers(http_payload)
        if headers is None:
            continue

        image, image_type = extract_image(headers, http_payload)
        
        if image is not None and image_type is not None:
            # 画像の保存
            file_name = "%s-pic_carver_%d.%s" % (pcap_file,carved_images,image_type)
            fd = open("%s/%s" % (pictures_directory, file_name), "wb")
            fd.write(image)
            fd.close()

            carved_images += 1

            # 顔検出
            try:
                result = face_detect("%s/%s" % (pictures_directory, file_name), file_name)
                if result is True:
                    faces_detected += 1
            except:
                pass
    return carved_images, faces_detected


carved_images, faces_detected = http_assembler(pictures_directory, faces_directory, pcap_file)

print("Extracted: %d images" % (carved_images))
print("Detected:  %d faces" % (faces_detected))
