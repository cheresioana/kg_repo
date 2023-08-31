
// const nodes = $.ajax({
//     type: 'GET',
//     url: 'http://127.0.0.1:5000/kg',
//     dataType: 'json',
//     success: function( data ) {
//         console.log(data)
//
//         const Graph = ForceGraph3D({
//             extraRenderers: [new CSS2DRenderer()]
//         })
//         (document.getElementById('3d-graph'))
//             .graphData(data)
//             //.jsonUrl('<?=base_url()?>/public/assets/datasets/kg2.json')
//             .nodeLabel('statement')
//             .nodeAutoColorBy('tag')
//             .linkWidth(link => 2)
//             //.nodeColor(node => nodeColorScale(node.tag))
//             .onNodeDragEnd(node => {
//                 node.fx = node.x;
//                 node.fy = node.y;
//                 node.fz = node.z;
//             })
//             .nodeThreeObject(node => {
//                 // This is with text only nodes
//                 /*const sprite = new SpriteText(node.statement.split(' ').slice(0,2).join(' '));
//                 sprite.material.depthWrite = false; // make sprite background transparent
//                 sprite.color = node.color;
//                 sprite.textHeight = 8;
//                 return sprite;*/
//
//                 const nodeEl = document.createElement('div');
//
//                 if (node.tag == "fake_news")
//                     nodeEl.textContent = 'FAKE';
//                 else
//                     nodeEl.textContent = node.statement;
//                 nodeEl.style.color = node.color;
//                 nodeEl.className = 'node-label';
//                 return new CSS2DObject(nodeEl);
//
//             })
//             .nodeThreeObjectExtend(true)
//             .onNodeClick((node, event) => {
//                 //var x = document.getElementById("info_bar");
//                 //x.classList.add('show');
//                 console.log(node)
//                 if (selectedNodes.has(node)) {
//                     selectedNodes.delete(node)
//                     $("#" + node.id).fadeOut();
//                     //element.remove();
//                 } else {
//                     selectedNodes.add(node);
//                     addInfoCard(node);
//
//                 }
//                 updateHighlight()
//                 //moveToNode()
//             });
//     }
// })

// const nodeEl = document.createElement('div');
// if (node.tag=== 'fake_news'){
//     nodeEl.textContent = node.statement.substring(0, 20) + "...";
//     nodeEl.style.color = '#ffc93c';
//     nodeEl.color = 'rgba(255, 255, 255, 255)';
//     nodeEl.style.opacity = 0.35;
// }
// else {
//     nodeEl.textContent = node.name;
//     nodeEl.style.color = '#ff6f3c'
// }
//
// nodeEl.className = 'node-label';
// return new CSS2DObject(nodeEl)

// const sprite = new SpriteText()
// if (node.tag=== 'fake_news'){
//     sprite.text = node.statement.substring(0, 20) + "...";
//     sprite.textContent = node.statement.substring(0, 20) + "...";
//     sprite.color = '#67f5ef';
//     sprite.material.opacity = 0.4;
//     sprite.textHeight = 6;
//
//     //sprite.style.opacity = 0.35;
// }
// else {
//     sprite.text = node.name;
//     sprite.textContent = node.name;
//     sprite.color = '#ff6f3c'
//     sprite.textHeight = 8;
// }
// sprite.material.depthWrite = false; // make sprite background transparent
// return sprite

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
const doubleClickDelay = 300; // Milliseconds
let clickedNodeId = null;
let clickedNodeTimer = null;
let Graph = null
function click_node(node) {
    /*if (clickedNodeId === node.id) {
        // This node has been clicked before within the delay period.
        // This is a double click.
        console.log('Node double clicked:', node);
        clearTimeout(clickedNodeTimer);
        const nodes = $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:5005/get_similar/' + node.id,
            dataType: 'json',
            success: function (data) {
                console.log(data)
                console.log('http://127.0.0.1:5005/get_similar/' + node.id)
                let { nodes, links } = Graph.graphData();
                for (var entry of data['nodes']){
                    let obj = nodes.find(o => o.id === entry.id)
                    if(obj == null){
                        console.log("element not found" + entry)
                        nodes.append(entry)
                    }
                    else console.log(obj)
                }
                console.log(links)
                let new_links = links
                new_links.push(...data['links'])
                console.log(new_links)

                Graph
                    .nodeThreeObject((node) => {
                        if (node.id === clickedNodeId) {

                            console.log("found")
                            console.log(node)
                            const distance = 10;
                            const distRatio = 1 + distance / Math.hypot(node.x, node.y, node.z);

                            const newPos = node.x || node.y || node.z
                                ? {x: node.x * distRatio + 150, y: node.y * distRatio, z: node.z * distRatio + 200}
                                : {x: 0, y: 0, z: distance}; // special case if node is in (0,0,0)

                            Graph.cameraPosition(
                                newPos, // new position
                                node, // lookAt ({ x, y, z })
                                3000  // ms transition duration
                            );
                            clickedNodeId = null; // Reset
                        }
                        return simple_nodes(node)
                    });
            }
        })

    } else {
        // This is the first click on this node.
        clickedNodeId = node.id;
        clickedNodeTimer = setTimeout(() => {
            clickedNodeId = null; // Reset after the delay period
        }, doubleClickDelay);
    }*/
}
function get_kg_url() {
    const nodes = $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:5005/get_kg',
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
                .onNodeClick(node => click_node(node))
                .nodeThreeObjectExtend(true)

            Graph.cameraPosition(
                { z: 300 },  // new position
                { x: 0, y: 0, z: 0 },  // look-at position
                3000  // transition duration
            );
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
                }, 10);}, 3000);


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


// This is a sample for calling a url for the kg with 10 nodes
function sample_with_url() {
    const nodes = $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:5005/sample_kg',
        dataType: 'json',
        success: function (data) {
            console.log(data)

            const Graph = ForceGraph3D()
            (document.getElementById('3d-graph'))
                .graphData(data)
                .onNodeDragEnd(node => {
                    node.fx = node.x;
                    node.fy = node.y;
                    node.fz = node.z;
                })

        }
    })
}
//sample_with_url()



//This is a sample graph for testing
function sample_graph() {
    const N = 300;
    const gData = {
        nodes: [...Array(N).keys()].map(i => ({id: i})),
        links: [...Array(N).keys()]
            .filter(id => id)
            .map(id => ({
                source: id,
                target: Math.round(Math.random() * (id - 1))
            }))
    };

    const Graph = ForceGraph3D()
    (document.getElementById('3d-graph'))
        .graphData(gData);
}

function updateGraphAnalyze(data){


    var origin_node = data['origin'][0]["id"]
    var my_data2 = {}
    my_data2["nodes"]= data["nodes"]
    my_data2["links"] = data['links']
    console.log(data)

    Graph.graphData(my_data2)
        .nodeAutoColorBy('tag')
        .nodeLabel('statement')
        .nodeThreeObject(node => {


            const nodeEl = document.createElement('div');

            if (node.id === origin_node){
                nodeEl.textContent = node.statement;
                nodeEl.color = '#e13131'
            }
            else if (node.tag=== 'key_element'){
                nodeEl.textContent = node.statement;
                nodeEl.style.color = '#ff6f3c'

            }
            else {
                nodeEl.textContent = node.statement
                nodeEl.style.color = '#b3eae7';
                nodeEl.color = '#67f5ef';
                nodeEl.style.opacity = 0.45;

            }

            /*nodeEl.textContent = node.statement;
            nodeEl.style.color = node.color;
            nodeEl.className = 'statement';*/
            return new CSS2DObject(nodeEl);
        })
        .onNodeDragEnd(node => {
            node.fx = node.x;
            node.fy = node.y;
            node.fz = node.z;
        })
        .onNodeClick(node => click_node(node))
        .nodeThreeObjectExtend(true)

    Graph.zoomToFit(230);


}

function openPanel() {
    const p = document.createElement("div")
    p.id = "add"
    p.classList.add("card",  "info-bar", "mt-1")
    p.style.direction="ltr"
    const card_body = document.createElement("div")
    card_body.classList.add("card-body")
    const h2 = document.createElement("h3")
    h2.classList.add("card-title")
    h2.appendChild(document.createTextNode("Add a new statement"))
    const pp2 = document.createElement("h5")
    pp2.classList.add("card-subtitle","mb-2","text-muted", "mt-1")
    const input1 = document.createElement("input")
    input1.classList.add("form-control")
    input1.value = "Nazis from Ukraine are going to invade Russia according to Vladimir Putin"
    const close = document.createElement("span")
    close.classList.add('pull-right','clickable', 'close-icon')
    close.onclick = function() {
        console.log("click close")
        let card = $(this).closest('.card')
        //remove_node_id(card[0].id)
        console.log(card)
        $(this).closest('.card').fadeOut();
    }

    const ifa_close = document.createElement("i")
    ifa_close.classList.add('fa','fa-times')
    close.appendChild(ifa_close)
    card_body.appendChild(close)
    const btn1 = document.createElement("button")
    btn1.classList.add("btn","btn-primary", "mt-2")
    btn1.textContent="Analyze"

    btn1.onclick = function () {
        var payload = {
            "statement": input1.value
        }
        $.ajax({
            type: 'POST',
            url: 'http://127.0.0.1:5005/analyze',
            data: JSON.stringify(payload),
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            success: function (data) {
                console.log(data)
                console.log("on focus")

                btn1.style.display = 'none';
                var keywords = data['keywords']
                var debunk = data["debunk"]
                var keywords_html = ''
                var i = 0;
                for (var keyw of keywords) {
                    console.log(keyw)
                    var class_name = "badge-info"
                    if (i % 2 == 0) {
                        class_name = "badge-success"
                    }
                    i = i + 1
                    keywords_html += '<span class="badge ' + class_name + ' ml-2 mb-2" style="font-size:20px"> ' + keyw + '<a href="#" style="font-size: 15px; color: white; margin-left:5px "> x</a> </span>'
                }
                let ss;
                ss = `
                <div class="form-group row mt-4 justify-content-center">
                    <div class="col-lg-3"><label style="font-size:20px">Keywords</label></div>
                    <div class="col-lg-9">
                       ` + keywords_html + `
                    </div>
                </div>
                <div class="form-group row mt-1">
                    <label for="inputPassword" class="col-sm-3 col-form-label" style="font-size:20px">Suggestions</label>
                        <div class="col-sm-9">
                            <textarea type="text" rows="10" class="form-control" id="inputPassword" placeholder="Suggestiions"> `+ debunk +` </textarea>
                </div>
        </div>`

                card_body.style.height = "100%"
                card_body.insertAdjacentHTML('beforeend', ss);
                updateGraphAnalyze(data['subgraf'])

            }
        })
    }
        console.log("ok")

    card_body.appendChild(h2)
    //card_body.appendChild(badge_row2)
    card_body.appendChild(pp2)
    card_body.appendChild(input1)
    card_body.appendChild(btn1)
    //card_body.appendChild(pp)
    //card_body.appendChild(ahref)
    p.appendChild(card_body)


    const element = document.getElementById("container");

    element.insertBefore(p, element.firstChild)

    p.classList.add('show');
    element.classList.add('show')
    console.log(p)
}

document.getElementById ("btnAddStatement").addEventListener ("click", openPanel, false);

//sample_graph()