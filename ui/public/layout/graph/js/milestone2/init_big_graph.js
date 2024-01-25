import { CSS2DRenderer, CSS2DObject } from '//unpkg.com/three/examples/jsm/renderers/CSS2DRenderer.js';

function simple_nodes(node){
    const nodeEl = document.createElement('div');
    if (node.tag=== 'fake_news'){
        nodeEl.textContent = node.statement.substring(0, 20) + "...";
        nodeEl.style.color = '#b3eae7';
        nodeEl.color = '#67f5ef';
        nodeEl.style.opacity = 0.45;

    }
    else {
        nodeEl.textContent = node.name;
        nodeEl.style.color = '#ff6f3c'
    }

    nodeEl.className = 'node-label';
    //print(nodeEl)
    return new CSS2DObject(nodeEl)
}

let Graph = null
function get_kg_url() {
    const nodes = $.ajax({
        type: 'GET',
        // url: 'http://localhost/eufacts4/public/GraphJson/michael_data.json',
        url: 'https://call_backend',
        dataType: 'json',
        success: function (data) {
            console.log(data)
            Graph = ForceGraph3D({
                extraRenderers: [new CSS2DRenderer()]
            })


            (document.getElementById('3d-graph'))
                .graphData(data)
                .nodeColor(node =>{
                    if (node.tag=== 'fake_news')
                        return 'rgba(103, 245, 239, 0.3)'
                    else
                        return 'rgba(255, 111, 60, 0.8)'
                })
                .nodeLabel('statement')
                .nodeThreeObject(node => simple_nodes(node))
                .onNodeDragEnd(node => {
                    node.fx = node.x;
                    node.fy = node.y;
                    node.fz = node.z;
                })
                //.width(800)
                .onNodeClick(node => addInfoCard(node))
                //.linkWidth(0.3)
                .nodeThreeObjectExtend(true)

            Graph.cameraPosition(
                { z: 300 },  // new position
                { x: 0, y: 0, z: 0 },  // look-at position
                3000  // transition duration
            );
            //Container.width(100)

            let angle = 0;
            let distance = 300
            let isRotationActive = true;
            setTimeout(() => {
                setInterval(() => {
                    if (isRotationActive) {
                        Graph.cameraPosition({
                            x: distance * Math.sin(angle),
                            z: distance * Math.cos(angle)
                        });
                        angle += Math.PI / 300;
                    }
                }, 50);}, 3000);


            document.getElementById('3d-graph').addEventListener('click', event => {
                isRotationActive = false;
                //event.target.innerHTML = `${(isRotationActive ? 'Pause' : 'Resume')} Rotation`;
            });
            document.getElementById('btnAddStatement').addEventListener('click', event => {
                isRotationActive = false;
                //event.target.innerHTML = `${(isRotationActive ? 'Pause' : 'Resume')} Rotation`;
            });
        }
    })
}

get_kg_url()



