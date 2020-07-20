import os.path as osp

try:
    import lxml.builder
    import lxml.etree
except ImportError:
    print("Please install lxml:\n\n    pip install lxml\n")
    sys.exit(1)

# this is just a demo bbox, please change here to your own logic
bboxes = [[68.0383, 42.0599, 123.3467, 83.8551],
        [698.8023, 147.2104, 724.7119, 216.1121],
        [505.4917, 297.4768, 533.9828, 345.2654]]

xml = []

maker = lxml.builder.ElementMaker()
xml = maker.annotation(
    maker.folder(),
    maker.filename(base + ".jpg"),
    maker.database(),  # e.g., The VOC2007 Database
    maker.annotation(),  # e.g., Pascal VOC2007
    maker.size(
        maker.height(str(img.shape[0])),
        maker.width(str(img.shape[1])),
        maker.depth(str(img.shape[2])),
    ),
    maker.segmented(),
)

for bbox in bboxes:

    (xmin, ymin), (xmax, ymax) = bbox
    # swap if min is larger than max.
    xmin, xmax = sorted([xmin, xmax])
    ymin, ymax = sorted([ymin, ymax])

    xml.append(
        maker.object(
            maker.name(shape["label"]),
            maker.pose(),
            maker.truncated(),
            maker.difficult(),
            maker.bndbox(
                maker.xmin(str(xmin)),
                maker.ymin(str(ymin)),
                maker.xmax(str(xmax)),
                maker.ymax(str(ymax)),
            ),
        )
    )

with open(out_xml_file, "wb") as f:
    f.write(lxml.etree.tostring(xml, pretty_print=True))
