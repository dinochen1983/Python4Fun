import csv
import math
import ifcopenshell
import ifcopenshell.api


# ============================================================
# 通用工具
# ============================================================

def to_float(value, default=0.0):
    if value is None:
        return default

    value = str(value).strip()

    if value == "":
        return default

    return float(value)


def get_value(row, key, default=0.0):
    """
    安全读取 CSV 字段。
    如果字段不存在或为空，返回 default。
    """
    return to_float(row.get(key, default), default)


def create_ifc_file():
    model = ifcopenshell.api.run(
        "project.create_file",
        version="IFC4"
    )

    project = ifcopenshell.api.run(
        "root.create_entity",
        model,
        ifc_class="IfcProject",
        name="CSV Structure Project"
    )

    ifcopenshell.api.run(
        "unit.assign_unit",
        model,
        length={
            "is_metric": True,
            "raw": "METERS"
        }
    )

    context = ifcopenshell.api.run(
        "context.add_context",
        model,
        context_type="Model"
    )

    body_context = ifcopenshell.api.run(
        "context.add_context",
        model,
        context_type="Model",
        context_identifier="Body",
        target_view="MODEL_VIEW",
        parent=context
    )

    return model, project, body_context


def create_spatial_structure(model, project):
    site = ifcopenshell.api.run(
        "root.create_entity",
        model,
        ifc_class="IfcSite",
        name="Default Site"
    )

    building = ifcopenshell.api.run(
        "root.create_entity",
        model,
        ifc_class="IfcBuilding",
        name="Default Building"
    )

    storey = ifcopenshell.api.run(
        "root.create_entity",
        model,
        ifc_class="IfcBuildingStorey",
        name="Ground Floor"
    )

    ifcopenshell.api.run(
        "aggregate.assign_object",
        model,
        relating_object=project,
        products=[site]
    )

    ifcopenshell.api.run(
        "aggregate.assign_object",
        model,
        relating_object=site,
        products=[building]
    )

    ifcopenshell.api.run(
        "aggregate.assign_object",
        model,
        relating_object=building,
        products=[storey]
    )

    for obj in [site, building, storey]:
        ifcopenshell.api.run(
            "geometry.edit_object_placement",
            model,
            product=obj
        )

    return storey


def assign_to_storey(model, storey, elements):
    ifcopenshell.api.run(
        "spatial.assign_container",
        model,
        relating_structure=storey,
        products=elements
    )


# ============================================================
# 几何创建
# ============================================================

def matrix_from_axes(origin, x_axis, y_axis, z_axis):
    """
    用局部坐标轴生成 IfcOpenShell 使用的 4x4 矩阵。

    origin: (x, y, z)
    x_axis: 局部 X 方向
    y_axis: 局部 Y 方向
    z_axis: 局部 Z 方向
    """
    ox, oy, oz = origin

    return [
        [x_axis[0], y_axis[0], z_axis[0], ox],
        [x_axis[1], y_axis[1], z_axis[1], oy],
        [x_axis[2], y_axis[2], z_axis[2], oz],
        [0, 0, 0, 1],
    ]


def normalize(v):
    x, y, z = v
    length = math.sqrt(x * x + y * y + z * z)

    if length == 0:
        raise ValueError("不能归一化零向量")

    return (
        x / length,
        y / length,
        z / length
    )


def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    )


def create_box_representation(model, context, length, width, height):
    """
    创建一个局部长方体：
    X 方向：length
    Y 方向：width
    Z 方向：height
    """
    representation = ifcopenshell.api.run(
        "geometry.add_wall_representation",
        model,
        context=context,
        length=length,
        thickness=width,
        height=height
    )

    return representation


def assign_geometry(model, product, representation, matrix):
    ifcopenshell.api.run(
        "geometry.assign_representation",
        model,
        product=product,
        representation=representation
    )

    ifcopenshell.api.run(
        "geometry.edit_object_placement",
        model,
        product=product,
        matrix=matrix
    )


# ============================================================
# 梁 Beam
# ============================================================
def matrix_from_location_and_angle(x, y, z, angle_rad):
    """
    根据 XY 平面角度生成 4x4 变换矩阵。
    局部 X 方向为梁长度方向。
    """
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    return [
        [cos_a, -sin_a, 0, x],
        [sin_a,  cos_a, 0, y],
        [0,      0,     1, z],
        [0,      0,     0, 1],
    ]
def create_beam_from_row(model, context, row):
    """
    Beam:
    - 尺寸：bb, hh
    - ax, ay, az 是梁顶面中心线起点
    - bx, by, az 是梁顶面中心线终点
    - 梁顶标高 = az
    - 梁底标高 = az - hh
    """

    name = row.get("name", "Beam")

    ax = get_value(row, "ax")
    ay = get_value(row, "ay")
    az = get_value(row, "az")

    bx = get_value(row, "bx")
    by = get_value(row, "by")

    bb = get_value(row, "bb")  # 梁宽
    hh = get_value(row, "hh")  # 梁高

    vx = bx - ax
    vy = by - ay

    beam_length = math.sqrt(vx * vx + vy * vy)

    if beam_length <= 0:
        raise ValueError(f"梁 {name} 的起点和终点重合，长度为 0")

    angle = math.atan2(vy, vx)

    beam = ifcopenshell.api.run(
        "root.create_entity",
        model,
        ifc_class="IfcBeam",
        name=name
    )

    representation = create_box_representation(
        model,
        context,
        length=beam_length,
        width=bb,
        height=hh
    )

    # --------------------------------------------------------
    # 坐标点是梁顶面中点线：
    #
    # 目标：
    #   顶面中心线起点 = ax, ay, az
    #
    # add_wall_representation 生成的几何大致为：
    #   X: 0 到 beam_length
    #   Y: 0 到 bb
    #   Z: 0 到 hh
    #
    # 所以需要：
    #   Y 方向移动 -bb / 2，让中心线位于梁宽中间
    #   Z 方向移动 -hh，让顶面位于 az
    #
    # 但 matrix 只能直接给局部原点位置。
    # 因此局部原点应位于：
    #   顶面中心线起点
    #   再沿局部 Y 负方向偏移 bb/2
    #   再沿 Z 负方向偏移 hh
    # --------------------------------------------------------

    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    # 局部 Y 轴方向为 (-sin_a, cos_a, 0)
    local_y_x = -sin_a
    local_y_y = cos_a

    origin_x = ax - local_y_x * bb / 2
    origin_y = ay - local_y_y * bb / 2
    origin_z = az - hh

    matrix = matrix_from_location_and_angle(
        origin_x,
        origin_y,
        origin_z,
        angle
    )

    assign_geometry(
        model,
        beam,
        representation,
        matrix
    )

    return beam
# ============================================================
# 柱 Column
# ============================================================

def create_column_from_row(model, context, row):
    """
    Column:
    - 尺寸：bb, hh
    - 平面坐标：ax, ay
    - 底标高：az
    - 顶标高：bz
    - 高度：abs(bz - az)
    """

    name = row.get("name", "Column")

    ax = get_value(row, "ax")
    ay = get_value(row, "ay")
    az = get_value(row, "az")

    bz = get_value(row, "bz")

    bb = get_value(row, "bb")  # 柱 X 尺寸
    hh = get_value(row, "hh")  # 柱 Y 尺寸

    column_height = get_value(row, "len")  

    if column_height <= 0:
        raise ValueError(f"柱 {name} 的高度为 0，请检查 az 和 bz")

    bottom_z = az-column_height

    column = ifcopenshell.api.run(
        "root.create_entity",
        model,
        ifc_class="IfcColumn",
        name=name
    )

    representation = create_box_representation(
        model,
        context,
        length=bb,
        width=hh,
        height=column_height
    )

    # 柱中心在 ax, ay
    # 因为长方体从局部原点开始生成，所以放置时减去半宽半高
    matrix = [
        [1, 0, 0, ax - bb / 2],
        [0, 1, 0, ay - hh / 2],
        [0, 0, 1, bottom_z],
        [0, 0, 0, 1],
    ]

    assign_geometry(
        model,
        column,
        representation,
        matrix
    )

    return column


# ============================================================
# 楼板 Slab，可选
# ============================================================

def create_slab_from_row(model, context, row):
    """
    Slab:
    使用 ax,ay bx,by cx,cy dx,dy 四个点生成矩形包围盒楼板。
    thickness 使用 hh。
    标高使用 az。
    """

    name = row.get("name", "Slab")

    ax = get_value(row, "ax")
    ay = get_value(row, "ay")

    bx = get_value(row, "bx")
    by = get_value(row, "by")

    cx = get_value(row, "cx")
    cy = get_value(row, "cy")

    dx = get_value(row, "dx")
    dy = get_value(row, "dy")

    az = get_value(row, "az")
    thickness = 1.0* get_value(row, "bb", 0.2)

    points = [
        (ax, ay),
        (bx, by),
        (cx, cy),
        (dx, dy)
    ]

    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    length = max_x - min_x
    width = max_y - min_y

    if length <= 0 or width <= 0:
        raise ValueError(f"楼板 {name} 的尺寸无效")

    slab = ifcopenshell.api.run(
        "root.create_entity",
        model,
        ifc_class="IfcSlab",
        name=name
    )

    representation = create_box_representation(
        model,
        context,
        length=length,
        width=width,
        height=thickness
    )

    matrix = [
        [1, 0, 0, min_x],
        [0, 1, 0, min_y],
        [0, 0, 1, az-thickness],
        [0, 0, 0, 1],
    ]

    assign_geometry(
        model,
        slab,
        representation,
        matrix
    )

    return slab


# ============================================================
# 主函数：读取 CSV 并创建 IFC
# ============================================================

def create_ifc_from_csv(csv_path, ifc_path):
    model, project, body_context = create_ifc_file()
    storey = create_spatial_structure(model, project)

    elements = []

    with open(csv_path, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            element_type = row.get("type", "").strip().lower()

            if element_type == "beam":
                element = create_beam_from_row(
                    model,
                    body_context,
                    row
                )
                elements.append(element)

            elif element_type == "column":
                element = create_column_from_row(
                    model,
                    body_context,
                    row
                )
                elements.append(element)

            elif element_type == "slab":
                element = create_slab_from_row(
                    model,
                    body_context,
                    row
                )
                elements.append(element)

            else:
                print(f"跳过未知构件类型：{row.get('type')}")

    assign_to_storey(model, storey, elements)

    model.write(ifc_path)

    print(f"IFC 文件已生成：{ifc_path}")


# ============================================================
# 程序入口
# ============================================================

if __name__ == "__main__":
    create_ifc_from_csv(
        csv_path="input.txt",
        ifc_path="structure_from_csv.ifc"
    )