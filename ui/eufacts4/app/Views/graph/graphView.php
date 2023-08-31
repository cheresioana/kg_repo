<!DOCTYPE html>
<html>

<head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Mindbugs | Knowledge graph</title>

    <link href="<?=base_url()?>/public/assets/admin/css/bootstrap.min.css" rel="stylesheet">
    <link href="<?=base_url()?>/public/assets/admin/font-awesome/css/font-awesome.css" rel="stylesheet">

    <link href="<?=base_url()?>/public/assets/admin/css/animate.css" rel="stylesheet">
    <link href="<?=base_url()?>/public/css/graph/style.css" rel="stylesheet">
    <link href="<?=base_url()?>/public/assets/admin/css/style.css" rel="stylesheet">
    <link href="<?=base_url()?>/public/assets/admin/css/graph_style.css" rel="stylesheet">
    <style>
        .float{
            position:fixed;
            width:60px;
            height:60px;
            bottom:40px;
            right:40px;
            background-color:#0C9;
            color:#FFF;
            border-radius:50px;
            text-align:center;
            box-shadow: 2px 2px 3px #999;
        }

        .my-float{
            margin-top:22px;
        }
    </style>
</head>

<body class="gray-bg">
<div class="row" >

    <div  id="container" class="info_bar col-lg-4 col-md-4 info_style" style="">

    </div>
<!--        <div id="info_bar" class="card col-lg-3">-->
<!--            <div class="card-body">-->
<!--                <h2 class="card-title">Card title</h2>-->
<!--                <h6 class="card-subtitle mb-2 text-muted">Card subtitle</h6>-->
<!--                <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>-->
<!--                <a href="#" class="card-link">Card link</a>-->
<!--                <a href="#" class="card-link">Another link</a>-->
<!--            </div>-->
<!--        </div>-->
    <div id="3d-graph" class="col-lg-8"></div>
</div>
<a href="#" class="float" id="btnAddStatement">
    <i class="fa fa-plus my-float"></i>
</a>



<script src="//unpkg.com/three"></script>
<script src="//unpkg.com/d3"></script>
<script src="<?=base_url()?>/public/assets/admin/js/3d-force-graph.min.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
<script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
<script type="importmap">{ "imports": { "three": "https://unpkg.com/three/build/three.module.js" }}</script>

<script type="module">

</script>

<style>
    .node-label {
        font-size: 12px;
        padding: 1px 4px;
        border-radius: 4px;
        background-color: rgba(0,0,0,0.5);
        user-select: none;
    }
</style>
<script src="//unpkg.com/three-spritetext"></script>
<script src="<?=base_url()?>/public/js/graph.js"></script>
<script type="module" src="<?=base_url()?>/public/js/init_graph.js"></script>
<script type="module">


</script>


</body>

</html>