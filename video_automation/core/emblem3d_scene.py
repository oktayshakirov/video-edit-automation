"""Run inside Blender (`emblem3d.render` calls it headless): build one emblem
object, light it, and render its loop as transparent PNGs.

    Blender -b --factory-startup --python emblem3d_scene.py -- '<json>'

json: {"name", "out", "frames", "size", "tint": [r, g, b] 0..1, "only": [i...]}

Every object is built from primitives and curves here - nothing is
downloaded - in two materials: the brand's metal (`tint`) and a dark gloss,
plus a soft white where a part has to read as light. It sways +-24 degrees
and bobs a little over `frames`, so the last frame meets the first.
"""

import json
import math
import sys

import bpy

ARGS = json.loads(sys.argv[sys.argv.index("--") + 1])
TINT = tuple(ARGS.get("tint", (1.0, 0.78, 0.36)))


# -- the scene ----------------------------------------------------------------

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = "BLENDER_EEVEE"
    s.render.film_transparent = True
    s.render.resolution_x = s.render.resolution_y = ARGS.get("size", 560)
    s.render.image_settings.file_format = "PNG"
    s.render.image_settings.color_mode = "RGBA"
    s.view_settings.view_transform = "AgX"
    try:
        s.view_settings.look = "AgX - Medium High Contrast"
    except TypeError:
        pass
    e = s.eevee
    for attr, val in (("taa_render_samples", 48), ("use_raytracing", True),
                      ("use_shadows", True)):
        if hasattr(e, attr):
            setattr(e, attr, val)
    w = bpy.data.worlds.new("w")
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.020, 0.022, 0.035, 1)
    bg.inputs[1].default_value = 1.0
    s.world = w
    return s


def mat(name, color, metal=0.0, rough=0.4, emit=0.0, coat=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    if coat and "Coat Weight" in b.inputs:
        b.inputs["Coat Weight"].default_value = coat
    if emit:
        b.inputs["Emission Color"].default_value = (*color, 1)
        b.inputs["Emission Strength"].default_value = emit
    return m


def lights():
    def area(name, loc, rot, power, size, color):
        d = bpy.data.lights.new(name, "AREA")
        d.energy, d.size, d.color = power, size, color
        o = bpy.data.objects.new(name, d)
        o.location, o.rotation_euler = loc, rot
        bpy.context.collection.objects.link(o)
    area("key", (-3.2, -3.6, 4.0), (math.radians(50), 0, math.radians(-40)), 900, 3.5,
         (1.0, 0.95, 0.88))
    area("rim", (3.4, 3.0, 2.6), (math.radians(-60), 0, math.radians(140)), 1100, 2.5,
         (0.70, 0.80, 1.0))
    area("fill", (4.0, -4.0, 0.5), (math.radians(85), 0, math.radians(45)), 220, 5.0,
         (0.85, 0.88, 1.0))
    # Two big soft panels out of shot: what the metal reflects.
    for x in (-6, 6):
        bpy.ops.mesh.primitive_plane_add(size=6, location=(x, -2, 1.5),
                                         rotation=(0, math.radians(90), 0))
        p = bpy.context.object
        p.data.materials.append(mat("panel", (1, 1, 1), emit=1.6))
        p.visible_camera = False


def camera():
    c = bpy.data.cameras.new("cam")
    c.lens = 92
    o = bpy.data.objects.new("cam", c)
    o.location = (0, -9.2, 1.6)
    o.rotation_euler = (math.radians(81), 0, 0)
    bpy.context.collection.objects.link(o)
    bpy.context.scene.camera = o


# -- helpers ------------------------------------------------------------------

def smooth(o, bevel=0.0, seg=4):
    if bevel:
        m = o.modifiers.new("bevel", "BEVEL")
        m.width, m.segments = bevel, seg
        m.limit_method = "ANGLE"
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def tube(points, depth, material, name="tube"):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth, cu.bevel_resolution = depth, 6
    cu.use_fill_caps = True
    sp = cu.splines.new("POLY")
    sp.points.add(len(points) - 1)
    for p, (x, y, z) in zip(sp.points, points):
        p.co = (x, y, z, 1)
    o = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(material)
    return o


def arc(cx, cz, r, a0, a1, n=48, y=0.0):
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), y,
             cz + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def add(o, material):
    o.data.materials.append(material)
    return o


# -- the objects ----------------------------------------------------------------

def microphone(G, D, L):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.62, location=(0, 0, 1.05),
                                         segments=48, ring_count=24)
    head = smooth(add(bpy.context.object, D))
    head.scale = (1, 1, 1.18)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.645, location=(0, 0, 1.05),
                                         segments=24, ring_count=14)
    grille = bpy.context.object
    grille.scale = (1, 1, 1.18)
    w = grille.modifiers.new("wire", "WIREFRAME")
    w.thickness = 0.028
    add(grille, G)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.6, minor_radius=0.07,
                                     location=(0, 0, 0.52))
    smooth(add(bpy.context.object, G))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.33, depth=1.3, location=(0, 0, -0.15),
                                        vertices=48)
    smooth(add(bpy.context.object, D), 0.04)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.34, minor_radius=0.05,
                                     location=(0, 0, -0.55))
    smooth(add(bpy.context.object, G))


def headphones(G, D, L):
    tube(arc(0, 0.1, 1.05, math.radians(10), math.radians(170)), 0.09, G, "band")
    for s in (-1, 1):
        x = s * 1.02
        bpy.ops.mesh.primitive_cylinder_add(radius=0.42, depth=0.34,
                                            location=(x, 0, -0.25),
                                            rotation=(0, math.radians(90), 0), vertices=48)
        smooth(add(bpy.context.object, D), 0.06)
        bpy.ops.mesh.primitive_torus_add(major_radius=0.36, minor_radius=0.11,
                                         location=(x - s * 0.2, 0, -0.25),
                                         rotation=(0, math.radians(90), 0))
        smooth(add(bpy.context.object, D))
        bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.05,
                                            location=(x + s * 0.18, 0, -0.25),
                                            rotation=(0, math.radians(90), 0), vertices=48)
        smooth(add(bpy.context.object, G))
        tube([(x, 0, -0.02), (x * 0.99, 0, 0.32)], 0.06, G, "yoke")


def coin(G, D, L):
    bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=0.2, vertices=96,
                                        rotation=(math.radians(90), 0, 0))
    smooth(add(bpy.context.object, G), 0.04, 3)
    for r in (0.86, 0.62):
        bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=0.035,
                                         rotation=(math.radians(90), 0, 0),
                                         location=(0, -0.1, 0))
        smooth(add(bpy.context.object, G))
    # A raised star in the middle, the same on both faces.
    pts = []
    for i in range(11):
        a = math.pi / 2 + i * math.pi / 5
        r = 0.42 if i % 2 == 0 else 0.18
        pts.append((r * math.cos(a), -0.12, r * math.sin(a)))
    tube(pts, 0.035, G, "star")


def padlock(G, D, L):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.35))
    body = bpy.context.object
    body.scale = (1.5, 0.55, 1.2)
    bpy.ops.object.transform_apply(scale=True)
    smooth(add(body, G), 0.12, 5)
    tube([(-0.48, 0, 0.2)] + arc(0, 0.62, 0.48, math.radians(180), 0)[1:] +
         [(0.48, 0, 0.2)], 0.11, D, "shackle")
    bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.2, location=(0, -0.28, -0.2),
                                        rotation=(math.radians(90), 0, 0), vertices=32)
    smooth(add(bpy.context.object, D))
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.29, -0.45))
    k = bpy.context.object
    k.scale = (0.09, 0.2, 0.32)
    add(k, D)


def clapper(G, D, L):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.25))
    b = bpy.context.object
    b.scale = (2.0, 0.16, 1.3)
    bpy.ops.object.transform_apply(scale=True)
    smooth(add(b, D), 0.05)
    for i in range(3):                       # chalk lines
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.085, -0.05 - i * 0.32))
        c = bpy.context.object
        c.scale = (1.7, 0.01, 0.03)
        add(c, L)
    for k, (z, tilt) in enumerate(((0.52, 0.0), (0.72, 18.0))):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
        top = bpy.context.object
        top.scale = (2.0, 0.16, 0.26)
        bpy.ops.object.transform_apply(scale=True)
        smooth(add(top, G), 0.03)
        top.location = (0, 0, z)
        top.rotation_euler = (0, math.radians(-tilt), 0)
        for i in range(5):                  # dark stripes
            bpy.ops.mesh.primitive_cube_add(size=1)
            st = bpy.context.object
            st.scale = (0.16, 0.17, 0.27)
            st.rotation_euler = (0, math.radians(-35), 0)
            st.location = (-0.8 + i * 0.4, 0, 0)
            add(st, D)
            st.parent = top


def note(G, D, L):
    for x, h in ((-0.55, 1.0), (0.55, 1.2)):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.36, location=(x, 0, -0.75))
        o = bpy.context.object
        o.scale = (1.25, 0.7, 0.85)
        o.rotation_euler = (0, math.radians(25), 0)
        smooth(add(o, G))
        tube([(x + 0.36, 0, -0.7), (x + 0.36, 0, -0.7 + h + 0.55)], 0.06, G, "stem")
    # The beam joins the two stem tops: (-0.19, 0.85) and (0.91, 1.05).
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.36, 0, 0.92))
    beam = bpy.context.object
    beam.scale = (1.26, 0.14, 0.24)
    beam.rotation_euler = (0, math.radians(-11), 0)
    smooth(add(beam, G), 0.04)


def play(G, D, L):
    bpy.ops.mesh.primitive_cube_add(size=1)
    b = bpy.context.object
    b.scale = (2.2, 0.36, 1.55)
    bpy.ops.object.transform_apply(scale=True)
    smooth(add(b, D), 0.34, 8)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.55, depth=0.2, vertices=3,
                                        location=(0.08, -0.2, 0),
                                        rotation=(math.radians(90), math.radians(-30), 0))
    smooth(add(bpy.context.object, G), 0.06)


def chart(G, D, L):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -1.0))
    base = bpy.context.object
    base.scale = (2.4, 0.9, 0.12)
    bpy.ops.object.transform_apply(scale=True)
    smooth(add(base, D), 0.04)
    for i, h in enumerate((0.55, 0.95, 0.8, 1.45, 1.95)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.92 + i * 0.46, 0, -0.94 + h / 2))
        c = bpy.context.object
        c.scale = (0.3, 0.3, h)
        bpy.ops.object.transform_apply(scale=True)
        smooth(add(c, G if i == 4 else D), 0.05)


def wave(G, D, L):
    hs = (0.35, 0.8, 1.35, 0.95, 1.7, 1.15, 0.6, 1.0, 0.4)
    for i, h in enumerate(hs):
        x = -1.2 + i * 0.3
        tube([(x, 0, -h / 2), (x, 0, h / 2)], 0.12, G if i == 4 else D, "bar")


def bulb(G, D, L):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.78, location=(0, 0, 0.35),
                                         segments=48, ring_count=24)
    glass = smooth(bpy.context.object)
    gm = mat("glass", (1.0, 0.86, 0.6), rough=0.05, emit=0.45)
    add(glass, gm)
    for i in range(3):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.34, minor_radius=0.06,
                                         location=(0, 0, -0.42 - i * 0.13))
        smooth(add(bpy.context.object, G))
    bpy.ops.mesh.primitive_cone_add(radius1=0.3, radius2=0.12, depth=0.2,
                                    location=(0, 0, -0.85))
    smooth(add(bpy.context.object, D))


OBJECTS = {"microphone": microphone, "headphones": headphones, "coin": coin,
           "padlock": padlock, "clapper": clapper, "note": note, "play": play,
           "chart": chart, "wave": wave, "bulb": bulb}


def main():
    s = reset()
    lights()
    camera()
    G = mat("metal", TINT, metal=1.0, rough=0.22)
    D = mat("dark", (0.035, 0.036, 0.048), metal=0.35, rough=0.3, coat=0.6)
    L = mat("light", (0.95, 0.95, 0.97), rough=0.5)
    before = set(bpy.data.objects)
    OBJECTS[ARGS["name"]](G, D, L)
    rig = bpy.data.objects.new("rig", None)
    bpy.context.collection.objects.link(rig)
    for o in set(bpy.data.objects) - before:
        if o.parent is None and o.type in ("MESH", "CURVE"):
            o.parent = rig
    n = ARGS.get("frames", 120)
    only = ARGS.get("only")
    for i in range(n):
        if only and i not in only:
            continue
        p = 2 * math.pi * i / n
        rig.rotation_euler = (math.radians(6) * math.sin(2 * p), 0,
                              math.radians(24) * math.sin(p))
        rig.location = (0, 0, 0.06 * math.sin(2 * p))
        s.render.filepath = f"{ARGS['out']}/{i:04d}.png"
        bpy.ops.render.render(write_still=True)


main()
