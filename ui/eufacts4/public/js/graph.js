// import { UnrealBloomPass } from '//unpkg.com/three/examples/jsm/postprocessing/UnrealBloomPass.js';
// import { CSS2DRenderer, CSS2DObject } from '//unpkg.com/three/examples/jsm/renderers/CSS2DRenderer.js';
const nodeColorScale = d3.scaleOrdinal(d3.schemeRdYlGn[4]);
let selectedNodes = new Set();

var onfocus = 0;


var sphereMesh = function(node) {
    // Glow sphere mesh.

    if(selectedNodes.has(node)) {
        const original_color = nodeColorScale(node.tag)
        const glowSize = 10;
        const geometry = new THREE.SphereGeometry(glowSize, 32, 32);
        const material = new THREE.MeshLambertMaterial({
            color: original_color,
            transparent: true,
            opacity: 0.3
        });
        const glowEffect = new THREE.Mesh(geometry, material);
        glowEffect.name = "glow";

        // Smaller solid sphere mesh.
        const geometrySolid = new THREE.SphereGeometry(5, 32, 32);
        const materialSolid = new THREE.MeshLambertMaterial({
            color: original_color,
            transparent: false,
            opacity: 1.0
        });
        const mesh = new THREE.Mesh(geometrySolid, materialSolid);
        mesh.name = "node";

        // Place the smaller solid sphere inside the large glow sphere.
        var group = new THREE.Group();
        group.add(mesh);
        group.add(glowEffect);
        return group;
    }
}

function addInfoCard(node){

    $.ajax({
        type: 'GET',
        url: '<?=base_url()?>/graph/graph/getFakeNews/'+node.id,
        dataType: 'json',
        success: function( data ) {

            const p = document.createElement("div")
            p.id = data["id"]
            p.classList.add("card",  "info-bar", "mt-1")
            p.style.maxHeight="320px"
            p.style.overflowY="scroll"
            p.style.direction="ltr"
            const card_body = document.createElement("div")
            card_body.classList.add("card-body")
            const h2 = document.createElement("h3")
            h2.classList.add("card-title")
            h2.appendChild(document.createTextNode(data["statement"]))
            const pp2 = document.createElement("h5")
            pp2.classList.add("card-subtitle","mb-2","text-muted", "mt-1")
            pp2.appendChild(document.createTextNode(data["summary_explanation"]))
            const pp = document.createElement("p")
            pp.classList.add("card-text")
            pp.appendChild(document.createTextNode(data["full_explanation"]))
            const badge_row = document.createElement("div")
            badge_row.classList.add('col')
            const pp3 = document.createElement("span")
            pp3.appendChild(document.createTextNode(data["verdict"]))
            switch (data['verdict']){
                case 'false':
                case 'mostly-false':
                    pp3.classList.add("badge","badge-danger")
                    break;
                case 'half-true':
                    pp3.classList.add("badge","badge-warning")
                    break;
                default:
                    pp3.classList.add("badge","badge-success")
                    break;
            }
            pp3.classList.add("mr-1")
            const pp4 = document.createElement("span")
            pp4.appendChild(document.createTextNode(data["debunk_date"]))
            pp4.classList.add("badge","badge-light","mr-1")
            const pp5 = document.createElement("span")
            pp5.appendChild(document.createTextNode(data["owner"]))
            pp5.classList.add("badge","badge-light", "mr-1")
            badge_row.appendChild(pp3)
            badge_row.appendChild(pp4)
            badge_row.appendChild(pp5)
            const badge_row2 = document.createElement("div")
            badge_row2.classList.add('row')
            badge_row2.appendChild(badge_row)

            badge_row2.classList.add('row')
            badge_row2.appendChild(badge_row)

            const ahref = document.createElement("a")
            ahref.href = data["debunk_link"]
            ahref.classList.add('card-link')
            ahref.appendChild(document.createTextNode('Original debunk'))

            const close = document.createElement("span")
            close.classList.add('pull-right','clickable', 'close-icon')
            close.onclick = function() {
                let card = $(this).closest('.card')
                remove_node_id(card[0].id)
                $(this).closest('.card').fadeOut();
            }
            const ifa_close = document.createElement("i")
            ifa_close.classList.add('fa','fa-times')
            close.appendChild(ifa_close)

            card_body.appendChild(close)
            card_body.appendChild(h2)
            card_body.appendChild(badge_row2)
            card_body.appendChild(pp2)
            card_body.appendChild(pp)
            card_body.appendChild(ahref)
            p.appendChild(card_body)


            const element = document.getElementById("container");

            element.insertBefore(p, element.firstChild)

            p.classList.add('show');
            element.classList.add('show')
            console.log(p)
        }
    });
}


function remove_node_id(id){
    selectedNodes.forEach((point) => {

        if (point.id == id) {
            console.log(id)
            selectedNodes.delete(point);
        }
    });
    updateHighlight()
}

function updateHighlight() {
    console.log("updateHighlights")
    console.log(onfocus)
    Graph
        .nodeThreeObject((node) => {
            // This is with text only nodes
            /*
                const sprite = new SpriteText(node.statement.split(' ').slice(0,2).join(' '));
                sprite.material.depthWrite = false; // make sprite background transparent

                sprite.textHeight = 8;

                sprite.color = node.color;
                if (selectedNodes.has(node))
                    sprite.color = 'red';
                return sprite;
                */
            //  if (onfocus !== 0)

            const nodeEl = document.createElement('div');
            nodeEl.textContent = node.statement.split(' ').slice(0,2).join(' ');
            nodeEl.style.color = node.color;
            nodeEl.className = 'node-label';
            if (selectedNodes.has(node))
                nodeEl.style.color = 'red';
            return new CSS2DObject(nodeEl);

        })
}
function moveToNode()
{
    Graph
        .nodeThreeObject((node) => {
            if (node.id === -1) {
                console.log("found")
                console.log(node)
                const distance = 200;
                const distRatio = 1 + distance / Math.hypot(node.x, node.y, node.z);

                const newPos = node.x || node.y || node.z
                    ? {x: node.x * distRatio +150, y: node.y * distRatio, z: node.z * distRatio + 200}
                    : {x: 0, y: 0, z: distance}; // special case if node is in (0,0,0)

                Graph.cameraPosition(
                    newPos, // new position
                    node, // lookAt ({ x, y, z })
                    3000  // ms transition duration
                );
            }
            const nodeEl = document.createElement('div');
            nodeEl.textContent = node.statement.split(' ').slice(0,2).join(' ');
            nodeEl.style.color = node.color;
            nodeEl.className = 'node-label';
            if (selectedNodes.has(node))
                nodeEl.style.color = 'red';
            return new CSS2DObject(nodeEl);
        });
}

// const bloomPass = new UnrealBloomPass();
// bloomPass.strength = 3;
// bloomPass.radius = 1;
// bloomPass.threshold = 0.1;
//Graph.postProcessingComposer().addPass(bloomPass);





    var data = [{
    type: 'scattergeo',
    mode: 'markers',
    locations: ['AUT', 'CZE', 'DEU', 'POL', 'ROU', 'HUN', 'SVN', 'SVK'],
    marker: {
    size: [10, 7, 15, 10, 15, 9, 8, 10, 7],
    sizemode: 'diameter',
    color: [10, 7, 15, 10, 15, 9, 8, 10, 7],
    cmin: 0,
    cmax: 50,
    colorscale: 'Blues',
    colorbar: {
    title: 'frequency',
    ticksuffix: '/week',
    showticksuffix: 'last'
},
    line: {
    color: 'None'
}
},
    name: 'europe data'
}];

    var frames = [];
    var numFrames = 60;

    for (var i = 0; i < numFrames; i++) {
    var frame = {
    name: i.toString(),
    data: [{
    type: 'scattergeo',
    mode: 'markers',
    locations: ['AUT', 'CZE', 'DEU', 'POL', 'ROU', 'HUN', 'SVN', 'SVK'],
    marker: {
    size: [
    10 * 1.02 ** i,
    7 * 1.02 ** i,
    15 * 1.02 ** i,
    10 * 1.02 ** i,
    9 * 1.02 ** i,
    8 * 1.02 ** i,
    10 * 1.02 ** i,
    7 * 1.02 ** i
    ],
    sizemode: 'diameter',
    color: [10, 7, 15, 10, 15, 9, 8, 10, 7],
    cmin: 0,
    cmax: 50,
    colorscale: 'Blues',
    colorbar: {
    title: 'frequency',
    ticksuffix: '/week',
    showticksuffix: 'last'
},
    line: {
    color: 'None'
}
}
}]
};
    frames.push(frame);
}

    var layout = {
    //title: 'Europe Bubble Map Animation',
    title: 'Location and evolution of the attacks',
    showlegend: false,
    font: {
    size: 9 // Set the desired font size in pixels
},
    geo: {
    scope: 'europe',
    //resolution: 50
}
};

    var config = {
    displayModeBar: false
};

    function startAnimation() {
    Plotly.animate('myDiv', null, {
        frame: {
            duration: 50,
            redraw: true
        },
        transition: {
            duration: 0
        }
    }, function(){
        // Animation completed, restart the animation
        startAnimation();
    });
}

    function graph_bubble() {


    Plotly.newPlot('myDiv', data, layout, config).then(function () {
        Plotly.addFrames('myDiv', frames);
        startAnimation(); // Start the animation initially

        setTimeout(graph_bubble, 4000);
    })
}
