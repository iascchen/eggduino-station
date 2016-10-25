/**
 * Created by chenhao on 2016/9/29.
 */

let getLut = function (m_min, m_max) {
    let numberOfColors = 512;
    lut = new THREE.Lut('rainbow', numberOfColors);
    lut.setMax(m_max);
    lut.setMin(m_min);
    return lut;
};

/*****************************************
 * Axis
 *****************************************/

let buildAxis = function (src, dst, colorHex, dashed) {
    let geom = new THREE.Geometry(), mat;

    if (dashed) {
        mat = new THREE.LineDashedMaterial({linewidth: 2, color: colorHex, dashSize: 5, gapSize: 5});
    } else {
        mat = new THREE.LineBasicMaterial({linewidth: 2, color: colorHex});
    }

    geom.vertices.push(src.clone());
    geom.vertices.push(dst.clone());
    geom.computeLineDistances(); // This one is SUPER important, otherwise dashed lines will appear as simple plain lines

    let axis = new THREE.Line(geom, mat, THREE.LineSegments);
    return axis;
};

let buildAxes = function (length) {
    let axes = new THREE.Object3D();

    axes.add(buildAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(length, 0, 0), 0xFF0000, true)); // +X
    // axes.add(buildAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(-length, 0, 0), 0xFF0000, true)); // -X
    axes.add(buildAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, length, 0), 0x00FF00, true)); // +Y
    // axes.add(buildAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, -length, 0), 0x00FF00, true)); // -Y
    axes.add(buildAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, length), 0x0000FF, true)); // +Z
    // axes.add(buildAxis(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, -length), 0x0000FF, true)); // -Z

    return axes;
};

/*****************************************
 * Egg
 *****************************************/
let RENDER_EGG = "Egg";
let RENDER_LIGHT = "Light";
let RENDER_WIRE = "Wire";

let sphereScale = 2.5, sphereY = 1.3;

let buildEgg = function (group, radius, render_type) {
    // console.log(render_type);

    var loader = new THREE.TextureLoader();
    loader.load('/static/texture.png', function (texture) {

        let geo = new THREE.SphereGeometry(radius * sphereScale, 64, 64);
        geo.applyMatrix(new THREE.Matrix4().makeScale(1.0, sphereY, 1.0));

        geo.mergeVertices();
        geo.computeVertexNormals();

        let material;
        if (render_type === RENDER_WIRE) {
            material = new THREE.MeshBasicMaterial({wireframe: true, color: 0x990000});
        } else if (render_type === RENDER_LIGHT) {
            material = new THREE.MeshLambertMaterial({transparent: true, opacity: 0.6});
        } else {
            material = new THREE.MeshBasicMaterial({map: texture});
        }

        let mesh = new THREE.Mesh(geo, material);
        group.add(mesh);

        // Axis
        let axis_arrow = buildAxes(100 * sphereY * sphereScale);
        group.add(axis_arrow);
    });
};

/*****************************************
 * Shadow
 *****************************************/

let buildShadow = function buildShadow(radius) {
    let canvas = document.createElement('canvas');
    canvas.width = 128;
    canvas.height = 128;

    let context = canvas.getContext('2d');
    let gradient = context.createRadialGradient(
        canvas.width / 2, canvas.height / 2, 0,
        canvas.width / 2, canvas.height / 2, canvas.width / 2
    );
    gradient.addColorStop(.3, 'rgba(200,200,200,1)');
    gradient.addColorStop(1, 'rgba(238,238,238,1)');

    context.fillStyle = gradient;
    context.fillRect(0, 0, canvas.width, canvas.height);

    let texture = new THREE.CanvasTexture(canvas);
    let geometry = new THREE.PlaneBufferGeometry(radius * sphereScale, radius * sphereScale, 3, 3);
    let material = new THREE.MeshBasicMaterial({map: texture, overdraw: 0.5});

    let mesh = new THREE.Mesh(geometry, material);
    mesh.position.y = -280 * sphereScale;
    mesh.rotation.x = -Math.PI / 2;
    return mesh;
};

/*****************************************
 * Sensors
 *****************************************/

let get_sensors_position = function (positions, radius, height, count, offset) {
    var point;

    for (let i = 0; i < count; i++) {
        point = {
            'x': 0.0 + radius * Math.cos(Math.PI * (2 * i + offset) / count),
            'y': height,
            'z': 0.0 + radius * Math.sin(Math.PI * (2 * i + offset) / count)
        };
        positions.push(point);
    }
};

let LIGHT_POINTS_MAT_RED = new THREE.MeshPhongMaterial({color: 0x990000, side: THREE.DoubleSide});
let LIGHT_POINTS_MAT_WHITE = new THREE.MeshPhongMaterial({color: 0xffffff, side: THREE.DoubleSide});
let LIGHT_POINTS_GEO = new THREE.SphereGeometry(20);

let get_sensors_location = function (radius) {
    var eachRow = 8;
    var lights_location = [];

    get_sensors_position(lights_location, radius * sphereScale, radius * 0.75 * sphereScale, eachRow, 0);
    get_sensors_position(lights_location, radius * sphereScale, -radius * 0.75 * sphereScale, eachRow, 0);

    return lights_location;
};

let addSensorPoints = function (obj, lights_location) {
    let _mesh, _loc;

    for (let i = 0; i < lights_location.length; i++) {
        _loc = lights_location[i];
        _mesh = new THREE.Mesh(LIGHT_POINTS_GEO, LIGHT_POINTS_MAT_WHITE);

        _mesh.position.set(_loc.x, _loc.y, _loc.z);
        _mesh.visible = true;

        // light_points[i] = _mesh;
        obj.add(_mesh);
    }
};

let BLACK = new THREE.Color(0x000000);
let WHITE = new THREE.Color(0xffffff);

let addBlackLights = function (obj, lights_location, lights, intensity) {
    let _light, _loc, _color;

    _color = BLACK;
    for (let i = 0; i < lights_location.length; i++) {

        _loc = lights_location[i];

        _light = new THREE.DirectionalLight(_color, intensity);
        _light.position.set(_loc.x, _loc.y, _loc.z);

        lights[i] = _light;

        obj.add(_light);
        obj.add(new THREE.PointLightHelper(_light, 10));
    }

    // console.log(lights)
};

/*****************************************
 * Updator
 *****************************************/

let update_temperature = function (lights, temperature_values, lut) {
    let _color, _sensor_value, _light;

    // console.log(temperature_values);

    if ((lights.length > 0) && (temperature_values != null)) {
        for (let j = 0; j < lights.length; j++) {
            _light = lights[j];

            try {
                _sensor_value = temperature_values[j];
                _color = lut.getColor(_sensor_value);
                _light.color = _color;
            } catch (error) {
                // ignore
            }
        }
    }
};

let AXIS_Z = new THREE.Vector3(0, 0, 0);
let AXIS_X = new THREE.Vector3(1, 0, 0);
let Q_INIT = new THREE.Quaternion();
Q_INIT.setFromAxisAngle(AXIS_X, Math.PI);

let MPU6050_RAW2G = 16384.0;

let update_position = function (obj, position_values) {
    // console.log("in update_position");

    var q = [];

    q[0] = position_values[0]; // w
    q[1] = position_values[1]; // x
    q[2] = position_values[2]; // y
    q[3] = position_values[3]; // z
    //console.log("Quaternion: %j", q);

    // console.log("euler: %j", euler);
    obj.lookAt(AXIS_Z);
    obj.quaternion.multiply(Q_INIT);

    var quaternion = new THREE.Quaternion(q[1], -q[3], q[2], q[0]);
    obj.quaternion.multiply(quaternion);
};